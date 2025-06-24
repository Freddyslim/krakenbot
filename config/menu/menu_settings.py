# Settings for Interface Menu

# imports
import os
import sys

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, lib_path)
import lib.kraken_api as kraken_api

################## main Menu ####################
main_menu_items = {
    1: 'Bearbeiten der APIKeys',
    2: 'Bearbeiten der withdraw Adressen',
    3: 'Kraken Request',
    4: 'Telegram Bot starten',
    5: 'Chatbots',
    99: 'Zurück'
}
############## kraken request menu ##############

kraken_request_menu_items = {
    1: "User Data",
    2: "Trading",
    3: "Funding",
    4: "Subaccount",
    5: "Staking",
    6: "Websocket",
    7: "Ticker",
    99: "Zurück"
}
# user data 
# menu
user_data_menu_items = {
    1: 'Get Account Balance',
    2: 'Get Trade Balance',
    3: 'Get Open Orders',
    4: 'Get Closed Orders',
    5: 'Query Orders Info',
    6: 'Get Trades History',
    7: 'Query Trades Infos',
    8: 'Get Open Positions',
    9: 'Get Ledgers Info',
    10: 'Query Ledgers',
    11: 'Get Trade Volume',
    12: 'Request Export Report',
    99: 'Zurück'
}
# functions
user_data_requests = {
    '1': kraken_api.get_acc_balance,
    '2': kraken_api.get_trade_balance,
    '3': kraken_api.get_open_orders,
    '4': kraken_api.get_closed_orders,
    '5': lambda k, s: kraken_api.query_orders_info(input('TXID: '), k, s),
    '6': kraken_api.get_trades_history,
    '7': lambda k, s: kraken_api.query_trades_info(input('TXID: '), k, s),
    '8': kraken_api.get_open_positions,
    '9': kraken_api.get_ledgers_info,
    '10': lambda k, s: kraken_api.query_ledgers_info(input('Ledger ID: '), k, s),
    '11': kraken_api.get_trade_volume,
    '12': lambda k, s: kraken_api.request_export_report(input('Report type: '), k, s),
}

################## WITHDRAW ADRESSES #################
withdraw_adresses_menu_items = {
    1: 'add withdraw address',
    2: 'edit withdraw address',
    3: 'delete withdraw address',
    99: 'back'
}

##################### API List #######################
api_list_menu_items = {
    1: 'add APIKeys',
    2: 'edit APIKeys',
    3: 'delete APIKeys',
    # 4: 'Auswahl des zu nutzenden APIKeys',
    99: 'back'
}

api_list_headers = [
    'name',
    'api_key',
    'api_sec',
    'api_url',
    'in_use'
]

withdraw_adress_headers = [
    'name',
    'asset',
    'key'
]