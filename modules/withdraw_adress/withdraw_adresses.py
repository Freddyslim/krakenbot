import os
import sys

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, lib_path)

import lib.lib as lib
import config.menu.menu_settings as menu_settings


def run() -> None:
    path_to_folder = input("Folder: (default: config/api/) ") or "config/api/"
    filename = input(f"Filename: (default: {path_to_folder}withdraw_db.json) ") or (
        path_to_folder + "withdraw_db.json")
    print(path_to_folder + "\n" + filename)
    print('Select file to edit (default: config/api/withdraw.db.json)')
    data, filename = lib.load_json_file(filename, path_to_folder)

    while True:
        print('WITHDRAW ADRESSEN')
        lib.create_withdraw_table(data)
        option = lib.create_menu_with_options(menu_settings.withdraw_adresses_menu_items.items())

        if option == 1:
            new_id = str(len(data) + 1)
            lib.add_withdraw_adress(data, new_id, menu_settings.withdraw_adress_headers)
            lib.write_json(data, filename)
        elif option == 2:
            id_ = input('ID des APIKeys: ')
            lib.change_withdraw_adress(data, id_, menu_settings.withdraw_adress_headers)
            lib.write_json(data, filename)
        elif option == 3:
            id_to_delete = input('ID des zu löschenden API-Keys: ')
            lib.delete_withdraw_adress(data, id_to_delete)
            lib.write_json(data, filename)
        elif option == 99:
            break
        else:
            print('\nno valid ID')


if __name__ == "__main__":
    run()
