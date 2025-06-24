"""Runner for example chatbots."""

from .base import TickerBot


def run() -> None:
    """Simple interface for running demo chatbots."""
    print("CHATBOT DEMO")
    print("1. Run ticker bot")
    print("99. Back")
    choice = input("Option: ") or "99"
    if choice == "1":
        pair = input("Kraken pair (default: XBTUSD): ") or "XBTUSD"
        symbol = input("Yahoo symbol (default: AAPL): ") or "AAPL"
        bot = TickerBot(pair=pair, symbol=symbol)
        bot.run()


