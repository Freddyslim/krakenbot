import config.menu.menu_settings as menu_settings
import lib.lib as lib

from modules.api_editor import api_list
from modules.withdraw_adress import withdraw_adresses
from modules.kraken_request import kraken_request
from modules.telegram_bot import telegram_bot
from modules.chatbot import run as chatbot_run
import lib.kraken_api as kraken_api


def select_api() -> str | None:
    """Return the API ID chosen by the user or ``None`` if not available."""
    creds = kraken_api.load_credentials()
    if not creds:
        print("No API credentials found. Add one first.")
        return None
    print("AVAILABLE API KEYS:")
    for key, entry in creds.items():
        print(f"{key}: {entry.get('name', '')}")
    choice = input("Use which API ID? (default: 1): ") or "1"
    if choice not in creds:
        print("Invalid selection")
        return None
    return choice

def main() -> None:
    while True:
        print("\nKRAKEN REMOTE \n")
        option = lib.create_menu_with_options(menu_settings.main_menu_items.items())

        if option == 1:
            api_list.run()
        elif option == 2:
            withdraw_adresses.run()
        elif option == 3:
            api_id = select_api()
            if api_id:
                kraken_request.run(api_id)
        elif option == 4:
            telegram_bot.run()
        elif option == 5:
            chatbot_run()
        elif option == 99:
            print()
            break
        else:
            print("Ungültige Eingabe")


if __name__ == "__main__":
    main()
