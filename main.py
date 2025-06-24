import config.menu.menu_settings as menu_settings
import lib.lib as lib

# api_url = "https://api.kraken.com"
api_name = "AllPerm"
# data, filename = lib.load_json_file()
# main()

while True:
    # Anzeigen der Optionen
    print ('\nKRAKEN REMOTE \n')
    option = lib.create_menu_with_options(menu_settings.main_menu_items.items())

    if option == 1:
        with open("modules/api_editor/api_list.py", mode="r", encoding="utf-8") as adresses:
            code = adresses.read()
        exec(code, globals())
    elif option == 2:
        with open("modules/withdraw_adress/withdraw_adresses.py", mode="r", encoding="utf-8") as adresses:
            code = adresses.read()
        exec(code, globals())
    elif option == 3:
        with open("modules/kraken_request/kraken_request.py", mode="r", encoding="utf-8") as request:
            code = request.read()
        exec(code, globals())
    elif option == 99:
        print('\n')
        break


def my_function(param1, param2):
    """_summary_

    Args:
        param1 (_type_): _description_
        param2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Implementation of my_function.
    return param1 + param2