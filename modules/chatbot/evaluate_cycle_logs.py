import glob
import json
import os
import re
from typing import List, Tuple

LOG_PATTERN = os.path.join("log", "limit_cycle_*.log")

RESULT_RE = re.compile(r"Gesamtgewinn: ([+-]?[0-9\.]+)")


def parse_log(path: str) -> Tuple[float, dict]:
    with open(path, "r") as fh:
        content = fh.read()
    match = RESULT_RE.search(content)
    profit = float(match.group(1)) if match else 0.0
    settings = {}
    if "Settings:" in content:
        try:
            settings_json = content.split("Settings:\n", 1)[1].split("\n\n", 1)[0]
            settings = json.loads(settings_json)
        except Exception:
            pass
    return profit, settings


def find_best(top_n: int = 5) -> None:
    results: List[Tuple[float, str, dict]] = []
    for path in glob.glob(LOG_PATTERN):
        profit, settings = parse_log(path)
        results.append((profit, path, settings))
    results.sort(key=lambda x: x[0], reverse=True)
    for profit, path, settings in results[:top_n]:
        print(f"{path}: {profit:.2f} €")
        print(json.dumps(settings, indent=2))
        print()


if __name__ == "__main__":
    find_best()
