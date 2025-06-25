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
    "pair": "XBTEUR",
    "lookback_days": 365,
    "interval": 1440,
    "profit_pct": 2.0,
    "start_balance": 1000,
    "wave_threshold_pct": 2.5
}
```

### Options

- **pair** – Kraken trading pair used to retrieve price data.
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

Historical data is requested via Kraken's OHLC endpoint, which accepts specific
intervals:

- **Intervals**: `1`, `5`, `15`, `30`, `60`, `240`, `1440`, `10080`, `21600`

Intraday intervals can be queried for roughly the last 60 days of history.

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
