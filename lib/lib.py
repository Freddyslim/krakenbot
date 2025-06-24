##############################  Imports  ##################################
### stadard
from prettytable import PrettyTable
import json
import pandas as pd
import os
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
### self created
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, lib_path)

#######################################################################
############################ functions ################################
#######################################################################
############################# API LIST ################################

def add_api_keys(data, id, headers):
    data[id] = {}  # Initialisiere das Dictionary für die ID
    for header in headers:
        data[id]['id'] = ''
        user_input = input(f"Bitte geben Sie einen Wert für '{header}' ein: ")
        data[id][header] = user_input
    return data

def change_api_list(data, id, headers):
    if id in data:
        for header in headers:
            user_input = input(f"Bitte geben Sie einen neuen Wert für '{header}' ein oder drücken Sie Enter für keine Veränderung: ")
            if user_input != "":
                data[id][header] = user_input
        return data
    else:
        print(f'ID {id} wurde nicht gefunden.')
        return data
    
def delete_api_keys(data, id_to_delete):
    print(f"Löschen des API-Key mit der ID {id_to_delete}")
    for key in data:
        print(f"suche nach API-Key mit der ID {id_to_delete}")
        print(type(key))
        print(type(id_to_delete))
        if data[key]["id"] == id_to_delete:
            del data[key]
            print(f'Der API-Key mit der ID {id_to_delete} wurde gelöscht.')
            return data
            
    print(f'Der API-Key mit der ID {id_to_delete} wurde nicht gefunden.')
    return data

def create_api_table(data):
    if len(data) == 0:
        print("No data to show.")
        return
    # Extrahiere die Spaltenüberschriften aus dem ersten Objekt in der Dictionary
    columns = list(data[next(iter(data))].keys())
    # Erstelle die PrettyTable-Instanz mit den Spaltenüberschriften
    table = PrettyTable(columns)
    # Setze die Ausrichtung auf links
    table.align = 'l'
    try:
        # Füge die Datenzeilen hinzu
        for entry in data.values():
            row = [entry[column] for column in columns]
            table.add_row(row)
        # Ausgabe der Tabelle
        print('\n' + str(table) + '\n')
    except Exception as e:
        print("Failed to show data: ", e)

########################### END API LIST ##############################       
########################## WITHDRAW ADRESS ############################       

def add_withdraw_adress(data, id, headers):
    data[id] = {}  # Initialisiere das Dictionary für die ID
    for header in headers:
        data[id]['id'] = ''
        user_input = input(f"Bitte geben Sie einen Wert für '{header}' ein: ")
        data[id][header] = user_input
    return data

def change_withdraw_adress(data, id):
    for d in data.values():
        if str(d['id']) == id:
            name = input('new name: ')
            api_key = input('new api_key: ')
            api_sec = input('new api_sec: ')
            if name!= '':
                d['name'] = name
            if api_key != '':
                d['api_key'] = api_key
            if api_sec != '':
                d['api_sec'] = api_sec
            print(f'Die Daten für ID {id} wurden aktualisiert.')
            break
    else:
        print(f'ID {id} wurde nicht gefunden.')
        
def delete_withdraw_adress(data, id_to_delete):
    print(f"Löschen des API-Key mit der ID {id_to_delete}")
    for key in data:
        print(f"suche nach API-Key mit der ID {id_to_delete}")
        print(type(key))
        print(type(id_to_delete))
        if data[key]["id"] == id_to_delete:
            del data[key]
            print(f'Der API-Key mit der ID {id_to_delete} wurde gelöscht.')
            return data
            
    print(f'Der API-Key mit der ID {id_to_delete} wurde nicht gefunden.')
    return data

def create_withdraw_table(data):
    if len(data) == 0:
        print("No data to show.")
        return
    # Extrahiere die Spaltenüberschriften aus dem ersten Objekt in der Dictionary
    columns = list(data[next(iter(data))].keys())
    # Erstelle die PrettyTable-Instanz mit den Spaltenüberschriften
    table = PrettyTable(columns)
    # Setze die Ausrichtung auf links
    table.align = 'l'
    try:
        # Füge die Datenzeilen hinzu
        for entry in data.values():
            row = [entry[column] for column in columns]
            table.add_row(row)
        # Ausgabe der Tabelle
        print('\n' + str(table) + '\n')
    except Exception as e:
        print("Failed to show data: ", e)

