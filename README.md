# Kraken Tool

This project is an experimental command line interface for the [Kraken](https://www.kraken.com/) cryptocurrency exchange. The code base was originally created for personal use and is not actively maintained. The repository contains various modules for interacting with the Kraken API, editing API credentials and exporting data such as trade history or ledger information.

## Warning

The original repository stored real API credentials in `config/api/kraken_key.json`. These files have been removed from version control. **Never store API keys directly in the repository**. Always use environment variables or configuration files that are ignored by Git.

## Requirements

- Python 3.10+
- The packages listed in `requirements.txt` (generate it from your environment or adjust as needed)

To keep the dependencies separated from the rest of your system we recommend creating a
Python *virtual environment* in the project folder. Follow these steps:

1. Open a terminal and change to the folder that contains this README.
2. Create the environment:
   ```bash
   python3 -m venv .venv
   ```
3. Activate the environment:
   - **Windows**
     ```cmd
     .venv\Scripts\activate
     ```
   - **macOS/Linux**
     ```bash
     source .venv/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. When you are finished you can leave the environment by running `deactivate`.

## Configuration

Copy the example files and fill in your own credentials:

```bash
cp config/api/kraken_key.json.example config/api/kraken_key.json
cp config/api/withdraw_db.json.example config/api/withdraw_db.json
```

Edit the new `.json` files with your API keys and withdraw settings. Keep these files outside of version control.

## Usage

The entry point is `main.py`. Running it will display a simple menu interface:

```bash
python main.py
```

From there you can manage API keys, withdraw addresses and perform a limited set of Kraken requests. Many features are incomplete and should be reviewed before real trading use.

For a step-by-step guide on starting and using the menu see [BOT_USAGE.md](BOT_USAGE.md).

## Security Notes

- Use API keys with the minimal set of permissions required for your tasks.
- Keep key files secure and never commit them to Git.
- This code executes modules using `exec`, which can be unsafe. Review modules before running.
- Consider using virtual environments and restricting network access when testing.

## Project Status

This project is provided as-is for reference. It has not been updated to modern best practices and is not recommended for production trading without significant auditing and refactoring.
