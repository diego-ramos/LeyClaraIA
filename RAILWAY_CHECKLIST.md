# ✅ Railway Deployment Checklist

Use this checklist to track your deployment progress.

## 📦 Pre-Deployment

- [ ] Code is pushed to GitHub
- [ ] Have `GOOGLE_API_KEY` ready
- [ ] Have `YOUTUBE_API_KEY` ready
- [ ] Railway account created at [railway.app](https://railway.app)

---

## 🔧 Backend Deployment

- [ ] Created new Railway project
- [ ] Connected GitHub repository
- [ ] Set Root Directory to `backend`
- [ ] Added environment variables:
  - [ ] `GOOGLE_API_KEY`
  - [ ] `YOUTUBE_API_KEY`
  - [ ] `CHROMA_DB_DIR=/app/chroma_db`
  - [ ] `PYTHONUNBUFFERED=1`
- [ ] Set Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Deployed backend successfully
- [ ] Generated backend domain
- [ ] Copied backend URL: `_______________________________`
- [ ] Added persistent volume:
  - [ ] Mount path: `/app/chroma_db`

---

## 🎨 Frontend Deployment

- [ ] Added new service to Railway project
- [ ] Connected same GitHub repository
- [ ] Set Root Directory to `frontend`
- [ ] Added environment variable:
  - [ ] `VITE_API_URL=https://your-backend-url.railway.app`
- [ ] Deployed frontend successfully
- [ ] Generated frontend domain
- [ ] Frontend URL: `_______________________________`

---

## 🔗 CORS Configuration

- [ ] Updated `backend/main.py` with frontend URL in CORS
- [ ] Committed changes to Git
- [ ] Pushed to GitHub
- [ ] Railway auto-redeployed backend

---

## ✨ Testing

- [ ] Visited frontend URL
- [ ] Homepage loads correctly
- [ ] Can upload a PDF document
- [ ] Can ask questions in chat
- [ ] Chat returns answers
- [ ] YouTube videos appear in results
- [ ] Uploaded documents persist after refresh

---

## 🎉 Post-Deployment

- [ ] Bookmarked frontend URL
- [ ] Bookmarked Railway dashboard
- [ ] Shared app with friends/testers
- [ ] Monitored usage in Railway dashboard
- [ ] Set up custom domain (optional)

---

## 📊 Monitoring

Check these regularly:

- [ ] Railway Usage tab (stay within $5/month free tier)
- [ ] Backend logs for errors
- [ ] Frontend logs for errors
- [ ] Application performance

---

## 🆘 If Something Goes Wrong

1. **Check Logs**: Service → Logs tab
2. **Verify Variables**: Service → Variables tab
3. **Check Build**: Service → Deployments tab
4. **Test Locally**: Ensure it works with `docker-compose up`
5. **Ask for Help**: Railway Discord or documentation

---

**Deployment Date**: _______________  
**Backend URL**: _______________  
**Frontend URL**: _______________  
**Status**: 🟢 Live | 🟡 Testing | 🔴 Issues
