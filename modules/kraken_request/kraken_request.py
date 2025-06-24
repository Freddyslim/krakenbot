import os
import sys
import json

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, lib_path)

import lib.lib as lib
import config.menu.menu_settings as menu_settings
import lib.kraken_api as kraken_api


def run(api_name: str) -> None:
    """Interactive menu for performing Kraken API requests."""
    filename = os.path.join("config", "api", "kraken_key.json")
    with open(filename, "r") as fh:
        data = json.load(fh)

    api_key, api_sec = kraken_api.get_api_pair(data, api_name)

    while True:
        print("KRAKEN REQUESTS:\n")
        option = lib.create_menu_with_options(menu_settings.kraken_request_menu_items.items())

        if option == 1:
            _run_user_data(api_key, api_sec)
        elif option == 7:
            pair = input("Ticker pair (default: XBTUSD): ") or "XBTUSD"
            data = kraken_api.ticker(pair)
            lib.display_data(data)
        elif option == 99:
            break
        else:
            print("Ungültige Eingabe")


def _run_user_data(api_key: str, api_sec: str) -> None:
    while True:
        option = lib.create_menu_with_options(menu_settings.user_data_menu_items.items())
        if option == 99:
            break
        func = menu_settings.user_data_requests.get(str(option))
        if not func:
            print("Ungültige Eingabe")
            continue
        try:
            data = func(api_key, api_sec)
            lib.display_data(data)
        except Exception as exc:
            print(f"Request failed: {exc}")


if __name__ == "__main__":
    from __main__ import api_name
    run(api_name)
