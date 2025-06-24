# Header (hier kommt eine kurze Beschreibung des Programms und evtl Mitwirkende oder Lizenz)

###########
# Imports #
###########
import time
import requests
import urllib.parse
import hashlib
import hmac
import base64
import pandas as pd
import csv

#############
# Setup API #
#############
api_url = "https://api.kraken.com"
with open("krakenex/main/kraken.key", "r") as f:
    lines = f.read().splitlines()
    api_key = lines [0]
    api_sec = lines [1]

####################
# Define constants #
####################



#############
# Functions #
#############



#############
# Hauptcode #
#############

def main():

  time.sleep(2) # Pause für 2 Sekunden

######################
# Programm ausführen #
######################

if __name__ == "__main__":
  main()

################
# Schlusszeile #
################

print("Auf Wiedersehen!")
