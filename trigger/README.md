# Telegram Alert System

This directory contains the Telegram alert system for Jal Rakshak.

## Quick Setup

### 1. Set Up Your Bot Token

**Option A: Using Environment Variables (Recommended)**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_IDS='["your_chat_id"]'
```

**Option B: Using config.py (Local Development)**
```bash
cp config.example.py config.py
# Edit config.py and add your token
```

### 2. Get Your Chat ID

```bash
python3 get_chat_id.py
```

### 3. Test the Setup

```bash
python3 test_and_get_chat_id.py
```

## Files

- `config.example.py` - Template configuration (safe to commit)
- `config.py` - Your actual config (NOT in git, use env vars or create locally)
- `telegram_alert.py` - Main alert functions
- `get_chat_id.py` - Helper to get your Telegram chat ID
- `test_and_get_chat_id.py` - Test script
- `SECURITY_SETUP.md` - Detailed security instructions

## Important Notes

⚠️ **NEVER commit `config.py` with real tokens!**

The old token that was exposed should be revoked. See `SECURITY_SETUP.md` for details.
