# Kraken Tool


## Getting started
CLI Tool  
Kraken API documentation


Dieses Tool soll die Möglichkeit bieten Funktionen der Kraken API zu nutzen.


### Struktur

kraken_remote/
<details open>
  <summary>config/</summary>
  
  - some configuration files (.gitignore)
</details>

<details open>
  <summary>lib/</summary>

  - [ ] kranken_api.py (all available kraken_api functions from https://docs.kraken.com/rest/)
  - [ ] lib.py (all self-created functions)
</details>
  
<details open>
  <summary>modules/</summary>

  - [ ] api_list.py (module to edit User APIs)
  - [ ] download_ledger_history.py (module to download ledger history)
  - [ ] kraken_request.py (module to easy use all available kraken_api functions from https://docs.kraken.com/rest/)
  - [ ] withdraw_adresses.py (module to use withdraw addresses from kraken account)
</details>

<details open>
  <summary>output/</summary>

  - some output files, that are generated from request (.gitignore)
</details>

<details open>
  <summary>main.py (Program)</summary>

  - [ ] api_list.py
  - [ ] withdraw_adresses.py
  - [ ] kraken_request.py
</details>

  
.gitignore  
README.md


<br>

* * *
<br>

# To Dos

## Bots

- [ ] Auto buy and withdraw 
- [ ] download ledger history and make backup
- [ ] download history data for asset (1m, 15m, ...)

## Funktionen

- [ ] Funktionen so umschreiben, dass Eingangsvariablen definiert sind
- [ ] Kommentare hinzufügen oder überarbeiten
- [ ] download history ledger implementieren
- [ ] api_list ändern nicht fertig
- [ ] löschen bestätigen hinzufügen
- [ ] 

  

<details open>
  <summary>Kraken Requests</summary>

  * - [ ] Kraken Requests
  *   - [ ] Market Data
  *   - [ ] User Data
      *   - [x] Get Account Balance
      *   - [ ] Get Trade Balance
      *   - [ ] Get Open Orders
      *   - [ ] Get open Orders
      *   - [ ] Query Orders Info
      *   - [ ] Get Trades History
      *   - [ ] Query Trades Infos
      *   - [ ] Get Open Positions
      *   - [ ] Get Ledgers Info
      *   - [ ] Query Ledgers
      *   - [ ] Get Trade Volume
      *   - [ ] Request Export Report
  *   - [ ] Trading
  *   - [ ] Funding
  *   - [ ] Subaccount
  *   - [ ] Staking
  *   - [ ] Websocket
  *   - [ ] Ticker

</details>


<details open>
  <summary>Datenmanagement</summary> 
  
  *  - [ ] withdraw adresses
     * - [x] add withdraw address 
     * - [x] edit withdraw adress 
     * - [x] delete withdraw address
     * - [ ] show currencies table
     * - [ ] add column apiURL?
  *  - [ ] api management
     * - [x] add api pair 
     * - [x] edit api pair
     * - [x] delete api pair
     * - [ ] Selection of api keys?? # perhaps better with binding to requets itself? 

</details>

