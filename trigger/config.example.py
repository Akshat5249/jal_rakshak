# Telegram Bot API configuration
# Copy this file to config.py and fill in your actual values
# NEVER commit config.py to git!

import os

# Get your bot token from @BotFather on Telegram
# Set this as an environment variable: export TELEGRAM_BOT_TOKEN="your_token_here"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# List of Telegram chat IDs to send alerts to
# To get chat IDs: send a message to your bot, then call https://api.telegram.org/bot<TOKEN>/getUpdates
# Or use: python get_chat_id.py
# Set as environment variable: export TELEGRAM_CHAT_IDS='["chat_id1", "chat_id2"]'
TELEGRAM_CHAT_IDS_STR = os.getenv("TELEGRAM_CHAT_IDS", "[]")
try:
    import json
    TELEGRAM_CHAT_IDS = json.loads(TELEGRAM_CHAT_IDS_STR)
except:
    TELEGRAM_CHAT_IDS = []

# Alert templates for different scenarios
# 🚨 To add a new alert type, add a new key-value pair below
ALERT_TEMPLATES = {
    "flood": "🚨 Flood Alert! Please move to higher ground immediately.",
    "contamination": "🔥 Contamination Alert! Evacuate the area immediately.",
    "thunderstorm": "⛈️ Thunderstorm Warning! Stay indoors and avoid open areas.",
    "lockdown": "🔒 Lockdown Alert! Please stay where you are and await further instructions.",
    "earthquake": "🌎 Earthquake Alert! Drop, Cover, and Hold On!"
}

# To add new alert templates:
# - Add a new entry to ALERT_TEMPLATES above, e.g.,
#   "tornado": "🌪️ Tornado Alert! Seek shelter immediately."

# List of recipient phone numbers (in E.164 format)
# Note: Phone numbers must be added to your WhatsApp Business account's allowed recipient list
RECIPIENT_PHONE_NUMBERS = [
    "+919996178315"
]
