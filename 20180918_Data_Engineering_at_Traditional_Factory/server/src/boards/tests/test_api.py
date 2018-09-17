# boards/tests/test_api.py
import requests
import json
import datetime
import alog
import time

ip = 'localhost:8000'
url = f"http://{ip}/boards/records/"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {
    'machine': 1,
    'rs232_time': None,
    'datas': {},
}

data = payload.copy()
data['num'] = 0
data['rs232_time'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
data['record_datas'] = {'measure_1': 1.05, 'measure_2': 2.10}

# create
r = requests.post(url, json=json.dumps(data))
alog.info(f"{r.status_code}, {r.json()}")


# delete
target = r.json().get('recordid')
alog.info(f"Delete: {target}")
r = requests.delete(f"{url}{target}")
alog.info(f"{r.status_code}")