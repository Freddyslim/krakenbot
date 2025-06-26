"""Runner for example chatbots."""

from .base import TickerBot
from .elliott_wave_bot import ElliottWaveBot, Settings
from .live_trader_bot import LiveTraderBot, LiveSettings
from .limit_cycle_bot import LimitCycleBot, CycleSettings


def run() -> None:
    """Simple interface for running demo chatbots."""
    print("CHATBOT DEMO")
    print("1. Run ticker bot")
    print("2. Run Elliott wave bot")
    print("3. Run live trader bot")
    print("4. Run limit cycle bot")
    print("5. Run cycle bot tests")
    print("6. Evaluate cycle bot logs")
    print("7. Run cycle backtest")
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
    elif choice == "3":
        filename = (
            input(
                "Settings file (default: config/chatbot/live_trader_settings.json): "
            )
            or "config/chatbot/live_trader_settings.json"
        )
        settings = LiveSettings.load(filename)
        bot = LiveTraderBot(settings)
        bot.run()
    elif choice == "4":
        filename = (
            input(
                "Settings file (default: config/chatbot/limit_cycle_settings.json): "
            )
            or "config/chatbot/limit_cycle_settings.json"
        )
        settings = CycleSettings.load(filename)
        bot = LimitCycleBot(settings)
        bot.run()
    elif choice == "5":
        from .test_runner import run_cycle_tests

        run_cycle_tests()
    elif choice == "6":
        from .evaluate_cycle_logs import find_best

        num = input("Number of results (default 5): ") or "5"
        find_best(int(num))
    elif choice == "7":
        from .cycle_backtest import run_backtest

        run_backtest()


