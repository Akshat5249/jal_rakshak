# Security Setup Guide

## ⚠️ IMPORTANT: Your Telegram Bot Token Was Exposed

If your bot token was committed to GitHub, you should:

1. **Revoke the old token**:
   - Open Telegram and message @BotFather
   - Send `/revoke` or `/revoke_token`
   - Select your bot
   - This will invalidate the old token

2. **Create a new token**:
   - Message @BotFather
   - Send `/newbot` or `/token`
   - Get your new token

3. **Update your configuration** (see below)

## Setting Up Your Telegram Bot Securely

### Option 1: Using Environment Variables (Recommended)

1. **Create a `.env` file** in the `trigger/` directory:
   ```bash
   cd trigger
   touch .env
   ```

2. **Add your credentials** to `.env`:
   ```bash
   TELEGRAM_BOT_TOKEN=your_new_token_here
   TELEGRAM_CHAT_IDS=["1456097608"]
   ```

3. **Load environment variables** before running scripts:
   ```bash
   # On macOS/Linux
   export TELEGRAM_BOT_TOKEN="your_token"
   export TELEGRAM_CHAT_IDS='["1456097608"]'
   
   # Or use a .env file with python-dotenv
   ```

### Option 2: Using config.py (Local Development Only)

1. **Copy the example file**:
   ```bash
   cd trigger
   cp config.example.py config.py
   ```

2. **Edit config.py** and add your token:
   ```python
   TELEGRAM_BOT_TOKEN = "your_new_token_here"
   TELEGRAM_CHAT_IDS = ["1456097608"]
   ```

3. **⚠️ NEVER commit config.py to git!** It's already in `.gitignore`

## Verifying Your Setup

Run the test script:
```bash
cd trigger
python3 test_and_get_chat_id.py
```

This will:
- Verify your bot token is valid
- Show your chat IDs
- Test sending a message

## For Production/Deployment

Always use environment variables in production:

### Railway/Render:
- Add environment variables in the dashboard:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_IDS`

### Vercel:
- Add environment variables in project settings
- They'll be available to serverless functions

### Local Development:
- Use `.env` file (make sure it's in `.gitignore`)
- Or set environment variables in your shell

## Security Best Practices

✅ **DO:**
- Use environment variables
- Keep `.env` files in `.gitignore`
- Use `config.example.py` as a template
- Revoke tokens if exposed

❌ **DON'T:**
- Commit `config.py` with real tokens
- Share tokens in chat/messages
- Use the same token in multiple places
- Leave tokens in code comments

## Removing Old Token from Git History

If you want to completely remove the exposed token from git history:

```bash
# WARNING: This rewrites git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch trigger/config.py" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (be careful!)
git push origin --force --all
```

**Note**: This is destructive and will change commit history. Only do this if you're the only one using the repo, or coordinate with your team.
