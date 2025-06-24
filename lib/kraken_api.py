
"""Provide several sample math calculations.

This module allows the user to make mathematical calculations.

The module contains the following functions:

- `add(a, b)` - Returns the sum of two numbers.
- `subtract(a, b)` - Returns the difference of two numbers.
- `multiply(a, b)` - Returns the product of two numbers.
o numbers.
"""

# imports
import requests
import hmac
import hashlib
import base64
import urllib.parse
import json
import time
import lib

# constants
api_url = "https://api.kraken.com"


#######################################################################
############################# functions ###############################
#######################################################################
############################## general ################################

# get api from key.file
def get_api_pair(data, api_name):
    """_summary_

    Args:
        data (_type_): _description_
        api_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    for key in data:
        if data[key]['name'] == api_name:
            return data[key]['api_key'], data[key]['api_sec']

# get kraken Signature
def get_kraken_signature(urlpath, data, secret):
    """_summary_

    Args:
        urlpath (_type_): _description_
        data (_type_): _description_
        secret (_type_): _description_

    Returns:
        _type_: _description_
    """
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce'])+ postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

# attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec, api_url):
    """_summary_

    Args:
        uri_path (_type_): _description_
        data (_type_): _description_
        api_key (_type_): _description_
        api_sec (_type_): _description_
        api_url (_type_): _description_

    Returns:
        _type_: _description_
    """
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req


    
############################## general ################################
#######################################################################
########################### public endpoint ###########################

def ticker():
    """_summary_

    Returns:
        _type_: _description_
    """
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=XMREUR')
    # print(resp.json())
    return resp.json()

########################### public endpoint ###########################
#######################################################################
############################## privat endpoint ########################

# get account balances
def get_acc_balance(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000*time.time()))
    }, api_key, api_sec, api_url)
    # print(resp.json())
    ### to catch only the result part
    data = resp.json()['result']
    # print(data)
    lib.create_balance_table(data)
    print('\n')

# get trade balances
def get_trade_balance(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    asset = input("Enter Währung: ")
    resp = kraken_request('/0/private/TradeBalance', {
        "nonce": str(int(1000*time.time())), # Required
        "asset": asset
    }, api_key, api_sec, api_url)
    # print(resp.json())
    data = resp.json()['result']
    lib.create_balance_table(data)
    print('\n')

# get open orders <----- Achtung!
def get_open_orders(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/OpenOrders', {
        "nonce": str(int(1000*time.time())), # Required
        "trades": True
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# get closed orders <---- Achtung!
def get_closed_orders(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/ClosedOrders', {
        "nonce": str(int(1000*time.time())), # Required
        "trades": '',
        "userref": 36493663,
        "start": '',
        "end": '',
        "ofs":'',
        "closetime": ''
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')


# Query Orders Info <---- Achtung!
def query_orders_info(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/QueryOrders', {
        "nonce": str(int(1000*time.time())), # Required
        "trades": '',
        "userref": '',
        "txid": "OBCMZD-JIEE7-77TH3F,OMMDB2-FSB6Z-7W3HPO",
        "consolidate_take": ''
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Get Trades History <---- Achtung!
def get_trades_history(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/TradesHistory', {
        "nonce": str(int(1000*time.time())), # Required
        "type": '',
        "trades": '',
        "start": '',
        "end": '',
        "ofs":'',
        "consolidate_take": ''
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Query Trade Info <---- Achtung!
def query_trades_info(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/QueryTrades', {
        "nonce": str(int(1000*time.time())), # Required
        "txid": "", # REQUIRED
        "trades": True
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Get Open Positions <---- Achtung!
def get_open_positions(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/OpenPositions', {
        "nonce": str(int(1000*time.time())), # Required
        "trades": '',
        "userref": '',
        "start": '',
        "end": '',
        "ofs":'',
        "closetime": ''
}, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Get Ledgers Info <---- Achtung!
def get_ledgers_info(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/Ledgers', {
        "nonce": str(int(1000*time.time())), # Required
        "asset": '',
        "aclass": '',
        "type": '',
        "start": '',
        "end": '',
        "ofs":''
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Query Ledgers <---- Achtung!
def query_ledgers_info(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/QueryLedgers', {
        "nonce": str(int(1000*time.time())), # Required
        "id": '',
        "trades": '',
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Get Trade Volume <---- Achtung!
def get_trade_volume(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/TradeVolume', {
        "nonce": str(int(1000*time.time())), # Required
        "pair": ''
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Request Export Report <---- Achtung!
def request_export_report(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/AddExport', {
        "nonce": str(int(1000*time.time())), # Required
        "report": '', # Required
        "format": '',
        "description": '', # Required
        "fields": '',
        "starttm": '',
        "endtm": ''
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Get Export Report Status <---- Achtung!
def get_export_report_status(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/GetExportReportStatus', {
        "nonce": str(int(1000*time.time())), # Required
        "report": 'ledgers' # Required
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Retrieve Data Export <---- Achtung!
def retrieve_data_export(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/RetrieveExport', {
        "nonce": str(int(1000*time.time())), # Required
        "id": '' # Required
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

# Delete Export Report <---- Achtung!
def delete_export_report(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/RemoveExport', {
        "nonce": str(int(1000*time.time())), # Required
        "id": '', # Required
        "type": '' # Required
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

############################## user data #################################
##########################################################################
############################# user trading ###############################

# Withdraw Fund <---- Achtung!
def withdraw_fund(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    with open('config/api/withdraw_db.json', 'r') as f:
        data = json.load(f)
    id = input("Geben Sie die Bezeichnung ein: ")
    selected_data = data[str(id)]
    nonce = str(int(1000*time.time()))
    print(selected_data['asset'])
    print(selected_data['key'])
    betrag = input("Geben Sie die Höhe des Betrags ein: ")
    resp = kraken_request('/0/private/Withdraw', {
    "nonce": nonce, 
    "asset": selected_data['asset'],
    "key": selected_data['key'],
    "amount": betrag
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n') 

# Add Order <---- Achtung!
def add_order(api_key, api_sec):
    """_summary_

    Args:
        api_key (_type_): _description_
        api_sec (_type_): _description_
    """
    resp = kraken_request('/0/private/AddOrder', {
    "nonce": str(int(1000*time.time())),
    "ordertype": "limit",
    "type": "buy",
    "volume": 0,
    "pair": "XBTUSD",
    "price": 27500
    }, api_key, api_sec, api_url)
    print(resp.json())
    print('\n')

