import json
import requests
import sys

from mysecrets import EBAY_APP_ID, PUSHOVER_KEY, PUSHOVER_USER

from ebaysdk.finding import Connection

def send_pushover(title, msg):
    data = {'token': PUSHOVER_KEY, 'user': PUSHOVER_USER, 'message': msg, 'title': title}
    requests.post('https://api.pushover.net/1/messages.json', data=data)

SELLER_NAME = 'giffgaff'
site_id = 'EBAY-GB'
api = Connection(config_file=None, siteid=site_id, appid=EBAY_APP_ID)
request = {'storeName': sys.argv[1] or SELLER_NAME,
           'paginationInput': {'entriesPerPage': 100, 'pageNumber': 1},
           'itemFilter': [{'name': 'MinQuantity', 'value': '1'}]}

items = {}
page = 1
while True:
    request['paginationInput']['pageNumber'] = page
    response = api.execute('findItemsIneBayStores', request)
    if response.reply.searchResult._count == '0':
        break
    for item in response.reply.searchResult.item:
        items[item.itemId] = {'title': item.title, 'price': item.sellingStatus.currentPrice.value}
    if int(response.reply.paginationOutput.totalPages) == page:
        break
    page += 1

try:
    old_items = json.load(open('items.json', 'r'))
except FileNotFoundError:
    old_items = items

missing_items = { item_id: item for item_id, item in old_items.items() if item_id not in items }
new_items = { item_id: item for item_id, item in items.items() if item_id not in old_items }
if missing_items:
    send_pushover('Missing items', '\n'.join([f'{item["title"]} - £{item["price"]} https://www.ebay.co.uk/itm/{item_id}' for item_id, item in missing_items.items()]))
if new_items:
    send_pushover('New items', '\n'.join([f'{item["title"]} - £{item["price"]} https://www.ebay.co.uk/itm/{item_id}' for item_id, item in new_items.items()]))
json.dump(items, open('items.json', 'w'))
