# Jerry Bay Bot (@jerrybaybot)

A Telegram bot with three tools:
- 🖼 Image format converter
- 🎨 AI image generator (free, via Pollinations.ai)
- 🔗 URL shortener (free, via TinyURL)

## Commands
- `/start` — shows instructions
- `/convert <format>` — reply to a photo with this command (e.g. `/convert png`)
- `/generate <prompt>` — generates an AI image from a text prompt
- `/shorten <url>` — shortens a long URL

## Local Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/jerrybay-bot.git
   cd jerrybay-bot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your bot token:
   ```bash
   cp .env.example .env
   ```
   Get your token from [@BotFather](https://t.me/BotFather) on Telegram.

4. Export the token and run:
   ```bash
   export TELEGRAM_BOT_TOKEN=your_token_here
   python bot.py
   ```

## Deploy on Railway

1. Push this project to a GitHub repo.
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**.
3. Select your repo.
4. In Railway's **Variables** tab, add:
   - `TELEGRAM_BOT_TOKEN` = your token from BotFather
5. Railway will detect the `Procfile` and deploy automatically as a worker process (no web port needed — this bot uses polling).
6. Once deployed, check the **Deployments** logs for `"Jerry Bay Bot is starting..."` to confirm it's live.

## Notes
- This bot uses **polling**, not webhooks, so it works out of the box on Railway with no extra domain/webhook configuration.
- Never commit your `.env` file or bot token to GitHub — `.gitignore` already excludes it.
