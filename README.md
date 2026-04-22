# Shelby Tele-Archive Bot

A decentralized Telegram Bot that bridges users to the [Shelby](https://shelby.xyz/) Web3 Storage Network. Send any file, photo, or video to the bot, and it will automatically generate AI-powered metadata summaries (via Google Gemini) and archive your assets permanently on-chain!

## Features
- **Auto-Summarization**: Uses Gemini 2.5 Flash to automatically summarize text and document metadata.
- **Web3 Storage**: Seamless integration with the Aptos-based Shelby Network.
- **Multi-format Support**: Uploads Text, Images, Documents (PDF/DOCX), and Videos (<20MB).
- **Two-way Archive**: Use `/list` to view your storage vault and `/download <blob_id>` to fetch files directly back into Telegram.
- **Hybrid Architecture**: Built with Python (`python-telegram-bot`) core and a Node.js Web3 bridging layer (`@shelby-protocol/sdk`).

## Prerequisites
- Python 3.10+
- Node.js 20+
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Google Gemini API Key
- Shelby Developer API Key
- An Aptos Wallet (with Testnet/Shelbynet APT for gas fees)

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/shelby-tele-archive-bot.git
   cd shelby-tele-archive-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. **Environment Configuration:**
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   Fill in your `.env` file with your credentials and keys:
   ```env
   TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
   GEMINI_API_KEY="your_google_gemini_api_key"
   
   SHELBY_NETWORK="shelbynet"
   SHELBY_API_KEY="your_shelby_developer_api_key"
   SHELBY_ACCOUNT_ADDRESS="0x..."
   SHELBY_ACCOUNT_PRIVATE_KEY="your_private_key"
   ```

4. **Run the Bot:**
   ```bash
   python main.py
   ```

## Docker Deployment
This repository comes with a `Dockerfile` pre-configured with a dual Python & Node.js runtime for easy deployment on a VPS or PaaS (like Render or Railway).

```bash
docker build -t shelby-bot .
docker run -d --name my-shelby-bot shelby-bot
```

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
