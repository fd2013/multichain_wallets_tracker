# Blockchain Transaction Bot

A Telegram bot that fetches the latest transaction for wallet addresses across multiple blockchain networks.

## Supported Networks
- Ethereum
- Binance Smart Chain
- Polygon
- Avalanche
- Arbitrum
- Optimism
- Fantom

## Prerequisites
- Python 3.7+
- Telegram Bot Token
- API keys from blockchain explorers

## Getting a Telegram Bot Token
1. Open Telegram and search for @BotFather
2. Send `/newbot` command
3. Follow prompts to set:
   - Bot name (display name)
   - Bot username (must end in 'bot')
4. BotFather will provide a token like: `123456789:ABCdefGHIjklmNOPQrstUVwxyz`
5. Keep this token secure - it provides full control of your bot

## Installation
```bash
pip install python-telegram-bot aiohttp
```

## Configuration
1. Create a Telegram bot via BotFather
2. Obtain API keys from blockchain explorers:
   - [Etherscan](https://etherscan.io/apis)
   - [BSCScan](https://bscscan.com/apis)
   - [PolygonScan](https://polygonscan.com/apis)
   - [Snowtrace](https://snowtrace.io/apis)
   - [Arbiscan](https://arbiscan.io/apis)
   - [Optimistic Etherscan](https://optimistic.etherscan.io/apis)
   - [FTMScan](https://ftmscan.com/apis)
3. Update API keys in the script

## Usage
1. Start the bot:
```bash
python bot.py
```

2. Telegram Commands:
- `/start` - Welcome message
- `/tx <network> <address>` - Get latest transaction

Example:
```
/tx ethereum 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

## Error Handling
- Invalid network names
- Invalid addresses
- API rate limits
- Network connection issues

## License
MIT
