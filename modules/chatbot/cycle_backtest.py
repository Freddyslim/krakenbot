import json
import os
import itertools
from typing import Iterable, List, Dict, Any

import pandas as pd
import requests

from lib import kraken_api

from .limit_cycle_bot import LimitCycleBot, CycleSettings


def _parse_duration(text: str) -> float | None:
    """Return duration in seconds for a string like '10m' or '2h'."""
    if not text:
        return None
    text = text.strip().lower()
    if text in {"inf", "infinite", "infinity"}:
        return None
    value = ""
    unit = ""
    for c in text:
        if c.isdigit():
            value += c
        else:
            unit += c
    if not value or not unit:
        return None
    value = int(value)
    if unit in {"s", "sec", "secs", "second", "seconds"}:
        mul = 1
    elif unit in {"m", "min", "mins", "minute", "minutes"}:
        mul = 60
    elif unit in {"h", "hr", "hrs", "hour", "hours"}:
        mul = 60 * 60
    elif unit in {"d", "day", "days"}:
        mul = 60 * 60 * 24
    elif unit in {"w", "week", "weeks"}:
        mul = 60 * 60 * 24 * 7
    elif unit in {"mo", "mon", "month", "months"}:
        mul = 60 * 60 * 24 * 30
    elif unit in {"y", "yr", "year", "years"}:
        mul = 60 * 60 * 24 * 365
    else:
        return None
    return value * mul


def _expand(value: Any) -> List[Any]:
    """Expand scalar or range object to a list of values."""
    if isinstance(value, dict):
        start = float(value.get("start", 0))
        end = float(value.get("end", start))
        step = float(value.get("step", 1))
        result: List[Any] = []
        x = start
        while x <= end + 1e-9:
            result.append(round(x, 10))
            x += step
        return result
    if isinstance(value, list):
        return value
    return [value]


class BacktestLimitCycleBot(LimitCycleBot):
    """LimitCycleBot using predefined price data instead of live quotes."""

    def __init__(self, settings: CycleSettings, prices: Iterable[float]):
        super().__init__(settings)
        self._prices = list(prices)
        self._index = 0

    def _get_price(self) -> float | None:  # type: ignore[override]
        if self._index >= len(self._prices):
            return None
        price = float(self._prices[self._index])
        self._index += 1
        return price


def _load_prices(pair: str, interval: int, duration: float | None) -> List[float]:
    """Return close prices fetched from Kraken's OHLC endpoint."""
    since = None
    if duration is not None:
        since = int((pd.Timestamp.utcnow() - pd.Timedelta(seconds=duration)).timestamp())
    try:
        resp = kraken_api.ohlc(pair, interval=interval, since=since)
    except requests.RequestException:
        return []
    data = resp.get("result", {}).get(pair)
    if not data:
        return []
    df = pd.DataFrame(
        data,
        columns=["time", "open", "high", "low", "close", "vwap", "volume", "count"],
    )
    return df["close"].astype(float).tolist()


def run_backtest(settings_file: str = "config/chatbot/cycle_backtest_settings.json") -> None:
    with open(settings_file, "r") as fh:
        cfg = json.load(fh)

    duration = _parse_duration(str(cfg.get("duration", "")))
    pair = cfg.get("pair", "XBTEUR")
    interval = int(cfg.get("interval", 60))
    prices = _load_prices(pair, interval, duration)
    if not prices:
        print("No price data loaded")
        return

    vary_keys = [
        "take_profit_percent",
        "buyback_percent",
        "safety_offset",
        "enable_stop_loss",
        "stop_loss_percent",
    ]
    base = {k: v for k, v in cfg.items() if k not in vary_keys}
    ranges: Dict[str, List[Any]] = {k: _expand(cfg.get(k)) for k in vary_keys}

    combos = list(itertools.product(*ranges.values()))
    os.makedirs(os.path.join("log", "test"), exist_ok=True)
    results = []
    for idx, combo in enumerate(combos, 1):
        params = dict(zip(vary_keys, combo))
        current = base | params
        settings = CycleSettings(**{k: v for k, v in current.items() if k in CycleSettings.__annotations__})
        bot = BacktestLimitCycleBot(settings, prices)
        log_name = f"cycle_backtest_{idx:04d}.log"
        bot.run(max_iterations=len(prices), log_dir=os.path.join("log", "test"), log_name=log_name)
        results.append((bot.total_profit, params, log_name))
        print(f"Finished test {idx}/{len(combos)} -> Profit {bot.total_profit:.2f} €")

    results.sort(key=lambda x: x[0], reverse=True)
    summary_path = os.path.join("log", "test", "summary.log")
    with open(summary_path, "w") as fh:
        for profit, params, log_name in results:
            fh.write(f"{log_name}: {profit:.2f} €\n")
            fh.write(json.dumps(params) + "\n")
        fh.write("\nTop 5 results:\n")
        for profit, params, log_name in results[:5]:
            fh.write(f"{log_name}: {profit:.2f} €\n")
            fh.write(json.dumps(params) + "\n")
    print(f"Results written to {summary_path}")


if __name__ == "__main__":
    run_backtest()
