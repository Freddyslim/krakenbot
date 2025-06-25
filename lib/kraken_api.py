import base64
import hashlib
import hmac
import json
import time
import urllib.parse
from typing import Dict, Tuple

import requests

API_URL = "https://api.kraken.com"


def load_credentials(filename: str = "config/api/kraken_key.json") -> Dict:
    """Load API credentials from a JSON file."""
    try:
        with open(filename, "r") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


def get_api_pair(data: Dict, api_name: str) -> Tuple[str, str]:
    """Return API key/secret pair for the given name."""
    try:
        api_key = data[api_name]["api_key"]
        api_sec = data[api_name]["api_sec"]
        return api_key, api_sec
    except KeyError as exc:
        raise ValueError(f"API credentials for '{api_name}' not found") from exc


def _sign(uri_path: str, data: Dict, secret: str) -> str:
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + postdata).encode()
    message = uri_path.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    return base64.b64encode(mac.digest()).decode()


def private_request(method: str, data: Dict, api_key: str, api_sec: str) -> Dict:
    """Perform a signed POST request to a private Kraken API method."""
    uri_path = f"/0/private/{method}"
    data["nonce"] = int(1000 * time.time())
    headers = {
        "API-Key": api_key,
        "API-Sign": _sign(uri_path, data, api_sec),
    }
    resp = requests.post(API_URL + uri_path, headers=headers, data=data)
    return resp.json()


def public_request(method: str, params: Dict | None = None) -> Dict:
    """Perform a GET request to a public Kraken API method."""
    params = params or {}
    resp = requests.get(API_URL + f"/0/public/{method}", params=params)
    return resp.json()


# Convenience wrappers -----------------------------------------------------

def get_acc_balance(api_key: str, api_sec: str) -> Dict:
    return private_request("Balance", {}, api_key, api_sec)


def get_trade_balance(api_key: str, api_sec: str) -> Dict:
    return private_request("TradeBalance", {}, api_key, api_sec)


def ticker(pair: str = "XBTUSD") -> Dict:
    return public_request("Ticker", {"pair": pair})


def ohlc(pair: str = "XBTUSD", interval: int = 1, since: int | None = None) -> Dict:
    """Return OHLC data for a pair."""
    params = {"pair": pair, "interval": interval}
    if since is not None:
        params["since"] = since
    return public_request("OHLC", params)


def get_open_orders(api_key: str, api_sec: str) -> Dict:
    return private_request("OpenOrders", {}, api_key, api_sec)


def get_closed_orders(api_key: str, api_sec: str) -> Dict:
    return private_request("ClosedOrders", {}, api_key, api_sec)


def query_orders_info(txid: str, api_key: str, api_sec: str) -> Dict:
    return private_request("QueryOrders", {"txid": txid}, api_key, api_sec)


def get_trades_history(api_key: str, api_sec: str) -> Dict:
    return private_request("TradesHistory", {}, api_key, api_sec)


def query_trades_info(txid: str, api_key: str, api_sec: str) -> Dict:
    return private_request("QueryTrades", {"txid": txid}, api_key, api_sec)


def get_open_positions(api_key: str, api_sec: str) -> Dict:
    return private_request("OpenPositions", {}, api_key, api_sec)


def get_ledgers_info(api_key: str, api_sec: str) -> Dict:
    return private_request("Ledgers", {}, api_key, api_sec)


def query_ledgers_info(id_: str, api_key: str, api_sec: str) -> Dict:
    return private_request("QueryLedgers", {"id": id_}, api_key, api_sec)


def get_trade_volume(api_key: str, api_sec: str) -> Dict:
    return private_request("TradeVolume", {}, api_key, api_sec)


def request_export_report(report: str, api_key: str, api_sec: str) -> Dict:
    return private_request("AddExport", {"report": report}, api_key, api_sec)
