import json
import os
import random

PAIRS = [
    "XBTEUR",  # Bitcoin
    "SOLEUR",  # Solana
    "LINKEUR",  # Chainlink
    "ETHEUR",  # Ethereum
    "XRPEUR",  # Ripple
    "ADAEUR",  # Cardano
]

SYMBOL_MAP = {
    "XBTEUR": "BTC-EUR",
    "SOLEUR": "SOL-EUR",
    "LINKEUR": "LINK-EUR",
    "ETHEUR": "ETH-EUR",
    "XRPEUR": "XRP-EUR",
    "ADAEUR": "ADA-EUR",
}

BASE_SETTINGS = {
    "symbol": "BTC-EUR",
    "pair": "XBTEUR",
    "use_kraken_price": False,
    "refresh_rate": 2,
    "startbuy_threshold": 0.4,
    "initial_portfolio_eur": 1000,
    "reinvestment_percent": 15,
    "take_profit_percent": 0.8,
    "buyback_percent": 0.5,
    "safety_offset": 0.15,
    "enable_stop_loss": False,
    "stop_loss_percent": 2.0,
    "debug": False,
    "log_interval_terminal": 1,
    "log_interval_file": 1,
    "auto_log": True,
}

def random_setting(pair: str) -> dict:
    s = BASE_SETTINGS.copy()
    s["pair"] = pair
    s["symbol"] = SYMBOL_MAP.get(pair, "BTC-EUR")
    s["refresh_rate"] = random.randint(1, 5)
    s["startbuy_threshold"] = round(random.uniform(0.2, 1.0), 2)
    s["initial_portfolio_eur"] = random.choice([500, 1000, 1500, 2000])
    # use more aggressive reinvestment
    s["reinvestment_percent"] = random.randint(25, 40)
    s["take_profit_percent"] = round(random.uniform(0.5, 2.0), 2)
    s["buyback_percent"] = round(random.uniform(0.3, 1.0), 2)
    # lower safety offset for more aggressive behaviour
    s["safety_offset"] = round(random.uniform(0.05, 0.25), 2)
    s["enable_stop_loss"] = random.choice([True, False])
    s["stop_loss_percent"] = round(random.uniform(1.5, 5.0), 2)
    # always keep auto_log enabled for test runs
    s["auto_log"] = True
    return s

def main(count_per_pair: int = 20) -> None:
    """Generate settings for each pair in :data:`PAIRS`."""
    out_dir = os.path.join("config", "chatbot", "tests")
    os.makedirs(out_dir, exist_ok=True)
    total = 0
    for pair in PAIRS:
        for i in range(count_per_pair):
            cfg = random_setting(pair)
            path = os.path.join(out_dir, f"cycle_settings_{total:04d}.json")
            with open(path, "w") as fh:
                json.dump(cfg, fh, indent=2)
            total += 1
    print(f"Generated {total} test configs in {out_dir}")

if __name__ == "__main__":
    main()
