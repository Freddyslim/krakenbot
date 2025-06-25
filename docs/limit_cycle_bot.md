# LimitCycleBot

`LimitCycleBot` is a simple strategy that repeatedly places limit orders around the current price. The bot only simulates trades and prints regular status updates. Later it can be connected to the Kraken API.

## Configuration

Copy `config/chatbot/limit_cycle_settings.json.example` to `config/chatbot/limit_cycle_settings.json` and adjust the values:

```json
{
    "symbol": "BTC-USD",
    "refresh_rate": 2,
    "startbuy_threshold": 0.4,
    "initial_portfolio_eur": 1000,
    "reinvestment_percent": 15,
    "take_profit_percent": 0.8,
    "buyback_percent": 0.5,
    "safety_offset": 0.15,
    "enable_stop_loss": false,
    "stop_loss_percent": 2.0,
    "debug": true,
    "log_interval_terminal": 1,
    "log_interval_file": 1,
    "auto_log": true
}
```

### Fields

- **symbol** – Ticker symbol used for price retrieval via Yahoo Finance.
- **refresh_rate** – Seconds between price checks.
- **startbuy_threshold** – Percentage above the current price for the initial buy order.
- **initial_portfolio_eur** – Euro amount used for the very first trade.
- **reinvestment_percent** – Percentage of the current portfolio that is reinvested after each completed cycle.
- **take_profit_percent** – Profit target above the last buy price before a sell order is placed.
- **buyback_percent** – Price drop below the last sell price before a new buy is placed.
- **safety_offset** – Offset applied to limit orders to increase the chance of execution.
- **enable_stop_loss** – If `true`, the bot places a stop-loss order after each buy.
- **stop_loss_percent** – Distance below the buy price at which the stop-loss triggers.
- **debug** – If `true`, the bot prints all status information to the console.
- **log_interval_terminal** – Number of refresh cycles between terminal log outputs.
- **log_interval_file** – Number of refresh cycles between file log entries.
- **auto_log** – If `true`, log output appears only when portfolio values change; when `false`, logs are printed on every interval.

## Running the bot

Start the chatbot menu and select the LimitCycleBot or run it directly:

```bash
python -m modules.chatbot.limit_cycle_bot
```

The bot starts with a limit buy order slightly above the current price. After it fills, a take-profit sell order and an optional stop-loss are placed. Once the position is closed, a new buy order is prepared. Each log output also shows the last realised profit once a full buy/sell cycle was completed.
