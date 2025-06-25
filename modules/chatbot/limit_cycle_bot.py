"""Simple limit order cycle bot for live price simulation."""

from __future__ import annotations

import json
import time
import os
from dataclasses import dataclass, asdict
from typing import Optional
import re

from .base import BaseChatBot
import lib.lib as lib


@dataclass
class CycleSettings:
    symbol: str = "BTC-USD"  # Yahoo Finance symbol
    refresh_rate: int = 2  # seconds between price checks
    startbuy_threshold: float = 0.4  # % difference between initial buy orders
    initial_portfolio_eur: float = 1000.0  # starting capital
    reinvestment_percent: float = 15.0  # % of balance used after each cycle
    take_profit_percent: float = 0.8  # target profit before selling
    buyback_percent: float = 0.5  # drop from sell price before rebuy
    safety_offset: float = 0.15  # margin on limit orders
    enable_stop_loss: bool = False  # activate stop-loss handling
    stop_loss_percent: float = 2.0  # loss threshold relative to buy price
    debug: bool = True  # print debug information
    log_interval_terminal: int = 1  # number of refresh cycles between terminal log output
    log_interval_file: int = 1  # number of refresh cycles between file log output

    @staticmethod
    def load(filename: str) -> "CycleSettings":
        with open(filename, "r") as fh:
            text = fh.read()
        lines = []
        for line in text.splitlines():
            line = line.split("//", 1)[0]
            line = line.split("#", 1)[0]
            lines.append(line)
        data = json.loads("\n".join(lines))
        valid = {k: v for k, v in data.items() if k in CycleSettings.__annotations__}
        return CycleSettings(**valid)


@dataclass
class LimitOrder:
    side: str  # "buy" or "sell"
    price: float
    amount: float


