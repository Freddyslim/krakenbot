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
    "debug": true
}
```

### Fields

- **symbol** – Ticker symbol used for price retrieval via Yahoo Finance.
- **refresh_rate** – Seconds between price checks.
- **startbuy_threshold** – Percentage difference between the two initial buy orders.
- **initial_portfolio_eur** – Euro amount used for the very first trade.
- **reinvestment_percent** – Percentage of the current portfolio that is reinvested after each completed cycle.
- **take_profit_percent** – Profit target above the last buy price before a sell order is placed.
- **buyback_percent** – Price drop below the last sell price before a new buy is placed.
- **safety_offset** – Offset applied to limit orders to increase the chance of execution.
- **debug** – If `true`, the bot prints all status information to the console.

## Running the bot

Start the chatbot menu and select the LimitCycleBot or run it directly:

```bash
python -m modules.chatbot.limit_cycle_bot
```

The bot places two initial limit buy orders slightly above and below the current price. After one fills, it sets a take-profit sell order and later a new buy order. Each log output also shows the last realised profit once a full buy/sell cycle was completed.
