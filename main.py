import config.menu.menu_settings as menu_settings
import lib.lib as lib

from modules.api_editor import api_list
from modules.withdraw_adress import withdraw_adresses
from modules.kraken_request import kraken_request

api_name = "AllPerm"


def main() -> None:
    while True:
        print("\nKRAKEN REMOTE \n")
        option = lib.create_menu_with_options(menu_settings.main_menu_items.items())

        if option == 1:
            api_list.run()
        elif option == 2:
            withdraw_adresses.run()
        elif option == 3:
            kraken_request.run(api_name)
        elif option == 99:
            print()
            break
        else:
            print("Ungültige Eingabe")


if __name__ == "__main__":
    main()
