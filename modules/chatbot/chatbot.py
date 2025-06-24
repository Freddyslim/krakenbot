"""Runner for example chatbots."""

from .base import TickerBot
from .elliott_wave_bot import ElliottWaveBot, Settings


def run() -> None:
    """Simple interface for running demo chatbots."""
    print("CHATBOT DEMO")
    print("1. Run ticker bot")
    print("2. Run Elliott wave bot")
    print("99. Back")
    choice = input("Option: ") or "99"
    if choice == "1":
        pair = input("Kraken pair (default: XBTUSD): ") or "XBTUSD"
        symbol = input("Yahoo symbol (default: AAPL): ") or "AAPL"
        bot = TickerBot(pair=pair, symbol=symbol)
        bot.run()
    elif choice == "2":
        filename = (
            input(
                "Settings file (default: config/chatbot/elliott_wave_settings.json): "
            )
            or "config/chatbot/elliott_wave_settings.json"
        )
        settings = Settings.load(filename)
        bot = ElliottWaveBot(settings)
        bot.run()


