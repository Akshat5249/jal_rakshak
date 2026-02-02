# Deployment Guide for Jal Rakshak

## Can you deploy on Vercel?

**Short answer: Yes, but with considerations.**

### ✅ What Works Great on Vercel:
- **Frontend (React/Vite)**: Perfect fit! Deploys easily
- **Static assets**: Images, fonts, etc.

### ⚠️ Challenges:
- **Backend (Flask)**: Needs conversion to serverless functions
- **Large files**: Excel file (~25MB) and ML model may exceed Vercel's limits
- **Cold starts**: Serverless functions have cold start times

## Recommended Approach: Hybrid Deployment

### Option 1: Hybrid (Recommended) ⭐
- **Frontend**: Deploy on Vercel (free, fast CDN)
- **Backend**: Deploy on Railway/Render/Fly.io (better for large files)

### Option 2: Full Vercel
- Convert Flask to serverless functions
- May need to optimize/compress files
- More complex setup

---

## Quick Start: Deploy Frontend to Vercel

### Step 1: Prepare Frontend

The frontend is already configured! I've updated it to use environment variables.

### Step 2: Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Navigate to frontend directory
cd jal-spotter-dash

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name? jal-rakshak-dash
# - Directory? ./
# - Override settings? No
```

### Step 3: Set Environment Variable

After deployment, go to Vercel Dashboard:
1. Select your project
2. Go to Settings → Environment Variables
3. Add: `VITE_API_URL` = `https://your-backend-url.com`

### Step 4: Redeploy

```bash
vercel --prod
```

---

## Backend Deployment Options

### Option A: Railway (Easiest) 🚂

1. **Sign up**: [railway.app](https://railway.app)
2. **New Project** → Deploy from GitHub
3. **Select your repo**
4. **Add Service** → Empty Service
5. **Settings** → Add:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python app.py`
6. **Variables** → Add:
   - `PORT` = `5000` (Railway auto-assigns, but Flask needs this)

**Pros**: 
- Free tier available
- Handles large files well
- Auto-deploys on git push
- Simple setup

### Option B: Render 🎨

1. **Sign up**: [render.com](https://render.com)
2. **New** → Web Service
3. **Connect GitHub repo**
4. **Settings**:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python app.py`
   - Environment: Python 3

**Pros**: 
- Free tier (with limitations)
- Good for Python apps
- Auto-deploys

### Option C: Fly.io 🚀

1. **Install CLI**: `curl -L https://fly.io/install.sh | sh`
2. **Login**: `fly auth login`
3. **Launch**: `fly launch` (in backend directory)
4. **Deploy**: `fly deploy`

**Pros**: 
- Global edge deployment
- Good performance
- Free tier available

---

## Full Vercel Deployment (Advanced)

If you want everything on Vercel, you need to:

### 1. Convert Flask to Serverless Functions

Each Flask route becomes a file in `/api/`:

```
api/
├── dashboard-summary.py
├── symptom-reports.py
├── water-sources.py
├── alerts.py
├── chart-data.py
├── predict.py
└── send-alert.py
```

### 2. Handle Large Files

Options:
- **Compress Excel file** (use pandas to save as parquet)
- **Use external storage** (S3, Cloudinary)
- **Pre-process data** and store in database (Supabase)

### 3. Optimize Model Loading

- Cache model in serverless function memory
- Use lighter model format
- Consider edge functions for faster cold starts

---

## Current Setup Status

✅ **Frontend**: Ready for Vercel
- Environment variables configured
- Build script ready
- Vercel config created

⚠️ **Backend**: Needs deployment platform
- Flask app ready
- Choose Railway/Render/Fly.io

---

## Quick Deploy Commands

### Frontend (Vercel):
```bash
cd jal-spotter-dash
vercel
```

### Backend (Railway):
```bash
# After setting up Railway project
railway up
```

---

## Environment Variables Needed

### Frontend (.env or Vercel):
```
VITE_API_URL=https://your-backend.railway.app
```

### Backend (Railway/Render):
```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_IDS=["your_chat_id"]
```

---

## Testing After Deployment

1. **Frontend**: Visit your Vercel URL
2. **Backend**: Test API endpoint:
   ```bash
   curl https://your-backend.railway.app/api/dashboard-summary
   ```
3. **Integration**: Check if frontend can reach backend

---

## Troubleshooting

### CORS Issues
- Add your Vercel frontend URL to Flask CORS:
  ```python
  CORS(app, origins=["https://your-app.vercel.app"])
  ```

### File Not Found
- Ensure Excel file and model are in the correct path
- Check file paths in `_shared.py`

### Cold Start Timeouts
- Vercel functions: 10s (Hobby), 60s (Pro)
- Consider warming functions or using edge functions

---

## Cost Estimate

### Free Tier:
- **Vercel**: 100GB bandwidth/month (usually enough)
- **Railway**: $5 credit/month (usually enough for small apps)
- **Render**: 750 hours/month free

**Total**: ~$0-5/month for small-medium traffic

---

## Next Steps

1. **Choose deployment strategy** (Hybrid recommended)
2. **Deploy frontend to Vercel** (5 minutes)
3. **Deploy backend to Railway/Render** (10 minutes)
4. **Set environment variables**
5. **Test and enjoy!** 🎉

Need help with a specific step? Let me know!
