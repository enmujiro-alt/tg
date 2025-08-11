# YouTube Downloader Telegram Bot

## How to deploy on Railway

1. Create a Telegram bot with @BotFather and get your BOT_TOKEN.
2. Upload this project to GitHub.
3. On https://railway.app, create a new project by deploying from your GitHub repository.
4. Add the environment variable:
   ```
   BOT_TOKEN = your_bot_token_here
   ```
5. Railway will install dependencies and start the bot automatically.

## Notes

- Telegram limits files to about 50 MB. Larger videos cannot be sent.
- You can improve the bot to send audio only or upload large files to external storage.

## License

Use responsibly.
