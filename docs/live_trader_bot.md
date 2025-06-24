# LiveTraderBot

`LiveTraderBot` ist ein einfacher Bot, der kontinuierlich Kursdaten aus Yahoo Finance auswertet und anhand einer Moving-Average-Strategie Kauf- und Verkaufszeitpunkte simuliert. Im Gegensatz zum `ElliottWaveBot` stoppt dieser Bot nicht nach einer Simulation, sondern läuft dauerhaft weiter und aktualisiert seine Berechnungen regelmäßig.

## Konfiguration

Kopiere `config/chatbot/live_trader_settings.json.example` nach `config/chatbot/live_trader_settings.json` und passe die Werte an:

```json
{
    "symbol": "BTC-USD",
    "lookback_days": 30,
    "interval": "1h",
    "trade_amount": 1000,
    "profit_target_pct": 1.5,
    "check_interval": 30,
    "debug": true
}
```

### Felder

- **symbol** – Ticker‑Symbol für Yahoo Finance (z. B. `BTC-USD`).
- **lookback_days** – Wie viele Tage an Historie beim Abruf verwendet werden.
- **interval** – Zeitintervall der historischen Daten (`1h`, `1d` …).
- **trade_amount** – Virtuelles Startkapital, das beim ersten Kaufsignal eingesetzt wird.
- **profit_target_pct** – Prozentualer Aufschlag auf den Kaufkurs, bei dem ein Verkauf erfolgen soll.
- **check_interval** – Wie viele Sekunden zwischen zwei Aktualisierungen liegen.
- **debug** – Wenn `true`, werden die berechneten Werte jedes Mal auf der Konsole ausgegeben.

Während der Laufzeit speichert der Bot seinen Zustand in `output/live_trader_state.json`. Dort findest du den aktuellen Kurs, gleitende Durchschnitte, offene Positionen und die letzte Aktion.

## Starten des Bots

Der Bot kann über das Chatbot-Menü gestartet werden:

```bash
python -m modules.chatbot.chatbot
```

Option **3** wählt den LiveTraderBot. Anschließend kann ein abweichender Pfad zur Einstellungsdatei angegeben werden oder du bestätigst den Standardpfad.

## Funktionsweise

Alle `check_interval` Sekunden ruft der Bot die jüngsten Kursdaten für das gewünschte Symbol ab. Liegt der kurzfristige gleitende Durchschnitt über dem langfristigen Durchschnitt und der aktuelle Kurs nicht wesentlich darüber, wird mit dem verfügbaren Kapital gekauft. Nach einem Kauf wird ein Verkaufsziel berechnet (`profit_target_pct`). Erreicht der Kurs dieses Ziel, wird verkauft und die Position geschlossen. Jede Berechnung wird in die Zustandsdatei geschrieben, sodass du jederzeit sehen kannst, welche Daten analysiert wurden und welche Entscheidung getroffen wurde.
