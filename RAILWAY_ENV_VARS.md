# Railway Environment Variables Configuration

## Backend Service Variables

Add these in Railway Dashboard → Backend Service → Variables tab:

```
GOOGLE_API_KEY=your_google_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
CHROMA_DB_DIR=/app/chroma_db
PYTHONUNBUFFERED=1
```

## Frontend Service Variables

Add these in Railway Dashboard → Frontend Service → Variables tab:

```
VITE_API_URL=https://your-backend-service.railway.app
```

**Important**: Replace `your-backend-service.railway.app` with your actual backend URL from Railway.

---

## How to Get Your Backend URL

1. Deploy your backend service first
2. Go to Backend Service → Settings → Networking
3. Click "Generate Domain"
4. Copy the generated URL (e.g., `https://leyclara-ia-backend-production.up.railway.app`)
5. Use this URL in the frontend's `VITE_API_URL` variable

---

## Notes

- Railway automatically provides `PORT` variable (don't set it manually)
- Variables can be updated anytime in the Railway dashboard
- After updating variables, Railway will automatically redeploy the service
- Keep your API keys secure and never commit them to Git
