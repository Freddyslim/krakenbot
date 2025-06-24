##############################  Imports  ##################################
### stadard
import os
import sys
### self created
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, lib_path)
import lib.lib as lib
import config.menu.menu_settings as menu_settings
import lib.kraken_api as kraken_api
import json
##############################  Settings  #################################

# SETTINGS FOR TESTING WITHOUT MAIN VARIABLES #

# api settings #
# import json
# api_name = "AllPerm"

# file settings #
path_to_folder = "config/api/"
filename = (path_to_folder + 'kraken_key.json')
with open(filename) as json_data:
   data = json.load(json_data)


#############################  API SETTING  ################################
# setting up api secrets #
api_key, api_sec = kraken_api.get_api_pair(data, api_name)


#############################  MAIN LOOP  #################################
# code runs only if modul is called from main.py # 
if __name__ == '__main__':
    # import variables from main # 
    from __main__ import api_name
    while True:
        # Anzeigen der Optionen für Kraken Request Gruppen
        print ('KRAKEN REQUESTS: \n')
        option = lib.create_menu_with_options(menu_settings.kraken_request_menu_items.items())

        # Anzeigen der Optionen für User Data # 
        if option == 1:
            while True:
                # Anzeigen der verschiedenen Request Typen #                      
                    option = lib.create_menu_with_options(menu_settings.user_data_menu_items.items())
                    if option == 99:
                        break

                    try:
                        choice = str(option)
                        menu_settings.user_data_requests[choice](api_key, api_sec)
                    except (ValueError, KeyError):
                        print("Ungültige Eingabe, bitte wählen Sie eine Option aus der Liste aus.")

        elif option == 7:
            data = kraken_api.ticker()
            # print(data)
            lib.display_data(data)


        elif option == 99:
            break