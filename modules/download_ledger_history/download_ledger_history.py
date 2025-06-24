import datetime
import time
import hashlib
import hmac
import base64
import json
import urllib.parse
import requests
import os
import csv
import pandas as pd

# Definitions
date_time = datetime.datetime.now().strftime("%Y")
file_name = 'output/download_ledger_history/ledger_history_' + date_time
api_url = "https://api.kraken.com"
api_name = 'AllPerm'


def get_api_pair(api_name):
    try:
        with open('config/api/kraken_key.json') as json_data:
            data = json.load(json_data)
    except:
        data = {}

    api_key = data[api_name]['api_key']
    api_sec = data[api_name]['api_sec']
    return api_key, api_sec


# Read Kraken API key and secret stored in environment variables
api_key, api_sec = get_api_pair(api_name)


def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce'])+ postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req 
           
    
# Construct the request and print the result

start_date = input("Please enter start date and time (YYYY-MM-DD HH:MM:SS): ")
end_date = input("Please enter end date and time (YYYY-MM-DD HH:MM:SS): ")
start_timestamp = int(datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').timestamp())
end_timestamp = int(datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').timestamp())

resp = kraken_request('/0/private/Ledgers', {
    "nonce": str(int(1000*time.time())),
    "start": start_timestamp,
    "end": end_timestamp,
}, api_key, api_sec)

data = resp.json()

print(data)

trades_data = data['result']['ledger']

# Convert Unix timestamps to readable datetime strings
for trade in trades_data.values():
    trade['time'] = datetime.datetime.fromtimestamp(int(trade['time'])).strftime('%Y-%m-%d %H:%M:%S')

if not os.path.exists(os.path.dirname('output/download_ledger_history/')):
    os.makedirs(os.path.dirname('output/download_ledger_history/'))

with open(file_name + '.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=trades_data[next(iter(trades_data))].keys())
    writer.writeheader()
    for trade in trades_data.values():
        writer.writerow(trade)

df = pd.read_csv(file_name + '.csv')
df.to_excel(file_name + '.xlsx')
