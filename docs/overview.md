# Project Overview

```mermaid
flowchart TD
    A[main.py] --> B[API key management]
    A --> C[Withdraw addresses]
    A --> D[Kraken requests]
    A --> E[Telegram bot]
    A --> J[Chatbots]
    B --> F[config/api/kraken_key.json]
    C --> G[config/api/withdraw_db.json]
    E --> H[config/telegram/bot_settings.json]
    D --> I[lib/kraken_api.py]
    J --> K[modules/chatbot]
    K --> L[config/chatbot/elliott_wave_settings.json]
    K --> M[config/chatbot/live_trader_settings.json]
    K --> N[config/chatbot/limit_cycle_settings.json]
```

This diagram shows the high level components of the project and how they relate
to the configuration files used for accessing the Kraken API and for running the
Telegram bot.

Additional strategy bots use JSON settings located in `config/chatbot/`. Along
with the Elliott wave example you can configure a continuously running
`LiveTraderBot` via `live_trader_settings.json` described in
`docs/live_trader_bot.md`. The new `LimitCycleBot` uses
`limit_cycle_settings.json` and is documented in `docs/limit_cycle_bot.md`.
