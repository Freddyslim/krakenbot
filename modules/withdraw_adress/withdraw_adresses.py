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
filename = (input("Filename: (default: " + path_to_folder + "withdraw_db.json)") or (path_to_folder + "withdraw_db.json"))
print(path_to_folder + '\n' + filename)
### GUI
print('Select file to edit (default: config/api/withdraw.db.json)')
data, filename = lib.load_json_file(filename, path_to_folder)

#############################  Main Loop  #################################

while True:
    print ('WITHDRAW ADRESSEN')
    ### refresh data table
    lib.create_withdraw_table(data)
    option = lib.create_menu_with_options(menu_settings.withdraw_adresses_menu_items.items())

    ### Hinzufügen einer withdraw Adresse
    if option == 1:
        lib.add_withdraw_adress(data, id, menu_settings.withdraw_adress_headers)
        # Aktualisieren der Daten in der JSON-Datei
        lib.write_json(data, filename)       
        
    ### Bearbeiten einer withdraw Adresse
    elif option == 2:
        id = input('ID des APIKeys: ')
        lib.change_withdraw_adress(data, id, menu_settings.withdraw_adress_headers)
        # Aktualisieren der Daten in der JSON-Datei
        lib.write_json(data, filename)     
        
    ### Löschen eines Withdraw Adresse
    elif option == 3:
        id_to_delete = input('ID des zu löschenden API-Keys: ')
        lib.delete_withdraw_adress(data, id_to_delete)
        # Aktualisieren der Daten in der JSON-Datei
        lib.write_json(data, filename) 

    ### Zurück
    elif option == 99:
        break

    else:
        print('\nno valid ID')