####################### END WITHDRAW ADRESS ##########################   

def create_balance_table(data):
    if not data:
        print("No data to show.")
        return
     
    # Extrahiere die Spaltenüberschriften
    columns = ['Asset', 'Balance']
        # Erstelle die PrettyTable-Instanz mit den Spaltenüberschriften
    table = PrettyTable(columns)
        # Setze die Ausrichtung auf links
    table.align = 'l'
    try:
        # Füge die Datenzeilen hinzu
        for asset, balance in data.items():
            table.add_row([asset, balance])
            
        # Ausgabe der Tabelle
        print(table)
        
    except Exception as e:
        print("Failed to show data:", e)

# write json with automatic id
def write_json(data, filename):
    id_counter = 1
    updated_data = {}
    if data:
        for key in data:
            item = data[key] # erstellt eine Kopie von `data[key]`
            item['id'] = str(id_counter)  # aktualisiert die `id` des Elements
            updated_data[str(id_counter)] = item  # fügt das aktualisierte Element zum `updated_data` hinzu
            id_counter += 1
        with open(filename, 'w') as f:
            json.dump(updated_data, f, indent=4)
        print('data updated sucessfully')

def display_data(data):
    x = PrettyTable()
    fields = ['Name'] # Standardliste mit der Spalte "Name"
    for _, value in data['result'].items():
        fields += list(value.keys()) # Aktualisieren der Spalten mit denen aus dem Dictionary
    x.field_names = fields
    for key, value in data['result'].items():
        row = [key]
        for field in fields[1:]: # Beginnen bei 1, um die "Name"-Spalte zu überspringen
            row.append(value.get(field, ''))
        x.add_row(row)
    print(x)


def display_data_balance(data):
    if not data:
        print('Error: No data provided')
        return
    if 'result' not in data or not data['result']:
        print('Error: Data format is incorrect')
        return

    table = PrettyTable()
    table.field_names = ['Currency', 'Balance']

    for currency, balance in data['result'].items():
        table.add_row([currency, balance])

    print(table)


def excel_to_json(excel_file, sheet_name, json_file):
    # Read Excel file into a pandas dataframe
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Convert dataframe to a dictionary
    data_dict = df.to_dict(orient='records')
    
    # Write dictionary to a JSON file
    with open(json_file, 'w') as f:
        json.dump(data_dict, f, indent=4)

def json_to_prettytable(json_data):
    data = json.loads(json_data)
    table = PrettyTable()
    table.field_names = list(data[0].keys())
    for row in data:
        table.add_row(list(row.values()))
    return table.get_string()

def create_menu_with_options(menu_items):
    for key, value in menu_items:
        print(f"{key}. {value}")
    option = int(input('\nOption: '))
    print ('\n')
    return option


def load_json_file(filename, path_to_folder):
    # try:
    #     app = QApplication([])
    #     filename, _ = QFileDialog.getOpenFileName(None, "Datei auswählen")
    #     with open(filename) as json_data:
    #         data = json.load(json_data)
    # except FileNotFoundError:
    # print('Datei wurde nicht gefunden.')
    #create folder if not exists
    if not os.path.exists(os.path.dirname(path_to_folder)):
        os.makedirs(os.path.dirname(path_to_folder))
    # Überprüfen, ob die Datei bereits vorhanden ist
    if os.path.isfile(filename):
        # Die Datei ist vorhanden, also wird sie geöffnet und der Inhalt wird gelesen
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        # Die Datei ist nicht vorhanden, also wird sie erstellt und mit einem leeren Dictionary initialisiert
        data = {}

    # Schreiben Sie das aktualisierte Dictionary in die Datei
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
            
    return data, filename

# def select_api_keys():


# def select_api_key():

# def create_generic_table(filename):
#     with open(filename) as f:
#         data = json.load(f)

#     # Erstellen der Tabelle
#     table = PrettyTable()
#     headers = set()
#     for item in data:
#         headers.update(item.keys())
#     table.field_names = list(headers)
#     table.align = 'l'
#     for item in data:
#         row = []
#         for header in headers:
#             row.append(item.get(header, ''))
#         table.add_row(row)

#     # Ausgabe der Tabelle
#     print('\n' + str(table) + '\n')
        
#     # Gib die Tabelle aus
#     print(table)