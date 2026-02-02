# Vercel Deployment Guide for Jal Rakshak

## Overview

Yes, you can deploy this project on Vercel! However, it requires some modifications:

### ✅ What Works on Vercel:
- **Frontend (React/Vite)**: Deploys perfectly
- **Python Serverless Functions**: Vercel supports Python functions

### ⚠️ What Needs Adaptation:
- **Flask App**: Must be converted to serverless functions
- **Large Files**: Excel file and ML model need to be included in deployment
- **Global State**: Data/model loading needs to be optimized for serverless

## Deployment Strategy

### Option 1: Full Vercel Deployment (Recommended)
- Frontend: Static site on Vercel
- Backend: Python serverless functions on Vercel
- Files: Excel and model included in repo

### Option 2: Hybrid Deployment
- Frontend: Vercel
- Backend: Separate service (Railway, Render, Fly.io, etc.)

## Step-by-Step: Full Vercel Deployment

### Prerequisites
1. Vercel account (free tier works)
2. Git repository (GitHub, GitLab, or Bitbucket)
3. Node.js and Python installed locally

### Step 1: Prepare Project Structure

The project structure needs to be:
```
jal-rakshak-master/
├── api/                    # Serverless functions (new)
│   ├── dashboard-summary.py
│   ├── symptom-reports.py
│   ├── water-sources.py
│   ├── alerts.py
│   ├── chart-data.py
│   ├── predict.py
│   └── send-alert.py
├── jal-spotter-dash/       # Frontend
│   └── ...
├── data/                   # Data files (new)
│   ├── final_nhs-wq_pre_2023_compressed.xlsx
│   └── model.joblib
├── vercel.json            # Vercel config
└── requirements.txt       # Python dependencies
```

### Step 2: Create Vercel Configuration

See `vercel.json` (will be created)

### Step 3: Convert Flask Routes to Serverless Functions

Each Flask route becomes a separate Python file in `/api/`

### Step 4: Update Frontend API URLs

Change hardcoded URLs to use environment variables

### Step 5: Deploy

```bash
npm i -g vercel
vercel login
vercel
```

## File Size Considerations

⚠️ **Important**: Vercel has limits:
- Serverless function size: 50MB (uncompressed)
- Total deployment size: 100MB

Your Excel file and model might be large. Options:
1. Compress files
2. Use external storage (S3, Cloudinary)
3. Pre-process data and store in database

## Alternative: Hybrid Deployment

If files are too large, consider:
- **Frontend**: Deploy on Vercel
- **Backend**: Deploy on Railway/Render/Fly.io (better for large files)
- **Database**: Use Supabase/PlanetScale for data storage

## Next Steps

I'll create the necessary files for you. Choose:
1. **Full Vercel** - I'll convert everything to serverless functions
2. **Hybrid** - I'll set up frontend for Vercel + guide for backend elsewhere
