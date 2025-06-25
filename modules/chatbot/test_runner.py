import glob
import os
import threading
import json
import re
from .limit_cycle_bot import LimitCycleBot, CycleSettings


_DURATION_PATTERN = re.compile(r"^(\d+)\s*([a-zA-Z]+)$")


def _parse_duration(text: str) -> float | None:
    """Return duration in seconds for a string like '10m' or '2h'.

    Returns ``None`` for 'inf' or invalid input."""
    if not text:
        return None
    if text.lower() in {"inf", "infinite", "infinity"}:
        return None
    m = _DURATION_PATTERN.match(text.strip())
    if not m:
        return None
    value = int(m.group(1))
    unit = m.group(2).lower()
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


def run_cycle_tests(*, log_dir: str = os.path.join("log", "test")) -> None:
    """Run ``LimitCycleBot`` with all test settings in parallel.

    The runtime is configured via ``config/chatbot/test_runner_settings.json``.
    """
    settings_file = os.path.join(
        "config", "chatbot", "test_runner_settings.json"
    )
    run_seconds = None
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as fh:
                cfg = json.load(fh)
            run_seconds = _parse_duration(str(cfg.get("duration", "inf")))
        except Exception:
            print(f"Failed to load {settings_file}, using infinite duration")
            run_seconds = None

    settings_dir = os.path.join("config", "chatbot", "tests")
    files = sorted(glob.glob(os.path.join(settings_dir, "*.json")))
    if not files:
        print(f"No test configs found in {settings_dir}")
        return
    os.makedirs(log_dir, exist_ok=True)
    print(f"Running {len(files)} cycle bot tests in parallel...")
    threads = []
    for fname in files:
        print(f"\nStarting {os.path.basename(fname)}")
        settings = CycleSettings.load(fname)
        bot = LimitCycleBot(settings)
        base = os.path.splitext(os.path.basename(fname))[0]
        log_name = f"limit_cycle_{base}.log"
        t = threading.Thread(
            target=bot.run,
            kwargs={
                "run_seconds": run_seconds,
                "log_dir": log_dir,
                "log_name": log_name,
            },
            daemon=True,
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
