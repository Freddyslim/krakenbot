import os
import sys

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, lib_path)

import lib.lib as lib
import config.menu.menu_settings as menu_settings


def run() -> None:
    path_to_folder = input("Folder: (default: config/api/) ") or "config/api/"
    filename = input(f"Filename: (default: {path_to_folder}kraken_key.json) ") or (
        path_to_folder + "kraken_key.json")
    print(path_to_folder + "\n" + filename)
    data, filename = lib.load_json_file(filename, path_to_folder)

    while True:
        lib.create_api_table(data)
        print("API CONFIGURATION")
        option = lib.create_menu_with_options(menu_settings.api_list_menu_items.items())

        if option == 1:
            new_id = str(len(data) + 1)
            data = lib.add_api_keys(data, new_id, menu_settings.api_list_headers)
            lib.write_json(data, filename)
        elif option == 2:
            id_to_edit = input("Which ID should be edited? ")
            if id_to_edit in data:
                lib.change_api_list(data, id_to_edit, menu_settings.api_list_headers)
                lib.write_json(data, filename)
            else:
                print("no valid id")
        elif option == 3:
            id_to_delete = input("Which ID should be deleted? ")
            data = lib.delete_api_keys(data, id_to_delete)
            lib.write_json(data, filename)
        elif option == 99:
            break
        else:
            print("\nno valid ID")


if __name__ == "__main__":
    run()
