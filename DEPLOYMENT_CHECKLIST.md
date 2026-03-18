# Deployment Checklist

## ✅ Pre-Deployment Checklist

### Backend Setup
- [ ] Python 3.9+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Database initialized (`python scripts/seed_data.py`)
- [ ] PINN model trained (`python scripts/train_model.py`)
- [ ] Anomaly database seeded
- [ ] Backend starts without errors (`python api/main.py`)
- [ ] API docs accessible at http://localhost:8000/docs

### Frontend Setup
- [ ] Node.js 18+ installed
- [ ] All dependencies installed (`npm install`)
- [ ] Environment variables set (`.env.local`)
- [ ] Frontend builds successfully (`npm run build`)
- [ ] Frontend starts without errors (`npm run dev`)
- [ ] All pages load correctly

### Integration Testing
- [ ] Backend responds to health check
- [ ] Frontend can connect to backend
- [ ] UPC scanning works
- [ ] Fill prediction works
- [ ] Fill execution works
- [ ] Vision detection works
- [ ] Health monitoring works
- [ ] SPC monitoring works
- [ ] Anomaly database works
- [ ] All API endpoints tested (`python test_integration.py`)

### Documentation
- [ ] README.md updated
- [ ] API documentation complete
- [ ] Integration guide reviewed
- [ ] Quick reference available
- [ ] Troubleshooting guide ready

## 🚀 Deployment Steps

### Option 1: Local Development
```bash
# 1. Start backend
python api/main.py

# 2. Start frontend (new terminal)
npm run dev

# 3. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Option 2: Automated Startup
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### Option 3: Production Deployment

#### Backend (Docker)
```bash
# Build image
docker build -t pinns-upc-backend -f Dockerfile.backend .

# Run container
docker run -d -p 8000:8000 --name backend pinns-upc-backend

# Check logs
docker logs backend
```

#### Frontend (Vercel)
```bash
# Build
npm run build

# Deploy
vercel deploy --prod

# Or use Vercel GitHub integration
```

## 🧪 Testing Checklist

### Manual Testing
- [ ] Open http://localhost:3000
- [ ] Dashboard loads with metrics
- [ ] Scanner page: Enter UPC 1234567890002
- [ ] Product loads with properties
- [ ] Calibration profile displays
- [ ] Navigate to Fill Monitor
- [ ] Adjust parameters with sliders
- [ ] Click "Predict Fill"
- [ ] Prediction displays with confidence
- [ ] Enter actual values
- [ ] Enable vision detection
- [ ] Click "Log Fill Result"
- [ ] Vision results display
- [ ] Navigate to Equipment Health
- [ ] Component health scores display
- [ ] Navigate to SPC Control
- [ ] Control chart displays (after 20+ fills)
- [ ] Navigate to Anomaly Database
- [ ] Search for solutions works
- [ ] Database statistics display

### Automated Testing
```bash
# Backend integration test
python test_integration.py

# Frontend lint
npm run lint

# Frontend build test
npm run build
```

### Performance Testing
- [ ] Page load time < 2 seconds
- [ ] API response time < 100ms
- [ ] UI animations smooth (60 FPS)
- [ ] No memory leaks
- [ ] No console errors

## 📊 Monitoring

### Backend Monitoring
```bash
# Check backend logs
tail -f backend.log

# Monitor API requests
# Use FastAPI built-in logging

# Check database size
ls -lh data/calibration.db
```

### Frontend Monitoring
```bash
# Check build size
npm run build
# Look for bundle size warnings

# Monitor browser console
# Open DevTools → Console

# Check network requests
# Open DevTools → Network
```

## 🐛 Common Issues & Solutions

### Issue: Backend won't start
```bash
# Solution 1: Check Python version
python --version  # Should be 3.9+

# Solution 2: Reinstall dependencies
pip install --upgrade -r requirements.txt

# Solution 3: Check port availability
netstat -an | grep 8000
# If in use, kill process or change port
```

### Issue: Frontend won't start
```bash
# Solution 1: Check Node version
node --version  # Should be 18+

# Solution 2: Clear cache
rm -rf node_modules package-lock.json .next
npm install

# Solution 3: Check port availability
netstat -an | grep 3000
```

### Issue: CORS errors
```bash
# Solution: Check backend CORS settings
# In api/main.py, verify:
allow_origins=["http://localhost:3000"]

# Also check .env.local:
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Issue: API connection timeout
```bash
# Solution 1: Ensure backend is running
curl http://localhost:8000/

# Solution 2: Check firewall
# Allow ports 3000 and 8000

# Solution 3: Check network
ping localhost
```

### Issue: Database not found
```bash
# Solution: Initialize database
python scripts/seed_data.py

# Check if file exists
ls -la data/calibration.db
```

### Issue: Model not trained
```bash
# Solution: Train model
python scripts/train_model.py

# Check if model exists
ls -la models/pinn_model.pth
```

## 📦 Production Deployment

### Environment Variables

#### Backend (.env)
```bash
DATABASE_PATH=./data/calibration.db
MODEL_PATH=./models/pinn_model.pth
LOG_LEVEL=INFO
```

#### Frontend (.env.production)
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Security Checklist
- [ ] API authentication implemented
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Rate limiting enabled
- [ ] Error messages don't leak sensitive info

### Performance Optimization
- [ ] Frontend code splitting
- [ ] Image optimization
- [ ] API response caching
- [ ] Database indexing
- [ ] Gzip compression
- [ ] CDN for static assets

### Backup Strategy
- [ ] Database backup schedule
- [ ] Model backup
- [ ] Configuration backup
- [ ] Automated backup testing

## 📈 Post-Deployment

### Monitoring Setup
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (New Relic)
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Log aggregation (Loggly)

### Analytics
- [ ] User analytics (Google Analytics)
- [ ] API usage tracking
- [ ] Performance metrics
- [ ] Error rate monitoring

### Maintenance
- [ ] Regular dependency updates
- [ ] Security patches
- [ ] Database optimization
- [ ] Model retraining schedule

## 🎯 Success Criteria

### Technical
- [ ] All tests passing
- [ ] No console errors
- [ ] API response time < 100ms
- [ ] Page load time < 2s
- [ ] 99.9% uptime

### Functional
- [ ] All features working
- [ ] Data persists correctly
- [ ] Real-time updates work
- [ ] Error handling works
- [ ] User feedback clear

### User Experience
- [ ] UI responsive on all devices
- [ ] Smooth animations
- [ ] Clear error messages
- [ ] Intuitive navigation
- [ ] Fast interactions

## 📞 Support Contacts

### Technical Issues
- Backend: Check `api/main.py` logs
- Frontend: Check browser console
- Database: Check `data/` directory
- Model: Check `models/` directory

### Documentation
- Integration: `FULLSTACK_INTEGRATION.md`
- API: http://localhost:8000/docs
- Quick Ref: `QUICK_REFERENCE.md`
- Troubleshooting: This file

## 🎉 Launch Checklist

### Final Checks
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Demo prepared
- [ ] Backup created
- [ ] Monitoring active
- [ ] Support ready

### Go Live
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Verify deployment
- [ ] Test production
- [ ] Announce launch
- [ ] Monitor closely

### Post-Launch
- [ ] Monitor errors
- [ ] Track performance
- [ ] Gather feedback
- [ ] Plan improvements
- [ ] Celebrate! 🎊

---

**Ready for deployment!** 🚀

Last updated: March 2026
