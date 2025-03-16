# Arc'teryx Beta LT Jacket Price Scanner

A simple price scanner that monitors Dutch retailers for the Arc'teryx Beta LT Jacket and sends Telegram notifications when the price drops below €250.

## Features

- Monitors multiple Dutch retailers for price changes
- Sends notifications via Telegram when price drops below target
- Runs automatically every 3 hours
- Easy to configure and extend

## Setup

1. Clone this repository:
```bash
git clone https://github.com/rogierx/arc-scanner.git
cd arc-scanner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a Telegram bot:
   - Message @BotFather on Telegram
   - Create a new bot using the `/newbot` command
   - Save the bot token you receive

4. Get your Telegram chat ID:
   - Message your bot
   - Visit: `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
   - Look for the `chat.id` in the response

5. Create a `.env` file in the project root:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## Usage

Run the scanner:
```bash
python scanner.py
```

The script will:
- Check prices immediately on startup
- Continue checking every 3 hours
- Send Telegram notifications when prices drop below €250

## Deployment

You can deploy this for free on PythonAnywhere:

1. Create a free account on [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload the files using the Files tab
3. Create a new task in the Tasks tab to run the script
4. Set it to run every 3 hours

## Supported Retailers

- Bergfreunde.nl
- Zwerfkei.nl
- Snowleader.nl
- Coef.nl
- Bever.nl

## Contributing

Feel free to add more retailers or improve the code! Just submit a pull request.