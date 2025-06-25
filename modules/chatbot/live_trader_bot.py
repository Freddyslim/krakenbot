"""Live trading simulation bot that runs continuously."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict
from typing import Dict, Optional

import pandas as pd
from lib import kraken_api


@dataclass
class LiveSettings:
    """Configuration for :class:`LiveTraderBot`."""

    pair: str = "XBTEUR"  # trading pair
    lookback_days: int = 30  # days of data to analyse
    interval: int = 60  # data granularity in minutes
    trade_amount: float = 1000.0  # amount used per trade
    profit_target_pct: float = 1.5  # desired profit percentage
    check_interval: int = 30  # seconds between price checks
    slope_window_minutes: int = 10  # trend calculation window
    debug: bool = True  # verbose output
    telegram_enabled: bool = False  # send updates via telegram
    telegram_settings_file: str = "config/telegram/bot_settings.json"  # telegram config

    @staticmethod
    def load(filename: str) -> "LiveSettings":
        with open(filename, "r") as fh:
            text = fh.read()
        lines: list[str] = []
        for line in text.splitlines():
            line = line.split("//", 1)[0]
            line = line.split("#", 1)[0]
            lines.append(line)
        data = json.loads("\n".join(lines))
        valid = {k: v for k, v in data.items() if k in LiveSettings.__annotations__}
        return LiveSettings(**valid)


class LiveTraderBot:
    """Very simple strategy that buys once an upward trend is detected."""

    def __init__(self, settings: LiveSettings) -> None:
        self.settings = settings
        self.position = 0.0
        self.cash = settings.trade_amount
        self.initial_balance = settings.trade_amount
        self.last_buy_price: float | None = None
        self.target_sell_price: float | None = None
        self.trade_history: list[dict] = []
        self.state_file = "output/live_trader_state.json"
        self.telegram_token: str | None = None
        self.telegram_chat_id: str | None = None
        self.log_dir = "log"
        os.makedirs(self.log_dir, exist_ok=True)
        timestamp = pd.Timestamp.utcnow().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"{timestamp}.log")
        try:
            with open(self.log_file, "w") as fh:
                json.dump({"settings": asdict(self.settings)}, fh, indent=2)
                fh.write("\n")
        except OSError:
            pass
        self._load_state()
        if self.settings.telegram_enabled:
            try:
                with open(self.settings.telegram_settings_file, "r") as fh:
                    data = json.load(fh)
                self.telegram_token = data.get("bot_token")
                self.telegram_chat_id = data.get("chat_id")
            except FileNotFoundError:
                print("Telegram settings file not found")
                self.settings.telegram_enabled = False

    def _fetch_data(self) -> pd.DataFrame:
        since = int((pd.Timestamp.utcnow() - pd.Timedelta(days=self.settings.lookback_days)).timestamp())
        resp = kraken_api.ohlc(self.settings.pair, interval=self.settings.interval, since=since)
        data = resp.get("result", {}).get(self.settings.pair)
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "vwap", "volume", "count"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df.set_index("time")

    def _write_state(self, info: Dict) -> None:
        try:
            with open(self.state_file, "w") as fh:
                json.dump(info, fh, indent=2)
        except OSError:
            pass

    def _load_state(self) -> None:
        """Load previous session state if settings match."""
        try:
            with open(self.state_file, "r") as fh:
                data = json.load(fh)
        except FileNotFoundError:
            return
        if data.get("settings") != asdict(self.settings):
            return
        self.position = data.get("position", self.position)
        self.cash = data.get("cash", self.cash)
        self.initial_balance = data.get("initial_balance", self.initial_balance)
        self.last_buy_price = data.get("last_buy_price")
        self.target_sell_price = data.get("target_sell_price")
        self.trade_history = data.get("trade_history", [])

    def _format_numbers(self, info: Dict) -> Dict:
        """Round numeric values for nicer log output."""
        formatted: Dict = {}
        for key, value in info.items():
            if isinstance(value, float):
                if key == "position":
                    formatted[key] = round(value, 6)
                else:
                    formatted[key] = round(value, 2)
            else:
                formatted[key] = value
        return formatted

    def _log(self, info: Dict) -> None:
        formatted = self._format_numbers(info)
        if self.settings.debug:
            print(json.dumps(formatted, indent=2, ensure_ascii=False))
        try:
            with open(self.log_file, "a") as fh:
                fh.write(json.dumps(formatted, indent=2, ensure_ascii=False))
                fh.write("\n")
        except OSError:
            pass

    def _notify(self, info: Dict) -> None:
        if not self.settings.telegram_enabled:
            return
        if not (self.telegram_token and self.telegram_chat_id):
            return
        import requests

        text_lines = [
            f"{info.get('timestamp')}",
            f"Aktion: {info.get('action') or 'keine'}",
            f"Preis: {info.get('price'):.2f}",
            f"Kurzfristiger MA: {info.get('short_ma'):.2f}",
            f"Langfristiger MA: {info.get('long_ma'):.2f}",
            f"Position: {info.get('position'):.6f}",
            f"Bargeld: {info.get('cash'):.2f}",
            f"Verkaufsziel: {info.get('target_sell_price')}",
            f"N\u00e4chster Kauf bei: {info.get('next_buy_price')}",
            f"Profit: {info.get('profit'):.2f}",
        ]
        if info.get("expected_next_order_time"):
            text_lines.append(
                f"Nächste Order ({info.get('expected_action')}) voraussichtlich gegen {info['expected_next_order_time']}"
            )
        text = "\n".join(text_lines)
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.telegram_token}/sendMessage",
                data={"chat_id": self.telegram_chat_id, "text": text},
                timeout=10,
            )
        except requests.RequestException:
            pass
        self._log({"telegram_message": text})

    def _interval_seconds(self) -> int:
        return int(self.settings.interval * 60)

    def _compute_price_slope(self, prices: pd.Series) -> float:
        """Return price change per second over the configured slope window."""
        if len(prices) < 2:
            return 0.0
        delta_price = prices.iloc[-1] - prices.iloc[0]
        delta_time = (prices.index[-1] - prices.index[0]).total_seconds()
        if delta_time == 0:
            return 0.0
        return float(delta_price) / delta_time

    def _estimate_time_to_target_from_slope(
        self, price: float, slope: float, target: Optional[float]
    ) -> Optional[pd.Timestamp]:
        if target is None or slope == 0:
            return None
        if (slope > 0 and target <= price) or (slope < 0 and target >= price):
            return pd.Timestamp.utcnow()
        seconds_needed = (target - price) / slope
        if seconds_needed <= 0:
            return None
        return pd.Timestamp.utcnow() + pd.Timedelta(seconds=seconds_needed)

    def run(self) -> None:
        print(
            f"Starting LiveTraderBot for {self.settings.pair} with trade amount {self.settings.trade_amount}"
        )
        while True:
            df = self._fetch_data()
            price = float(df["close"].iloc[-1])
            prev_price = float(df["close"].iloc[-2]) if len(df) > 1 else price
            short_ma = float(df["close"].rolling(window=7).mean().iloc[-1])
            long_ma = float(df["close"].rolling(window=25).mean().iloc[-1])

            window_points = max(
                2,
                int(
                    self.settings.slope_window_minutes * 60 / self._interval_seconds()
                )
                + 1,
            )
            recent_prices = df["close"].tail(window_points)
            price_slope = self._compute_price_slope(recent_prices)

            action = None
            timestamp = pd.Timestamp.utcnow().isoformat()
            if self.position == 0 and short_ma > long_ma and price <= short_ma:
                qty = self.cash / price
                self.position = qty
                self.cash = 0.0
                self.last_buy_price = price
                self.target_sell_price = price * (1 + self.settings.profit_target_pct / 100)
                action = f"BUY {self.position:.6f} at {price:.2f}"
                self.trade_history.append({"action": "BUY", "price": price, "qty": qty, "timestamp": timestamp})
            elif self.position > 0 and price >= (self.target_sell_price or 0):
                qty = self.position
                self.cash = self.position * price
                self.position = 0.0
                profit_trade = (price - (self.last_buy_price or price)) * qty
                action = f"SELL at {price:.2f}"
                self.trade_history.append({"action": "SELL", "price": price, "qty": qty, "timestamp": timestamp, "profit": profit_trade})
                sells = [t for t in self.trade_history if t.get("action") == "SELL"]
                if sells:
                    avg_profit = sum(t.get("profit", 0) for t in sells) / len(sells)
                    self.settings.profit_target_pct = max(0.5, min(5.0, self.settings.profit_target_pct + avg_profit / 100))
                self.target_sell_price = None

            next_target = (
                short_ma if self.position == 0 else self.target_sell_price
            )
            eta_ts = self._estimate_time_to_target_from_slope(
                price, price_slope, next_target
            )
            current_value = self.cash + self.position * price
            profit = current_value - self.initial_balance
            info = {
                "timestamp": timestamp,
                "price": price,
                "short_ma": short_ma,
                "long_ma": long_ma,
                "position": self.position,
                "cash": self.cash,
                "last_buy_price": self.last_buy_price,
                "target_sell_price": self.target_sell_price,
                "next_buy_price": short_ma if self.position == 0 else None,
                "expected_next_order_time": eta_ts.isoformat() if eta_ts else None,
                "expected_action": "BUY" if self.position == 0 else "SELL",
                "price_slope": price_slope,
                "action": action,
                "profit": profit,
            }

            state = {
                "settings": asdict(self.settings),
                "position": self.position,
                "cash": self.cash,
                "last_buy_price": self.last_buy_price,
                "target_sell_price": self.target_sell_price,
                "trade_history": self.trade_history,
                "initial_balance": self.initial_balance,
                "timestamp": timestamp,
            }

            self._write_state(state)
            self._log(info)
            self._notify(info)
            time.sleep(self.settings.check_interval)


if __name__ == "__main__":
    settings = LiveSettings.load("config/chatbot/live_trader_settings.json")
    bot = LiveTraderBot(settings)
    bot.run()
