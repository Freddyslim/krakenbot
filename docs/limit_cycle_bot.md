# LimitCycleBot

`LimitCycleBot` is a simple strategy that repeatedly places limit orders around the current price. The bot only simulates trades and prints regular status updates. Later it can be connected to the Kraken API.

## Configuration

Copy `config/chatbot/limit_cycle_settings.json.example` to `config/chatbot/limit_cycle_settings.json` and adjust the values:

```json
{
    "symbol": "BTC-EUR",
    "pair": "XBTEUR",
    "use_kraken_price": false,
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

-### Fields

- **pair** – Kraken trading pair used when fetching prices from the API.
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

The bot starts with a limit buy order slightly above the current price. After it fills, a stop-loss order is placed immediately. The take-profit sell order is only created once the price first reaches the configured target and then trails the price upwards. Once the position is closed, a new buy order is prepared. Each log output shows the last realised profit and the accumulated *Gesamtgewinn* across all cycles.

## Cycle bot tests

You can run many ``LimitCycleBot`` instances with random settings using the test
runner. Copy ``config/chatbot/test_runner_settings.json.example`` to
``config/chatbot/test_runner_settings.json`` and adjust the ``duration`` field:

```json
{
    "duration": "1h"
}
```

Allowed units are ``m`` (minutes), ``h`` (hours), ``d`` (days), ``w`` (weeks),
``mo`` (months) and ``y`` (years). Use ``"infinite"`` for an unlimited run.
Start the tests from the chatbot menu with option ``5``.

## Historical simulation

The ``BacktestLimitCycleBot`` runs the cycle strategy against saved price data and
tries multiple parameter combinations. Copy
``config/chatbot/cycle_backtest_settings.json.example`` to
``config/chatbot/cycle_backtest_settings.json`` and adjust the values. Provide a
CSV file via the ``data_file`` field containing ``time`` and ``close`` columns.
Ranges for the tested settings use objects with ``start``, ``end`` and ``step``
or a list of explicit values.

Start the backtest with:

```bash
python -m modules.chatbot.cycle_backtest
```

Logs are written to ``log/test/`` and ``summary.log`` lists all profits along
with the top five configurations.
