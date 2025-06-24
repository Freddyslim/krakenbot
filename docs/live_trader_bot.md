# LiveTraderBot

`LiveTraderBot` ist ein einfacher Bot, der kontinuierlich Kursdaten aus Yahoo Finance auswertet und anhand einer Moving-Average-Strategie Kauf- und Verkaufszeitpunkte simuliert. Er verschickt dabei lediglich Handlungsempfehlungen und führt keine echten Trades aus. Im Gegensatz zum `ElliottWaveBot` stoppt dieser Bot nicht nach einer Simulation, sondern läuft dauerhaft weiter und aktualisiert seine Berechnungen regelmäßig. Aktivierst du Telegram, werden die Empfehlungen an dein Chatfenster gesendet.

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
    "debug": true,
    "telegram_enabled": false,
    "telegram_settings_file": "config/telegram/bot_settings.json"
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
- **telegram_enabled** – Wenn `true`, werden Empfehlungen per Telegram verschickt.
- **telegram_settings_file** – Pfad zur Datei mit Bot-Token und Chat-ID.

Während der Laufzeit speichert der Bot seinen Zustand in `output/live_trader_state.json`. Dort findest du den aktuellen Kurs, gleitende Durchschnitte, offene Positionen und die letzte Aktion.

## Starten des Bots

Der Bot kann über das Chatbot-Menü gestartet werden:

```bash
python -m modules.chatbot.chatbot
```

Option **3** wählt den LiveTraderBot. Anschließend kann ein abweichender Pfad zur Einstellungsdatei angegeben werden oder du bestätigst den Standardpfad.

## Funktionsweise

Alle `check_interval` Sekunden ruft der Bot die jüngsten Kursdaten für das gewünschte Symbol ab. Liegt der kurzfristige gleitende Durchschnitt über dem langfristigen Durchschnitt und der aktuelle Kurs nicht wesentlich darüber, empfiehlt der Bot einen Kauf. Nach einem virtuellen Kauf wird ein Verkaufsziel berechnet (`profit_target_pct`). Erreicht der Kurs dieses Ziel, wird eine Verkaufsempfehlung ausgesprochen und die Position geschlossen. Jede Berechnung wird in die Zustandsdatei geschrieben, sodass du jederzeit sehen kannst, welche Daten analysiert wurden und welche Entscheidung getroffen wurde.

Darüber hinaus berechnet der Bot einen simulierten Gesamtgewinn basierend auf den ausgeführten Kauf- und Verkaufssignalen. Dieser Wert erscheint im Terminal und wird in der Logdatei notiert. Wird der Bot mit identischen Einstellungen erneut gestartet, liest er den letzten Stand aus `output/live_trader_state.json` ein und führt die Berechnung fort.

## Logging

Bei jedem Start legt der Bot eine Logdatei im Ordner `log/` an. Darin werden die verwendeten Einstellungen sowie alle versendeten Telegram-Nachrichten festgehalten. Der Ordner steht in der `.gitignore`, damit keine sensiblen Informationen versioniert werden.
