"""Elliott Wave strategy bot generating trade recommendations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import json
import os

import pandas as pd
import yfinance as yf


@dataclass
class Trade:
    action: str  # "buy" or "sell"
    price: float
    time: pd.Timestamp


@dataclass
class Settings:
    symbol: str = "BTC-USD"
    period: str = "1y"
    interval: str = "1d"
    profit_pct: float = 2.0
    start_balance: float = 1000.0
    wave_threshold_pct: float = 2.5

    @staticmethod
    def load(filename: str) -> "Settings":
        with open(filename, "r") as fh:
            data = json.load(fh)
        return Settings(**data)


class ElliottWaveBot:
    """Simple Elliott Wave based strategy."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.data: pd.DataFrame | None = None
        self.trades: List[Trade] = []

    def fetch_data(self) -> pd.DataFrame:
        ticker = yf.Ticker(self.settings.symbol)
        df = ticker.history(period=self.settings.period, interval=self.settings.interval)
        df = df.dropna()
        self.data = df
        return df

    # Basic zigzag detection to approximate waves
    def _detect_waves(self) -> List[Tuple[pd.Timestamp, float]]:
        if self.data is None or self.data.empty:
            return []
        df = self.data
        threshold = self.settings.wave_threshold_pct / 100
        highs = df["High"]
        lows = df["Low"]
        points: List[Tuple[pd.Timestamp, float]] = []
        last_extreme = df.index[0]
        last_price = df["Close"].iloc[0]
        last_is_high = None
        for time, row in df.iterrows():
            price = row["Close"]
            change = (price - last_price) / last_price
            if last_is_high is None:
                if abs(change) >= threshold:
                    last_is_high = price > last_price
                    last_extreme = time
                    last_price = price
                    points.append((time, price))
            else:
                if last_is_high and price < last_price * (1 - threshold):
                    last_is_high = False
                    last_extreme = time
                    last_price = price
                    points.append((time, price))
                elif not last_is_high and price > last_price * (1 + threshold):
                    last_is_high = True
                    last_extreme = time
                    last_price = price
                    points.append((time, price))
        return points

    def _generate_signals(self) -> None:
        waves = self._detect_waves()
        if len(waves) < 2:
            return
        # Buy after trough, sell after next peak with profit_pct requirement
        for i in range(len(waves) - 1):
            t0, p0 = waves[i]
            t1, p1 = waves[i + 1]
            if p1 > p0 * (1 + self.settings.profit_pct / 100):
                self.trades.append(Trade("buy", p0, t0))
                self.trades.append(Trade("sell", p1, t1))

    def simulate(self) -> float:
        if self.data is None:
            self.fetch_data()
        self._generate_signals()
        balance = self.settings.start_balance
        position = 0.0
        for trade in self.trades:
            if trade.action == "buy" and balance > 0:
                position = balance / trade.price
                balance = 0.0
            elif trade.action == "sell" and position > 0:
                balance = position * trade.price
                position = 0.0
        # If we end with a position, liquidate at last close
        if position > 0 and self.data is not None:
            balance = position * float(self.data["Close"].iloc[-1])
        return balance

    def run(self) -> None:
        self.fetch_data()
        final_balance = self.simulate()
        print(f"ElliottWaveBot finished. Trades executed: {len(self.trades)}")
        print(f"Final balance starting from {self.settings.start_balance}: {final_balance:.2f}")
        for trade in self.trades:
            print(f"{trade.time.date()} - {trade.action.upper()} at {trade.price:.2f}")


if __name__ == "__main__":
    settings = Settings.load("config/chatbot/elliott_wave_settings.json")
    bot = ElliottWaveBot(settings)
    bot.run()
