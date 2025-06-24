import json
import os
import sys
from typing import Dict

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, lib_path)

import lib.kraken_api as kraken_api


def load_bot_settings(filename: str = "config/telegram/bot_settings.json") -> Dict:
    """Load Telegram bot settings from a JSON file."""
    try:
        with open(filename, "r") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


def _get_api_pair(api_id: str) -> tuple[str, str]:
    creds = kraken_api.load_credentials()
    try:
        return kraken_api.get_api_pair(creds, api_id)
    except ValueError as exc:
        raise RuntimeError("API credentials not found") from exc


async def cmd_start(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Available commands:\n/balance - show account balance\n/ticker <pair> - show ticker info"
    )


async def cmd_balance(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = context.bot_data.get("settings")
    api_key, api_sec = _get_api_pair(settings.get("api_id", "1"))
    data = kraken_api.get_acc_balance(api_key, api_sec)
    result = data.get("result", {})
    if not result:
        await update.message.reply_text("Failed to fetch balance")
        return
    text = "Balance:\n" + "\n".join(f"{k}: {v}" for k, v in result.items())
    await update.message.reply_text(text)


async def cmd_ticker(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pair = " ".join(context.args) if context.args else "XBTUSD"
    data = kraken_api.ticker(pair)
    result = data.get("result")
    if not result:
        await update.message.reply_text("Failed to fetch ticker")
        return
    info = next(iter(result.values()))
    text = f"Ticker {pair}: Last price {info.get('c',[0])[0]}"
    await update.message.reply_text(text)


def run() -> None:
    settings = load_bot_settings()
    token = settings.get("bot_token")
    if not token:
        print("Bot token not configured")
        return

    app = ApplicationBuilder().token(token).build()
    app.bot_data["settings"] = settings

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("balance", cmd_balance))
    app.add_handler(CommandHandler("ticker", cmd_ticker))

    print("Telegram bot running... press Ctrl+C to stop")
    app.run_polling()


if __name__ == "__main__":
    run()
