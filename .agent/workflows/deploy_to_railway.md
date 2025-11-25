---
description: How to deploy the TeLoExplico application to Railway
---

# Deploy TeLoExplico to Railway

This guide will walk you through deploying your full-stack application (FastAPI backend + React frontend) to Railway.

## Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Railway Account**: Sign up at [railway.app](https://railway.app) (free, no credit card required)
3. **API Keys**: Have your `GOOGLE_API_KEY` and `YOUTUBE_API_KEY` ready

---

## Step 1: Push Your Code to GitHub

If you haven't already, push your code to GitHub:

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

---

## Step 2: Create a New Railway Project

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account
5. Select your **TeLoExplico** repository

---

## Step 3: Add PostgreSQL Database (Optional)

If your app needs PostgreSQL in the future:

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically create a database and set the `DATABASE_URL` environment variable

> **Note**: Currently, your app uses ChromaDB (file-based), so PostgreSQL is optional.

---

## Step 4: Deploy the Backend

### 4.1 Create Backend Service

1. In your Railway project, click **"+ New"** → **"GitHub Repo"**
2. Select your repository
3. Railway will auto-detect the Dockerfile

### 4.2 Configure Backend Environment Variables

1. Click on your backend service
2. Go to **"Variables"** tab
3. Add the following variables:

```
GOOGLE_API_KEY=your_actual_google_api_key
YOUTUBE_API_KEY=your_actual_youtube_api_key
CHROMA_DB_DIR=/app/chroma_db
PYTHONUNBUFFERED=1
```

### 4.3 Configure Backend Settings

1. Go to **"Settings"** tab
2. **Root Directory**: Set to `backend`
3. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Click **"Deploy"**

### 4.4 Get Backend URL

1. Once deployed, go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. Copy the URL (e.g., `https://your-backend.railway.app`)

---

## Step 5: Deploy the Frontend

### 5.1 Create Frontend Service

1. In your Railway project, click **"+ New"** → **"GitHub Repo"**
2. Select the same repository again

### 5.2 Configure Frontend Settings

1. Click on the new service
2. Go to **"Settings"** tab
3. **Root Directory**: Set to `frontend`
4. **Build Command**: `npm install && npm run build`
5. **Start Command**: Leave empty (will use Dockerfile)

### 5.3 Update Frontend to Use Backend URL

**IMPORTANT**: You need to update your frontend to point to the Railway backend URL.

In `frontend/src` (wherever you make API calls), replace `http://localhost:8000` with your Railway backend URL.

Example in your API configuration file:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-backend.railway.app';
```

### 5.4 Add Frontend Environment Variable

1. Go to **"Variables"** tab
2. Add:
```
VITE_API_URL=https://your-backend.railway.app
```

### 5.5 Generate Frontend Domain

1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. Your app will be live at `https://your-frontend.railway.app`

---

## Step 6: Update CORS Settings

Update your backend `main.py` to allow your Railway frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.railway.app"  # Add your Railway frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push:
```bash
git add .
git commit -m "Update CORS for Railway deployment"
git push origin main
```

Railway will automatically redeploy.

---

## Step 7: Add Persistent Storage (Important!)

Since your app uses ChromaDB (file-based database), you need persistent storage:

1. Click on your **backend service**
2. Go to **"Settings"** → **"Volumes"**
3. Click **"+ New Volume"**
4. **Mount Path**: `/app/chroma_db`
5. Click **"Add"**

This ensures your vector database persists across deployments.

---

## Step 8: Monitor Your Deployment

1. Go to **"Deployments"** tab to see build logs
2. Check **"Logs"** tab for runtime logs
3. If there are errors, check the logs and fix accordingly

---

## Step 9: Test Your Application

1. Visit your frontend URL: `https://your-frontend.railway.app`
2. Upload a document
3. Try the chat functionality
4. Verify everything works!

---

## Troubleshooting

### Backend won't start
- Check **"Logs"** tab for errors
- Verify all environment variables are set correctly
- Ensure `requirements.txt` has all dependencies

### Frontend can't connect to backend
- Verify `VITE_API_URL` is set correctly
- Check CORS settings in `main.py`
- Ensure backend is deployed and running

### Files not persisting
- Make sure you added a Volume to the backend service
- Verify the mount path is `/app/chroma_db`

### Out of credits
- Railway gives $5/month free
- Monitor usage in **"Usage"** tab
- Optimize by reducing replicas or instance size if needed

---

## Cost Optimization Tips

1. **Use a single service**: Combine frontend and backend if needed
2. **Set sleep mode**: Railway can sleep inactive services
3. **Monitor usage**: Check the "Usage" tab regularly
4. **Remove unused services**: Delete test deployments

---

## Updating Your App

Railway auto-deploys on every push to your GitHub repo:

```bash
# Make changes
git add .
git commit -m "Your changes"
git push origin main
```

Railway will automatically rebuild and redeploy! 🚀

---

## Alternative: Deploy Both Services from One Repo

If you want to deploy both services from a single Railway project:

1. Create **two services** in the same project
2. Point both to the same GitHub repo
3. Set different **Root Directory** for each:
   - Backend: `backend`
   - Frontend: `frontend`

This keeps everything organized in one Railway project.

---

## Summary

✅ Backend deployed with persistent storage  
✅ Frontend deployed and connected to backend  
✅ Environment variables configured  
✅ Auto-deploy on git push enabled  
✅ Custom domains generated  

Your app is now live on Railway! 🎉
