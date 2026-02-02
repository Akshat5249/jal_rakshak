#!/usr/bin/env python3
"""
Interactive script to test Telegram bot and get your chat ID.
"""

import requests
import sys
from config import TELEGRAM_BOT_TOKEN

def get_bot_info():
    """Get bot information"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_info = data.get("result", {})
                return bot_info.get("username"), bot_info.get("first_name")
    except Exception as e:
        print(f"Error: {e}")
    return None, None

def get_chat_ids():
    """Get all chat IDs from recent updates"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                updates = data.get("result", [])
                chat_ids = {}
                for update in updates:
                    if "message" in update:
                        chat = update["message"].get("chat", {})
                        chat_id = str(chat.get("id"))
                        if chat_id not in chat_ids:
                            chat_ids[chat_id] = {
                                "first_name": chat.get("first_name", "Unknown"),
                                "username": chat.get("username", ""),
                                "type": chat.get("type", "unknown")
                            }
                return chat_ids
    except Exception as e:
        print(f"Error: {e}")
    return {}

def test_send_message(chat_id, message="🧪 Test message from Jal Rakshak"):
    """Test sending a message to a chat ID"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("ok"):
                return True, "Success!"
            else:
                return False, result.get("description", "Unknown error")
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    print("=" * 60)
    print("Telegram Bot Setup & Test")
    print("=" * 60)
    print()
    
    # Get bot info
    bot_username, bot_name = get_bot_info()
    if not bot_username:
        print("❌ Error: Invalid bot token or cannot connect to Telegram API")
        sys.exit(1)
    
    print(f"✅ Bot found: @{bot_username} ({bot_name})")
    print()
    
    # Get chat IDs
    print("📥 Checking for chat IDs...")
    chat_ids = get_chat_ids()
    
    if not chat_ids:
        print("❌ No chat IDs found!")
        print()
        print("📋 To fix this:")
        print(f"   1. Open Telegram and search for: @{bot_username}")
        print("   2. Click 'Start' or send any message to the bot")
        print("   3. Run this script again")
        print()
        sys.exit(1)
    
    print(f"✅ Found {len(chat_ids)} chat ID(s):")
    print()
    
    working_chat_ids = []
    for chat_id, info in chat_ids.items():
        print(f"Chat ID: {chat_id}")
        print(f"  Name: {info['first_name']}")
        if info['username']:
            print(f"  Username: @{info['username']}")
        print(f"  Type: {info['type']}")
        
        # Test sending a message
        print(f"  Testing... ", end="", flush=True)
        success, message = test_send_message(chat_id)
        if success:
            print("✅ Working!")
            working_chat_ids.append(chat_id)
        else:
            print(f"❌ Failed: {message}")
        print()
    
    if working_chat_ids:
        print("=" * 60)
        print("✅ Working Chat IDs (add these to config.py):")
        print("=" * 60)
        print("TELEGRAM_CHAT_IDS = [")
        for chat_id in working_chat_ids:
            print(f'    "{chat_id}",')
        print("]")
        print()
    else:
        print("❌ No working chat IDs found. Make sure you've started a conversation with the bot!")
