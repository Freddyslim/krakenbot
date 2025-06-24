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
