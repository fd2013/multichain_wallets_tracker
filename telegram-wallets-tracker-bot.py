import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import aiohttp
import json

# API Keys and endpoints
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
EXPLORER_APIS = {
    "ethereum": {
        "key": "YOUR_ETHERSCAN_API_KEY",
        "url": "https://api.etherscan.io/api"
    },
    "bsc": {
        "key": "YOUR_BSCSCAN_API_KEY",
        "url": "https://api.bscscan.com/api"
    },
    "polygon": {
        "key": "YOUR_POLYGONSCAN_API_KEY",
        "url": "https://api.polygonscan.com/api"
    },
    "avalanche": {
        "key": "YOUR_SNOWTRACE_API_KEY",
        "url": "https://api.snowtrace.io/api"
    },
    "arbitrum": {
        "key": "YOUR_ARBISCAN_API_KEY",
        "url": "https://api.arbiscan.io/api"
    },
    "optimism": {
        "key": "YOUR_OPTIMISTIC_ETHERSCAN_API_KEY",
        "url": "https://api-optimistic.etherscan.io/api"
    },
    "fantom": {
        "key": "YOUR_FTMSCAN_API_KEY",
        "url": "https://api.ftmscan.com/api"
    }
}

async def fetch_latest_transaction(network: str, address: str) -> dict:
    """Fetch the latest transaction for a given address on specified network."""
    if network not in EXPLORER_APIS:
        raise ValueError(f"Unsupported network: {network}")
    
    api_config = EXPLORER_APIS[network]
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 1,
        "sort": "desc",
        "apikey": api_config["key"]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(api_config["url"], params=params) as response:
            data = await response.json()
            
            if data["status"] == "1" and data["result"]:
                return data["result"][0]
            else:
                raise ValueError(f"No transactions found or API error: {data.get('message')}")

def format_transaction(tx: dict, network: str) -> str:
    """Format transaction data into readable message."""
    explorer_urls = {
        "ethereum": "https://etherscan.io",
        "bsc": "https://bscscan.com",
        "polygon": "https://polygonscan.com",
        "avalanche": "https://snowtrace.io",
        "arbitrum": "https://arbiscan.io",
        "optimism": "https://optimistic.etherscan.io",
        "fantom": "https://ftmscan.com"
    }
    
    return (
        f"Network: {network.upper()}\n"
        f"Hash: {tx['hash']}\n"
        f"From: {tx['from']}\n"
        f"To: {tx['to']}\n"
        f"Value: {float(tx['value']) / 10**18:.6f} (native token)\n"
        f"Transaction Fee: {float(tx['gasPrice']) * float(tx['gasUsed']) / 10**18:.6f}\n"
        f"View: {explorer_urls[network]}/tx/{tx['hash']}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(
        "Welcome! Use /tx <network> <address> to fetch the latest transaction.\n"
        "Supported networks: ethereum, bsc, polygon, avalanche, arbitrum, optimism, fantom"
    )

async def get_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tx command."""
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /tx <network> <address>")
        return
    
    network = context.args[0].lower()
    address = context.args[1]
    
    try:
        tx = await fetch_latest_transaction(network, address)
        message = format_transaction(tx, network)
        await update.message.reply_text(message)
    except ValueError as e:
        await update.message.reply_text(f"Error: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"An unexpected error occurred: {str(e)}")

def main():
    """Initialize and run the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tx", get_transaction))
    
    application.run_polling()

if __name__ == "__main__":
    main()
