import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any, Dict, Optional
import functools

import requests

import lib.lib as lib

API_URL = "https://api.kraken.com"

# Known public and private method names as defined by Kraken's REST API.
PUBLIC_METHODS = {
    "Time",
    "SystemStatus",
    "Assets",
    "AssetPairs",
    "Ticker",
    "OHLC",
    "Depth",
    "Trades",
    "Spread",
}

PRIVATE_METHODS = {
    "Balance",
    "TradeBalance",
    "OpenOrders",
    "ClosedOrders",
    "QueryOrders",
    "TradesHistory",
    "QueryTrades",
    "OpenPositions",
    "Ledgers",
    "QueryLedgers",
    "TradeVolume",
    "AddOrder",
    "CancelOrder",
    "AddExport",
    "GetExportReportStatus",
    "RetrieveExport",
    "RemoveExport",
    "Withdraw",
}


def get_api_pair(data: Dict[str, Dict[str, str]], api_name: str):
    """Return API key and secret for the given API profile."""
    for key in data:
        if data[key].get("name") == api_name:
            return data[key].get("api_key"), data[key].get("api_sec")
    return None, None


class KrakenAPI:
    """Minimal Kraken REST API client."""

    def __init__(self, api_key: Optional[str] = None, api_sec: Optional[str] = None, api_url: str = API_URL):
        self.api_key = api_key
        self.api_sec = api_sec
        self.api_url = api_url.rstrip("/")
        self.session = requests.Session()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _sign(self, urlpath: str, data: Dict[str, Any]) -> str:
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data["nonce"]) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(self.api_sec), message, hashlib.sha512)
        return base64.b64encode(mac.digest()).decode()

    def _request(self, method: str, urlpath: str, data: Optional[Dict[str, Any]] = None, *, private: bool = False):
        if data is None:
            data = {}
        if private:
            if not self.api_key or not self.api_sec:
                raise ValueError("API key and secret required for private endpoints")
            data["nonce"] = int(time.time() * 1000)
            headers = {
                "API-Key": self.api_key,
                "API-Sign": self._sign(urlpath, data),
            }
            resp = self.session.post(self.api_url + urlpath, headers=headers, data=data)
        else:
            resp = self.session.get(self.api_url + urlpath, params=data)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Public and private query helpers
    # ------------------------------------------------------------------
    def public(self, method: str, params: Optional[Dict[str, Any]] = None):
        return self._request("GET", f"/0/public/{method}", params, private=False)

    def private(self, method: str, params: Optional[Dict[str, Any]] = None):
        return self._request("POST", f"/0/private/{method}", params, private=True)

    # ------------------------------------------------------------------
    # Dynamic endpoint access
    # ------------------------------------------------------------------
    def __getattr__(self, name: str):
        if name in PUBLIC_METHODS:
            return functools.partial(self.public, name)
        if name in PRIVATE_METHODS:
            return functools.partial(self.private, name)
        raise AttributeError(name)


# ----------------------------------------------------------------------
# Convenience wrapper functions used by the CLI modules
# ----------------------------------------------------------------------

def ticker(pair: str = "XMREUR"):
    api = KrakenAPI()
    return api.Ticker({"pair": pair})


def get_acc_balance(api_key: str, api_sec: str):
    api = KrakenAPI(api_key, api_sec)
    result = api.Balance()
    lib.create_balance_table(result.get("result", {}))
    return result


def get_trade_balance(api_key: str, api_sec: str):
    api = KrakenAPI(api_key, api_sec)
    asset = input("Enter Währung: ")
    result = api.TradeBalance({"asset": asset})
    lib.create_balance_table(result.get("result", {}))
    return result
