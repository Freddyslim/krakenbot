# ElliottWaveBot

`ElliottWaveBot` is an experimental strategy that tries to detect basic Elliott wave
patterns in historical price data. It loads settings from a JSON file so you can
quickly adjust parameters without modifying the code. The bot only prints buy and
sell signals and performs a simple simulation to show the resulting balance if
you had followed those trades.

## Configuration

Copy `config/chatbot/elliott_wave_settings.json.example` to
`config/chatbot/elliott_wave_settings.json` and edit the values:

```json
{
    "symbol": "BTC-USD",
    "period": "1y",
    "interval": "1d",
    "profit_pct": 2.0,
    "start_balance": 1000,
    "wave_threshold_pct": 2.5
}
```

### Options

- **symbol** – Ticker symbol used with Yahoo Finance. Determines which asset
  prices are analysed.
- **period** – How far back the historical data should go (e.g. `1y` for one
  year or `6mo` for six months).
- **interval** – Resolution of the price data (`1d`, `1h`, etc.). Shorter
  intervals increase the number of potential waves and therefore trades.
- **profit_pct** – Minimum percentage difference between a low and the
  subsequent high before a trade is triggered. Larger values reduce the number of
  trades but target higher profits.
- **start_balance** – Virtual starting balance used for the simulation.
- **wave_threshold_pct** – Percentage price move required to mark a new swing in
  the simplified wave detection. Lower values create more waves and therefore
  more trades.

### Valid periods and intervals

Historical data is requested via Yahoo Finance, which accepts specific strings
for time ranges and resolutions:

- **Periods**: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`,
  `max`
- **Intervals**: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`,
  `1wk`, `1mo`, `3mo`

Intraday intervals (`1m`–`1h`) are limited to roughly the last 60 days of
history.

Changing these values influences how many signals the bot will generate. For
example, reducing `wave_threshold_pct` and `interval` leads to frequent trades
on small moves while increasing them will result in fewer but potentially larger
trades.

## Running the bot

Start the chatbot menu and choose the Elliott wave bot:

```bash
python -m modules.chatbot.chatbot
```

When prompted for a settings file you can either accept the default path or
specify your own configuration. The bot will fetch historical prices, generate
signals and display the final simulated balance along with the executed trades.
