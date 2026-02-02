# Telegram Notifications Setup Guide

## Step 1: Create a Telegram Bot

1. **Open Telegram** and search for `@BotFather`
2. **Start a conversation** with BotFather
3. **Send the command**: `/newbot`
4. **Follow the prompts**:
   - Choose a name for your bot (e.g., "Jal Rakshak Alert Bot")
   - Choose a username (must end with `bot`, e.g., `jalrakshak_alert_bot`)
5. **Copy the bot token** that BotFather gives you (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Get Your Chat ID

You need to get your Telegram chat ID to receive notifications. Here are two methods:

### Method 1: Using a Helper Bot (Easiest)

1. Search for `@userinfobot` on Telegram
2. Start a conversation with it
3. It will reply with your chat ID (a number like `123456789`)

### Method 2: Using API (Manual)

1. **Start a conversation** with your bot (search for your bot's username)
2. **Send any message** to your bot (e.g., "Hello")
3. **Open this URL in your browser** (replace `YOUR_BOT_TOKEN` with your actual token):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
4. Look for `"chat":{"id":123456789}` in the response - that number is your chat ID

## Step 3: Update Configuration

1. Open `trigger/config.py`
2. Update `TELEGRAM_BOT_TOKEN` with your bot token from Step 1
3. Update `TELEGRAM_CHAT_IDS` with your chat ID(s) from Step 2:
   ```python
   TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
   TELEGRAM_CHAT_IDS = [
       "YOUR_CHAT_ID_HERE",  # Add your chat ID as a string
       # Add more chat IDs if you want multiple recipients
   ]
   ```

## Step 4: Test the Setup

Run the test script:
```bash
cd trigger
python3 telegram_alert.py
```

Or test via the API:
```bash
curl -X POST http://localhost:5000/api/send-alert \
  -H "Content-Type: application/json" \
  -d '{"message": "Test alert from Jal Rakshak!"}'
```

## Troubleshooting

### "Forbidden: bot was blocked by the user"
- The chat ID is blocked or the user hasn't started a conversation with the bot
- **Solution**: Start a conversation with your bot first, then try again

### "Unauthorized" or "Invalid token"
- Your bot token is incorrect
- **Solution**: Double-check the token in `config.py` matches what BotFather gave you

### "Chat not found"
- The chat ID is incorrect
- **Solution**: Get your chat ID again using Method 1 or 2 above

### No errors but no message received
- Make sure you've started a conversation with your bot
- Check that your chat ID is correct and added to `TELEGRAM_CHAT_IDS`

## Current Status

Based on the test:
- ✅ Bot token appears to be valid
- ✅ Chat ID `1129126139` is working
- ❌ Chat ID `1456097608` is blocked - user needs to unblock the bot or start a new conversation
