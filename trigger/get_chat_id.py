#!/usr/bin/env python3
"""
Helper script to get your Telegram chat ID.
Make sure you've started a conversation with your bot first!
"""

import requests
import sys
from config import TELEGRAM_BOT_TOKEN

def get_chat_ids():
    """
    Get all chat IDs that have sent messages to your bot.
    """
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Error: Please set TELEGRAM_BOT_TOKEN in config.py first!")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                updates = data.get("result", [])
                if not updates:
                    print("📭 No messages found. Please send a message to your bot first!")
                    print(f"   Search for your bot on Telegram and send it a message.")
                    return
                
                print("✅ Found chat IDs:")
                print("-" * 50)
                chat_ids = set()
                for update in updates:
                    if "message" in update:
                        chat = update["message"].get("chat", {})
                        chat_id = str(chat.get("id"))
                        chat_type = chat.get("type", "unknown")
                        first_name = chat.get("first_name", "Unknown")
                        username = chat.get("username", "No username")
                        
                        if chat_id not in chat_ids:
                            chat_ids.add(chat_id)
                            print(f"Chat ID: {chat_id}")
                            print(f"  Name: {first_name}")
                            print(f"  Username: @{username}" if username != "No username" else "  Username: (none)")
                            print(f"  Type: {chat_type}")
                            print()
                
                print("-" * 50)
                print("\n📋 Add these to TELEGRAM_CHAT_IDS in config.py:")
                print("TELEGRAM_CHAT_IDS = [")
                for chat_id in sorted(chat_ids):
                    print(f'    "{chat_id}",')
                print("]")
            else:
                print(f"❌ Error: {data.get('description', 'Unknown error')}")
                if "Unauthorized" in str(data.get('description', '')):
                    print("   Your bot token is invalid. Check config.py")
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    get_chat_ids()
