import glob
import os
import threading
from .limit_cycle_bot import LimitCycleBot, CycleSettings


def run_cycle_tests(max_iterations: int | None = 10, *, log_dir: str = os.path.join("log", "test")) -> None:
    """Run LimitCycleBot with all test settings in parallel."""
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
        t = threading.Thread(
            target=bot.run,
            kwargs={"max_iterations": max_iterations, "log_dir": log_dir},
            daemon=True,
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
