# Kraken API Overview

Die Datei `lib/kraken_api.py` enthält kleine Helferfunktionen für die wichtigsten Endpunkte der Kraken REST‑API. Im Menü "Kraken Request" können sie über die ID des gewünschten API‑Schlüssels aufgerufen werden. Folgende Funktionen stehen zur Verfügung:

| Funktion                | Beschreibung                                           |
|-------------------------|--------------------------------------------------------|
| `get_acc_balance`       | Kontostand aller Assets abrufen. Benötigt privaten API‑Key. |
| `get_trade_balance`     | Übersicht über das Trading-Konto.                      |
| `get_open_orders`       | Alle offenen Order anzeigen.                            |
| `get_closed_orders`     | Abgeschlossene Order anzeigen.                          |
| `query_orders_info`     | Informationen zu bestimmten Order-IDs anfordern.       |
| `get_trades_history`    | Historie aller Trades zurückliefern.                   |
| `query_trades_info`     | Details zu einzelnen Trade-IDs.                        |
| `get_open_positions`    | Offene Positionen anzeigen.                            |
| `get_ledgers_info`      | Überblick über sämtliche Kontobewegungen.             |
| `query_ledgers_info`    | Details zu bestimmten Ledger-IDs.                      |
| `get_trade_volume`      | Handelsvolumen für bestimmte Währungspaare.           |
| `request_export_report` | Erstellung eines Export-Reports anstoßen.             |
| `ticker`                | Öffentlicher Aufruf – aktuelle Marktdaten zu einem Paar. |

Die privaten Funktionen benötigen einen gültigen API‑Key und das zugehörige Secret, wie in `config/api/kraken_key.json` hinterlegt. Die Namen der Parameter entsprechen direkt den Anforderungen der Kraken‑API, so dass du sie in beliebiger Kombination verwenden kannst.

Weitere Details zu den Parametern findest du in der offiziellen [Kraken API Dokumentation](https://docs.kraken.com/rest/).
