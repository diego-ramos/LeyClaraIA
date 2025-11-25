# 🚂 Deploy to Railway - Quick Guide

## 📋 Prerequisites
- GitHub account with your code pushed
- Railway account (sign up at [railway.app](https://railway.app) - FREE)
- Your API keys: `GOOGLE_API_KEY` and `YOUTUBE_API_KEY`

---

## 🚀 Quick Deploy Steps

### 1️⃣ Create Railway Project
1. Go to [railway.app](https://railway.app) → **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your **TeLoExplico** repository

### 2️⃣ Deploy Backend
1. Railway auto-detects the project
2. Click **"Add variables"** and set:
   ```
   GOOGLE_API_KEY=your_key_here
   YOUTUBE_API_KEY=your_key_here
   CHROMA_DB_DIR=/app/chroma_db
   PYTHONUNBUFFERED=1
   ```
3. Go to **Settings** → **Root Directory** → Set to `backend`
4. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Deploy**
6. Go to **Settings** → **Networking** → **Generate Domain**
7. **Copy your backend URL** (e.g., `https://teloexplico-backend.railway.app`)

### 3️⃣ Add Persistent Storage
1. Click on backend service → **Settings** → **Volumes**
2. Click **"+ New Volume"**
3. **Mount Path**: `/app/chroma_db`
4. Click **Add**

### 4️⃣ Deploy Frontend
1. In your project, click **"+ New"** → **"GitHub Repo"**
2. Select the same repository
3. Click **"Add variables"** and set:
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```
   (Use the URL from step 2.7)
4. Go to **Settings** → **Root Directory** → Set to `frontend`
5. Click **Deploy**
6. Go to **Settings** → **Networking** → **Generate Domain**
7. **Your app is live!** 🎉

### 5️⃣ Update CORS (Important!)
Update `backend/main.py` to allow your Railway frontend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-url.railway.app"  # Add this
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then push to GitHub:
```bash
git add .
git commit -m "Update CORS for Railway"
git push
```

Railway will auto-redeploy! ✅

---

## 🎯 What You Get

✅ **Backend**: FastAPI running on Railway  
✅ **Frontend**: React app with Nginx  
✅ **Database**: ChromaDB with persistent storage  
✅ **Auto-deploy**: Every git push triggers new deployment  
✅ **Free tier**: $5/month credit (enough for small apps)  
✅ **HTTPS**: Automatic SSL certificates  

---

## 💡 Tips

- **Monitor usage**: Check Railway dashboard → "Usage" tab
- **View logs**: Click service → "Logs" tab for debugging
- **Custom domain**: Railway allows custom domains (Settings → Networking)
- **Environment variables**: Can be updated anytime without redeploying

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Check Logs tab, verify environment variables |
| Frontend can't connect | Verify `VITE_API_URL` matches backend URL |
| Files not persisting | Ensure Volume is mounted at `/app/chroma_db` |
| Out of credits | Check Usage tab, optimize or upgrade plan |

---

## 📊 Cost Estimate (Free Tier)

- **$5/month free credit**
- Backend: ~$3-4/month (512MB RAM)
- Frontend: ~$1-2/month (static hosting)
- **Total**: Fits within free tier for low-medium traffic ✅

---

## 🔄 Auto-Deploy Workflow

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main
```

Railway automatically:
1. Detects the push
2. Builds your Docker containers
3. Deploys new version
4. Zero downtime! 🚀

---

**Need help?** Check the full guide: `.agent/workflows/deploy_to_railway.md`