class LimitCycleBot(BaseChatBot):
    """Trading bot that simulates recurring limit orders."""

    def __init__(self, settings: CycleSettings) -> None:
        self.settings = settings
        self.eur_balance = settings.initial_portfolio_eur
        self.asset_balance = 0.0
        self.last_profit: Optional[dict] = None
        self.current_buy_amount = settings.initial_portfolio_eur
        self.last_buy_price: Optional[float] = None
        self.open_buy_low: Optional[LimitOrder] = None
        self.open_buy_high: Optional[LimitOrder] = None
        self.open_sell: Optional[LimitOrder] = None
        self.open_stop_loss: Optional[LimitOrder] = None
        self.high_since_buy: Optional[float] = None
        self.low_since_sell: Optional[float] = None
        self.start_time = time.time()
        self.log_counter = 0
        self.log_file_path = ""

    # --- Helpers ---------------------------------------------------------
    def _waiting_for(self) -> str:
        if self.open_stop_loss:
            return f"stop loss <= {self.open_stop_loss.price:.4f} €"
        if self.open_sell:
            return f"sell >= {self.open_sell.price:.4f} €"
        if self.open_buy_low and self.open_buy_high:
            return (
                f"buy <= {self.open_buy_low.price:.4f} € or >= {self.open_buy_high.price:.4f} €"
            )
        if self.open_buy_low:
            return f"buy <= {self.open_buy_low.price:.4f} €"
        if self.open_buy_high:
            return f"buy >= {self.open_buy_high.price:.4f} €"
        return "new cycle"

    def _log(self, price: float, *, to_terminal: bool = True, to_file: bool = False) -> None:
        """Output portfolio status to terminal and/or file."""
        current_value = self.eur_balance + self.asset_balance * price
        elapsed = int(time.time() - self.start_time)
        lines = [
            f"[LOG {elapsed}s] Portfolio Status:",
            f"Asset:               {self.settings.symbol}",
            f"Aktueller Kurs:      {price:.4f} €",
            f"Startkapital:        {self.settings.initial_portfolio_eur:.2f} €",
            f"Aktueller Wert:      {current_value:.2f} €",
            f"Eingesetzt:          {self.current_buy_amount:.2f} €",
            f"Freies Kapital:      {self.eur_balance:.2f} €",
        ]
        if self.asset_balance > 0:
            asset = self.settings.symbol.split("-")[0]
            lines.append(f"Bestand:            {self.asset_balance:.8f} {asset}")
        if self.last_buy_price:
            lines.append(f"Letzter Kaufkurs:    {self.last_buy_price:.4f} €")
        if self.open_sell or self.open_buy_low or self.open_stop_loss:
            lines.append("")
            lines.append("Offene Orders:")
            if self.open_sell:
                lines.append(
                    f"  – Sell @ {self.open_sell.price:.4f} € (Take Profit)"
                )
            if self.open_buy_low:
                lines.append(f"  – Buy @ {self.open_buy_low.price:.4f} € (Rebuy)")
            if self.open_stop_loss:
                lines.append(
                    f"  – Stop @ {self.open_stop_loss.price:.4f} € (Stop Loss)"
                )
        lines.append(f"Warte auf: {self._waiting_for()}")
        profit_lines = []
        if self.last_profit:
            lp = self.last_profit
            profit_lines = [
                "",
                "Letzter Profit:",
                f"  Gekauft: {lp['buy_eur']:.2f} € @ {lp['buy_price']:.4f} €",
                f"  Verkauft: {lp['sell_eur']:.2f} € @ {lp['sell_price']:.4f} €",
                f"  Gewinn: {lp['profit_eur']:+.2f} € ({lp['profit_pct']:+.2f} %)",
            ]

        if to_terminal and self.settings.debug:
            print("\n".join(lines))
            if profit_lines:
                print("\n".join(profit_lines))

        if to_file:
            with open(self.log_file_path, "a") as fh:
                fh.write("\n".join(lines) + "\n")
                if profit_lines:
                    fh.write("\n".join(profit_lines) + "\n")

    def _execute_sell(self, sell_price: float, amount: float, stop_loss: bool = False) -> None:
        eur_received = amount * sell_price
        self.eur_balance += eur_received
        self.asset_balance = 0.0
        buy_eur = self.current_buy_amount
        profit_eur = eur_received - buy_eur
        profit_pct = profit_eur / buy_eur * 100
        self.last_profit = {
            "buy_eur": buy_eur,
            "buy_price": self.last_buy_price,
            "sell_eur": eur_received,
            "sell_price": sell_price,
            "profit_eur": profit_eur,
            "profit_pct": profit_pct,
            "stop_loss": stop_loss,
        }
        msg = (
            f"STOP LOSS triggered at {sell_price:.4f} €"
            if stop_loss
            else f"SELL executed at {sell_price:.4f} € for {eur_received:.2f} €"
        )
        if self.settings.debug:
            lib.highlight_message(msg)
        self.open_sell = None
        self.open_stop_loss = None
        self.high_since_buy = None
        self.current_buy_amount = (
            (self.eur_balance) * self.settings.reinvestment_percent / 100
        )
        target_price = sell_price * (1 - self.settings.buyback_percent / 100)
        buy_price = target_price * (1 + self.settings.safety_offset / 100)
        amount = self.current_buy_amount / buy_price
        self.open_buy_low = LimitOrder("buy", buy_price, amount)
        if self.settings.debug:
            lib.highlight_message(
                f"Next buy order placed at {buy_price:.4f} € for {self.current_buy_amount:.2f} €"
            )

    def _place_start_orders(self, price: float) -> None:
        diff = self.settings.startbuy_threshold / 100
        high_price = price * (1 + diff)
        amount = self.current_buy_amount / price
        self.open_buy_low = None
        self.open_buy_high = LimitOrder("buy", high_price, amount)
        self.high_since_buy = None
        self.low_since_sell = None
        if self.settings.debug:
            lib.highlight_message(
                f"Initial buy order placed at {high_price:.4f} €"
            )

    def _update_sell_order(self, price: float) -> None:
        if not self.open_sell:
            return
        if self.high_since_buy is None or price > self.high_since_buy:
            self.high_since_buy = price
            new_price = self.high_since_buy * (1 - self.settings.safety_offset / 100)
            if new_price > self.open_sell.price:
                if self.settings.debug:
                    print(
                        f"Adjusting sell order from {self.open_sell.price:.4f} to {new_price:.4f} €"
                    )
                self.open_sell.price = new_price
        if price >= self.open_sell.price:
            self._execute_sell(self.open_sell.price, self.open_sell.amount)

    def _check_stop_loss(self, price: float) -> None:
        if not (self.settings.enable_stop_loss and self.open_stop_loss):
            return
        if price <= self.open_stop_loss.price:
            self._execute_sell(
                self.open_stop_loss.price, self.open_stop_loss.amount, stop_loss=True
            )

    def _update_buy_orders(self, price: float) -> None:
        if self.open_buy_low and price < self.open_buy_low.price:
            new_price = price * (1 + self.settings.safety_offset / 100)
            if new_price < self.open_buy_low.price:
                if self.settings.debug:
                    print(
                        f"Adjusting buy order from {self.open_buy_low.price:.4f} to {new_price:.4f} €"
                    )
                self.open_buy_low.price = new_price
        if self.open_buy_low and price <= self.open_buy_low.price:
            # execute buy
            buy_price = self.open_buy_low.price
            amount = self.open_buy_low.amount
            cost = buy_price * amount
            self.eur_balance -= cost
            self.asset_balance += amount
            self.last_buy_price = buy_price
            if self.settings.debug:
                lib.highlight_message(
                    f"BUY executed at {buy_price:.4f} € for {cost:.2f} €"
                )
            self.open_buy_low = None
            self.open_buy_high = None
            target_price = buy_price * (1 + self.settings.take_profit_percent / 100)
            sell_price = target_price * (1 - self.settings.safety_offset / 100)
            self.open_sell = LimitOrder("sell", sell_price, amount)
            if self.settings.enable_stop_loss:
                stop_price = buy_price * (1 - self.settings.stop_loss_percent / 100)
                self.open_stop_loss = LimitOrder("sell", stop_price, amount)
            if self.settings.debug:
                lib.highlight_message(
                    f"Sell order placed at {sell_price:.4f} € for target profit"
                )
        elif self.open_buy_high:
            if price < self.open_buy_high.price:
                new_price = price * (1 + self.settings.safety_offset / 100)
                if new_price < self.open_buy_high.price:
                    if self.settings.debug:
                        print(
                            f"Adjusting buy order from {self.open_buy_high.price:.4f} to {new_price:.4f} €"
                        )
                    self.open_buy_high.price = new_price
            if price >= self.open_buy_high.price:
                buy_price = self.open_buy_high.price
                amount = self.open_buy_high.amount
                cost = buy_price * amount
                self.eur_balance -= cost
                self.asset_balance += amount
                self.last_buy_price = buy_price
                if self.settings.debug:
                    lib.highlight_message(
                        f"BUY executed at {buy_price:.4f} € for {cost:.2f} €"
                    )
                self.open_buy_low = None
                self.open_buy_high = None
                target_price = buy_price * (1 + self.settings.take_profit_percent / 100)
                sell_price = target_price * (1 - self.settings.safety_offset / 100)
                self.open_sell = LimitOrder("sell", sell_price, amount)
                if self.settings.enable_stop_loss:
                    stop_price = buy_price * (1 - self.settings.stop_loss_percent / 100)
                    self.open_stop_loss = LimitOrder("sell", stop_price, amount)
                if self.settings.debug:
                    lib.highlight_message(
                        f"Sell order placed at {sell_price:.4f} € for target profit"
                    )

    # --- Main loop -------------------------------------------------------
    def run(self) -> None:
        """Run the trading loop until interrupted."""
        os.makedirs("log", exist_ok=True)
        self.log_file_path = os.path.join(
            "log", f"limit_cycle_{int(self.start_time)}.log"
        )
        with open(self.log_file_path, "w") as fh:
            fh.write("Settings:\n")
            json.dump(asdict(self.settings), fh, indent=2)
            fh.write("\n\n")

        reason = "completed"
        try:
            price = self.fetch_yahoo_price(self.settings.symbol)
            if price is None:
                print("Failed to fetch initial price")
                reason = "failed to fetch initial price"
                return
            self._place_start_orders(price)
            while True:
                price = self.fetch_yahoo_price(self.settings.symbol)
                if price is None:
                    time.sleep(self.settings.refresh_rate)
                    continue
                self._update_buy_orders(price)
                self._check_stop_loss(price)
                self._update_sell_order(price)
                self.log_counter += 1
                if self.log_counter % self.settings.log_interval_terminal == 0:
                    self._log(price, to_terminal=True)
                if self.log_counter % self.settings.log_interval_file == 0:
                    self._log(price, to_terminal=False, to_file=True)
                time.sleep(self.settings.refresh_rate)
        except KeyboardInterrupt:
            reason = "aborted by user"
        except Exception as exc:
            reason = f"exception: {exc}"
            raise
        finally:
            with open(self.log_file_path, "a") as fh:
                fh.write(f"Beendet: {reason}\n")


if __name__ == "__main__":
    settings = CycleSettings.load("config/chatbot/limit_cycle_settings.json")
    bot = LimitCycleBot(settings)
    bot.run()
