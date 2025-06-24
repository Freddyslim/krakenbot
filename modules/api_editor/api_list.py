#################################
# ╭━━━┳━━━┳━━╮╭╮╱╱╭━━┳━━━┳━━━━╮ #
# ┃╭━╮┃╭━╮┣┫┣╯┃┃╱╱╰┫┣┫╭━╮┃╭╮╭╮┃ #
# ┃┃╱┃┃╰━╯┃┃┃╱┃┃╱╱╱┃┃┃╰━━╋╯┃┃╰╯ #
# ┃╰━╯┃╭━━╯┃┃╱┃┃╱╭╮┃┃╰━━╮┃╱┃┃   #
# ┃╭━╮┃┃╱╱╭┫┣╮┃╰━╯┣┫┣┫╰━╯┃╱┃┃   #
# ╰╯╱╰┻╯╱╱╰━━╯╰━━━┻━━┻━━━╯╱╰╯   #
#################################  

##############################  Imports  ##################################
### stadard
import os
import sys
### self created
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, lib_path)
import lib.lib as lib
import config.menu.menu_settings as menu_settings

##############################  Settings  #################################

### file settings ###
### CLI
path_to_folder = input("Folder: (default: config/api/) ") or "config/api/"
filename = (input("Filename: (default: " + path_to_folder + "kraken_key.json)") or (path_to_folder + "kraken_key.json"))
print(path_to_folder + '\n' + filename)
### GUI
# print('Select file to edit (default: config/api/kraken_key.json)')
data, filename = lib.load_json_file(filename, path_to_folder)

#############################  Main Loop  #################################

while True:
    # refresh data table
    lib.create_api_table(data)    
    # Anzeigen der Optionen
    print ('API CONFIGURATION')
    option = lib.create_menu_with_options(menu_settings.api_list_menu_items.items())
 
    # Hinzufügen eines APIKeys
    if option == 1:
        data = lib.add_api_keys(data, id, menu_settings.api_list_headers)
        # Speichern der Daten in der JSON-Datei
        lib.write_json(data, filename)

    # Bearbeiten eines APIKeys
    elif option == 2:
        id_to_edit = input('Which ID should be edited? ')
        for obj in data:
            if id_to_edit in obj:
                lib.change_api_list(data, id_to_edit, menu_settings.api_list_headers)
                # Speichern der Daten in der JSON-Datei
                lib.write_json(data, filename)
                break
        else:
            print('no valid id')

    # Löschen eines API-Keys
    elif option == 3:
        id_to_delete = input('Which ID should be deleted? ')
        data = lib.delete_api_keys(data, id_to_delete)
        # Speichern der Daten in der JSON-Datei
        lib.write_json(data, filename)

    # Zurück
    elif option == 99:
        break

    else:
        print('\nno valid ID')

    
