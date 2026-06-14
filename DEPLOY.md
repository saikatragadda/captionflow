# CaptionAI — Deployment Guide

## What this is
A Flask web app where users visit a URL, type their post idea, and get AI-generated captions instantly. No setup needed on their end.

---

## Deploy to Render (FREE — recommended, easier than Vercel for Flask)

### Step 1 — Push to GitHub
1. Go to github.com → New repository → call it `captionai`
2. In terminal:
```bash
cd ~/Downloads/caption_web
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/captionai.git
git push -u origin main
```

### Step 2 — Deploy on Render
1. Go to render.com → Sign up free
2. Click "New +" → "Web Service"
3. Connect your GitHub → select `captionai` repo
4. Settings:
   - **Environment:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
5. Click "Advanced" → "Add Environment Variable"
   - Key: `ANTHROPIC_API_KEY`
   - Value: your API key
6. Click "Create Web Service"

### Step 3 — You're live!
Render gives you a free URL like: `https://captionai.onrender.com`

That's the link you sell on Gumroad! 🎉

---

## Test locally first
```bash
cd caption_web
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
python app.py
```
Then open: http://localhost:5000

---

## How to sell access
1. Deploy the app → get your Render URL
2. Go to Gumroad → create product → price $19
3. In the "Thank you" message, paste your URL
4. Buyers pay → instantly get the link → use the tool

---

## Protecting your app (optional, later)
Right now anyone with the link can use it (you pay the API costs).
To limit usage, you can later add:
- A simple password page
- Email-based access tokens
- Rate limiting (max 20 generations per day per IP)

For now, keep it simple and start selling!
