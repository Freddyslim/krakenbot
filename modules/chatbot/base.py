"""Base classes and helpers for strategy chatbots."""

from typing import Tuple

import yfinance as yf

from lib import kraken_api


class BaseChatBot:
    """Base chatbot providing data fetching helpers."""

    def fetch_kraken_ticker(self, pair: str = "XBTUSD") -> dict:
        """Return ticker info for a currency pair using Kraken public API."""
        return kraken_api.ticker(pair)

    def fetch_yahoo_price(self, symbol: str) -> float | None:
        """Return the latest price for a symbol from Yahoo Finance."""
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            return None
        return float(data["Close"].iloc[-1])


class TickerBot(BaseChatBot):
    """Simple bot that prints prices from Kraken and Yahoo Finance."""

    def __init__(self, pair: str = "XBTUSD", symbol: str = "AAPL", delay: int = 5):
        self.pair = pair
        self.symbol = symbol
        self.delay = delay

    def run(self) -> None:
        import time

        print(
            f"Starting TickerBot for Kraken pair {self.pair} and Yahoo symbol {self.symbol}"
        )
        for _ in range(3):
            kdata = self.fetch_kraken_ticker(self.pair)
            last = None
            if kdata.get("result"):
                info = next(iter(kdata["result"].values()))
                last = info.get("c", [None])[0]
            yprice = self.fetch_yahoo_price(self.symbol)
            print(f"Kraken last: {last}  Yahoo price: {yprice}")
            time.sleep(self.delay)

