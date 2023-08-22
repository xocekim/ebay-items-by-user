# ebay-items-by-user
find all items from a store on ebay uk and send alerts of new or missing items via pushover

## quick setup
```shell
python3 -mvenv venv
. venv/bin/activate
python -mpip install --upgrade pip
pip install -r requirements.txt
echo -e "$(crontab -l)\n* * * * * cd $(dirname $(realpath main.py)) && venv/bin/python main.py giffgaff" | crontab -
```
