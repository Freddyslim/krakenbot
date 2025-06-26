"""Base classes and helpers for strategy chatbots."""

import time
from typing import Any, Dict

from requests import RequestException

from lib import kraken_api


class BaseChatBot:
    """Base chatbot providing data fetching helpers."""

    _last_call = 0.0
    _rate_limit = 1.0  # seconds between public requests

    def fetch_kraken_ticker(self, pair: str = "XBTUSD") -> Dict[str, Any]:
        """Return ticker info for a currency pair using Kraken public API."""
        wait = self._rate_limit - (time.time() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        try:
            data = kraken_api.ticker(pair)
        except RequestException:
            # Network access might be blocked in some environments
            data = {}
        finally:
            self._last_call = time.time()
        return data


class TickerBot(BaseChatBot):
    """Simple bot that prints prices from Kraken."""

    def __init__(self, pair: str = "XBTUSD", delay: int = 1):
        self.pair = pair
        self.delay = max(delay, self._rate_limit)

    def run(self) -> None:
        import time

        print(f"Starting TickerBot for Kraken pair {self.pair}")
        for _ in range(3):
            kdata = self.fetch_kraken_ticker(self.pair)
            last = None
            if kdata.get("result"):
                info = next(iter(kdata["result"].values()))
                last = info.get("c", [None])[0]
            print(f"Kraken last: {last}")
            time.sleep(self.delay)

