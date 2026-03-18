# Deployment Guide: PINNs-UPC Calibration System

## 🎯 Quick Deployment (5 Minutes)

### Prerequisites
- GitHub account
- Vercel account (free)
- Railway account (free)

---

## 📦 Option 1: Vercel (Frontend) + Railway (Backend)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/pinns-upc-system.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Run `uvicorn api.main:app`
6. Copy your backend URL: `https://YOUR-APP.railway.app`

### Step 3: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel auto-detects Next.js
5. Add Environment Variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://YOUR-APP.railway.app` (from Step 2)
6. Click "Deploy"

### Step 4: Test Your Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Try the Scanner page
3. Check if it connects to the backend

---

## 📦 Option 2: Render (Full-Stack)

### Step 1: Deploy Backend

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - Name: `pinns-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Copy URL: `https://pinns-backend.onrender.com`

### Step 2: Deploy Frontend

1. In Render, click "New +" → "Static Site"
2. Connect same GitHub repository
3. Configure:
   - Name: `pinns-frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `.next`
4. Add Environment Variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://pinns-backend.onrender.com`
5. Click "Create Static Site"

---

## 📦 Option 3: Full Local Demo (For Hackathon Presentation)

If deployment is taking too long, run locally and share screen:

```bash
# Terminal 1: Start Backend
python api/main.py

# Terminal 2: Start Frontend
npm run dev

# Share: http://localhost:3000
```

---

## 🔧 Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Backend (Railway/Render will auto-detect)
```
PORT=8000
DATABASE_URL=sqlite:///./data/calibration.db
```

---

## 🚨 Common Issues

### Issue 1: CORS Error
**Problem:** Frontend can't connect to backend

**Solution:** Update `api/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app"],  # Add your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 2: Build Timeout
**Problem:** Vercel build takes too long

**Solution:** Increase timeout in `vercel.json`:
```json
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next",
      "config": {
        "maxDuration": 60
      }
    }
  ]
}
```

### Issue 3: Python Dependencies Fail
**Problem:** Railway can't install PyTorch

**Solution:** Use lighter dependencies or upgrade Railway plan

---

## 💰 Cost Breakdown

### Free Tier (Perfect for Hackathon)
- **Vercel:** Free (100GB bandwidth, unlimited projects)
- **Railway:** Free ($5 credit/month, enough for demo)
- **Total:** $0/month

### Production Tier
- **Vercel Pro:** $20/month (team features)
- **Railway Pro:** $20/month (more resources)
- **Total:** $40/month

---

## 🎥 For Hackathon Demo

### Best Approach:
1. **Deploy frontend to Vercel** (shows you can deploy)
2. **Run backend locally** (more reliable for live demo)
3. **Use ngrok** to expose local backend:
   ```bash
   ngrok http 8000
   # Copy ngrok URL to NEXT_PUBLIC_API_URL
   ```

### Why This Works:
- ✅ Frontend is live (judges can access)
- ✅ Backend is stable (no deployment issues during demo)
- ✅ Shows deployment capability
- ✅ Reliable for presentation

---

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed (Railway/Render)
- [ ] Backend URL copied
- [ ] Frontend deployed (Vercel)
- [ ] Environment variable set
- [ ] CORS configured
- [ ] Test Scanner page
- [ ] Test Fill Monitor
- [ ] Test PDF export
- [ ] Share live URL with judges

---

## 🔗 Useful Links

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **Render Docs:** https://render.com/docs
- **Next.js Deployment:** https://nextjs.org/docs/deployment

---

## 🆘 Need Help?

If deployment fails:
1. Check build logs in Vercel/Railway
2. Verify all files are committed to Git
3. Check environment variables are set
4. Test locally first: `npm run build`

**For hackathon:** Running locally is perfectly acceptable! Just share your screen.

---

*Good luck with your deployment! 🚀*
