# Using the Kraken Bot

This repository contains a simple command line tool that interacts with the Kraken cryptocurrency exchange. After setting up the environment described in the main `README.md` you can start the interactive menu.

## Start the bot

1. Activate your Python virtual environment if it is not already active.
2. Run the main entry point:
   ```bash
   python main.py
   ```
3. You will see a menu similar to this:
   ```
   KRAKEN REMOTE

   1 - Manage API keys
   2 - Manage withdraw addresses
   3 - Make a Kraken request
   4 - Telegram bot
   5 - Chatbots
   99 - Exit
   ```
4. Enter the number of the option you want to use and press `Enter`.
5. When you are done you can choose `99` to exit or press `CTRL+C` if needed.

Each menu item loads a small module that performs the selected task. The project is experimental, so review the modules before using them with real funds.
