import glob
import os
from .limit_cycle_bot import LimitCycleBot, CycleSettings


def run_cycle_tests(max_iterations: int = 10) -> None:
    """Run LimitCycleBot with all test settings sequentially."""
    settings_dir = os.path.join("config", "chatbot", "tests")
    files = sorted(glob.glob(os.path.join(settings_dir, "*.json")))
    if not files:
        print(f"No test configs found in {settings_dir}")
        return
    print(f"Running {len(files)} cycle bot tests...")
    for fname in files:
        print(f"\nRunning {os.path.basename(fname)}")
        settings = CycleSettings.load(fname)
        bot = LimitCycleBot(settings)
        bot.run(max_iterations=max_iterations)
