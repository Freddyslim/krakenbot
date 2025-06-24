"""Live trading simulation bot that runs continuously."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Dict

import pandas as pd
import yfinance as yf


@dataclass
class LiveSettings:
    """Configuration for :class:`LiveTraderBot`."""

    symbol: str = "BTC-USD"
    lookback_days: int = 30
    interval: str = "1h"
    trade_amount: float = 1000.0
    profit_target_pct: float = 1.5
    check_interval: int = 30
    debug: bool = True

    @staticmethod
    def load(filename: str) -> "LiveSettings":
        with open(filename, "r") as fh:
            data = json.load(fh)
        return LiveSettings(**data)


class LiveTraderBot:
    """Very simple strategy that buys once an upward trend is detected."""

    def __init__(self, settings: LiveSettings) -> None:
        self.settings = settings
        self.position = 0.0
        self.cash = settings.trade_amount
        self.last_buy_price: float | None = None
        self.target_sell_price: float | None = None
        self.state_file = "output/live_trader_state.json"

    def _fetch_data(self) -> pd.DataFrame:
        ticker = yf.Ticker(self.settings.symbol)
        period = f"{self.settings.lookback_days}d"
        df = ticker.history(period=period, interval=self.settings.interval)
        return df.dropna()

    def _write_state(self, info: Dict) -> None:
        try:
            with open(self.state_file, "w") as fh:
                json.dump(info, fh, indent=2)
        except OSError:
            pass

    def _log(self, info: Dict) -> None:
        if self.settings.debug:
            print(json.dumps(info, indent=2))

    def run(self) -> None:
        print(
            f"Starting LiveTraderBot for {self.settings.symbol} with trade amount {self.settings.trade_amount}"
        )
        while True:
            df = self._fetch_data()
            price = float(df["Close"].iloc[-1])
            short_ma = float(df["Close"].rolling(window=7).mean().iloc[-1])
            long_ma = float(df["Close"].rolling(window=25).mean().iloc[-1])

            action = None
            if self.position == 0 and short_ma > long_ma and price <= short_ma:
                self.position = self.cash / price
                self.cash = 0.0
                self.last_buy_price = price
                self.target_sell_price = price * (1 + self.settings.profit_target_pct / 100)
                action = f"BUY {self.position:.6f} at {price:.2f}"
            elif self.position > 0 and price >= (self.target_sell_price or 0):
                self.cash = self.position * price
                self.position = 0.0
                action = f"SELL at {price:.2f}"
                self.target_sell_price = None

            info = {
                "timestamp": pd.Timestamp.utcnow().isoformat(),
                "price": price,
                "short_ma": short_ma,
                "long_ma": long_ma,
                "position": self.position,
                "cash": self.cash,
                "last_buy_price": self.last_buy_price,
                "target_sell_price": self.target_sell_price,
                "next_buy_price": short_ma if self.position == 0 else None,
                "action": action,
            }

            self._write_state(info)
            self._log(info)
            time.sleep(self.settings.check_interval)


if __name__ == "__main__":
    settings = LiveSettings.load("config/chatbot/live_trader_settings.json")
    bot = LiveTraderBot(settings)
    bot.run()
