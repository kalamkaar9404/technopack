# Complete Setup & Launch Guide

## 🎯 Overview

This guide will take you from zero to a fully running PINNs-UPC Calibration System in about 15-20 minutes.

**What you'll get:**
- Backend API running on http://localhost:8000
- Frontend UI running on http://localhost:3000
- All features working (PINN, Vision, Health, SPC, Anomaly DB)
- Sample data loaded and ready to use

---

## 📋 Prerequisites

### Required Software

1. **Python 3.9 or higher**
   ```bash
   # Check version
   python --version
   # or
   python3 --version
   ```
   
   If not installed:
   - Windows: Download from https://www.python.org/downloads/
   - Mac: `brew install python@3.11`
   - Linux: `sudo apt install python3.11`

2. **Node.js 18 or higher**
   ```bash
   # Check version
   node --version
   ```
   
   If not installed:
   - Download from https://nodejs.org/ (LTS version)
   - Or use nvm: `nvm install 18`

3. **pip (Python package manager)**
   ```bash
   # Check if installed
   pip --version
   ```
   
   Usually comes with Python. If not:
   ```bash
   python -m ensurepip --upgrade
   ```

4. **npm (Node package manager)**
   ```bash
   # Check if installed
   npm --version
   ```
   
   Comes with Node.js installation.

### Optional but Recommended

- **Git** (for version control)
- **VS Code** (for editing)
- **Postman** (for API testing)

---

## 🚀 Step-by-Step Setup

### Step 1: Navigate to Project Directory

```bash
# Open terminal/command prompt
# Navigate to your project folder
cd path/to/pinns-upc-calibration
```

### Step 2: Install Python Dependencies

```bash
# Install all Python packages
pip install -r requirements.txt

# This will install:
# - torch (PyTorch for PINN model)
# - fastapi (Backend API)
# - uvicorn (API server)
# - sqlalchemy (Database)
# - opencv-python (Computer vision)
# - streamlit (Alternative UI)
# - And more...

# Wait for installation to complete (2-5 minutes)
```

**If you get errors:**
```bash
# Try with --upgrade flag
pip install --upgrade -r requirements.txt

# Or use pip3
pip3 install -r requirements.txt

# On Windows, you might need:
python -m pip install -r requirements.txt
```

### Step 3: Install Node.js Dependencies

```bash
# Install all Node packages
npm install

# This will install:
# - next (Next.js framework)
# - react (UI library)
# - typescript (Type safety)
# - tailwindcss (Styling)
# - And more...

# Wait for installation to complete (3-7 minutes)
```

**If you get errors:**
```bash
# Clear cache and retry
rm -rf node_modules package-lock.json
npm install

# Or use yarn
yarn install

# Or use pnpm
pnpm install
```

### Step 4: Initialize Database & Train Model

```bash
# Run the setup script
python setup.py

# This will:
# 1. Create data directories
# 2. Seed database with 10 sample products
# 3. Initialize anomaly database
# 4. Train initial PINN model (5-10 minutes)

# You'll see progress messages like:
# ✓ Directories created
# ✓ Database seeded
# ✓ Anomaly database initialized
# ✓ Model training started...
# ✓ Model training completed
```

**Expected output:**
```
╔══════════════════════════════════════════════════════════╗
║   PINNs-UPC Calibration System - Quick Setup            ║
║   Technopack Hackathon 2026                              ║
╚══════════════════════════════════════════════════════════╝

✓ Python version: 3.11.0
✓ Directories created
✓ Installing dependencies
✓ Seeding database with sample products
✓ Anomaly database initialized
✓ Training initial PINN model (this may take 5-10 minutes)
✓ Model training completed

╔══════════════════════════════════════════════════════════╗
║   Setup Complete! 🎉                                     ║
╚══════════════════════════════════════════════════════════╝

To start the application:
    streamlit run src/ui/app.py

Sample UPC codes to try:
    1234567890001 - Water
    1234567890002 - Vegetable Oil
    1234567890003 - Honey
```

### Step 5: Verify Setup

```bash
# Check if database was created
ls -la data/calibration.db
# Should show a file with size > 0

# Check if model was trained
ls -la models/pinn_model.pth
# Should show a file with size > 0

# Check if anomaly database exists
ls -la data/anomaly_db.json
# Should show a file with size > 0
```

---

## 🎬 Launch Application

### Option 1: Automated Launch (Recommended)

**Windows:**
```bash
# Double-click start.bat
# Or run in terminal:
start.bat
```

**Linux/Mac:**
```bash
# Make script executable (first time only)
chmod +x start.sh

# Run script
./start.sh
```

**What happens:**
1. Checks if dependencies are installed
2. Starts backend API on port 8000
3. Waits 3 seconds
4. Starts frontend on port 3000
5. Opens two terminal windows

**You'll see:**
```
======================================
  PINNs-UPC Calibration System
  Starting Full Stack Application
======================================

Checking Python dependencies...
✓ Dependencies installed

Checking Node.js dependencies...
✓ Dependencies installed

Starting Python backend on http://localhost:8000...
✓ Backend started

Starting Next.js frontend on http://localhost:3000...
✓ Frontend started

======================================
  Application Started Successfully!
======================================

Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs

Press Ctrl+C to stop both servers
```

### Option 2: Manual Launch

**Terminal 1 - Backend:**
```bash
# Start FastAPI backend
python api/main.py

# You should see:
# INFO:     Started server process
# INFO:     Waiting for application startup.
# ✓ Backend initialized successfully
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
# Start Next.js frontend
npm run dev

# You should see:
#   ▲ Next.js 16.1.6
#   - Local:        http://localhost:3000
#   - Network:      http://192.168.1.x:3000
#
# ✓ Ready in 2.3s
```

---

## ✅ Verify Everything Works

### Step 1: Check Backend

Open browser and go to:
```
http://localhost:8000/docs
```

You should see:
- Swagger UI with API documentation
- List of all endpoints
- Try the "GET /" endpoint - should return `{"status": "online"}`

### Step 2: Check Frontend

Open browser and go to:
```
http://localhost:3000
```

You should see:
- Dashboard with metrics
- Sidebar navigation
- Beautiful UI with charts

### Step 3: Test Integration

Run the integration test:
```bash
# In a new terminal
python test_integration.py
```

Expected output:
```
======================================================================
  PINNs-UPC Calibration System - Integration Test
======================================================================

1. Testing health check...
   ✓ Backend is online: {'status': 'online', ...}

2. Testing get products...
   ✓ Found 10 products
     - Water (1234567890001)
     - Vegetable Oil (1234567890002)
     - Honey (1234567890003)

3. Testing UPC scan...
   ✓ Scanned: Vegetable Oil
     Viscosity: 0.065 Pa·s
     Profile: 1.5s, 50.0 PSI

4. Testing fill prediction...
   ✓ Predicted volume: 498.50 mL
     Predicted time: 2.10 s
     Confidence: 95.0%

5. Testing fill execution...
   ✓ Executed fill: 498.50 mL
     Anomaly detected: False
     📷 Vision: 498.50 mL (confidence: 92%)

6. Testing health monitoring...
   ✓ Component health:
     - Nozzle: 100.0%
     - Valve: 100.0%
     - Pump: 100.0%
     - Sensor: 100.0%

7. Testing SPC monitoring...
   ✓ SPC status:
     Control chart: insufficient_data
     Cpk: insufficient_data

8. Testing anomaly database...
   ✓ Anomaly database:
     Total anomalies: 5
     Average effectiveness: 90%
     Issue types: foam_overflow, clog, drift, underfill, overfill

======================================================================
  Test Results
======================================================================

Passed: 8/8

✓ All tests passed! Integration is working correctly.
```

---

## 🎮 Using the Application

### 1. Dashboard (Home Page)

Navigate to: http://localhost:3000

**What you'll see:**
- System metrics (temperature, pressure, flow rate, uptime)
- Real-time charts
- System health summary
- Calibration status

### 2. Scanner Page

Navigate to: http://localhost:3000/scanner

**Try it:**
1. Enter UPC code: `1234567890002`
2. Click "Scan" button
3. See product information load
4. View calibration profile
5. Click "Start Fill Operation"

**Sample UPC codes:**
- `1234567890001` - Water (thin liquid)
- `1234567890002` - Vegetable Oil (medium)
- `1234567890003` - Honey (thick liquid)
- `1234567890004` - Milk
- `1234567890005` - Soda (carbonated)

### 3. Fill Monitor Page

Navigate to: http://localhost:3000/fill-monitor

**Try it:**
1. Adjust parameters with sliders
2. Click "Predict Fill"
3. See AI prediction with confidence
4. Enter actual values
5. Enable vision detection
6. Click "Log Fill Result"
7. See vision verification results

### 4. Equipment Health Page

Navigate to: http://localhost:3000/equipment-health

**What you'll see:**
- Component health scores (nozzle, valve, pump, sensor)
- Active alerts (if any)
- Maintenance schedule
- Accuracy trend charts

### 5. SPC Control Chart Page

Navigate to: http://localhost:3000/spc-control

**What you'll see:**
- Control chart (after 20+ fills)
- Rule violation alerts
- Process capability metrics (Cp, Cpk)

### 6. Anomaly Database Page

Navigate to: http://localhost:3000/anomaly-database

**Try it:**
1. Select issue type: "foam_overflow"
2. Click "Search Solutions"
3. See community solutions
4. View effectiveness and upvotes

---

## 🔧 Troubleshooting

### Problem: Backend won't start

**Error: "Port 8000 already in use"**
```bash
# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

**Error: "Module not found"**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Error: "Database not found"**
```bash
# Re-run setup
python setup.py
```

### Problem: Frontend won't start

**Error: "Port 3000 already in use"**
```bash
# Kill process using port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:3000 | xargs kill -9

# Or use different port:
npm run dev -- -p 3001
```

**Error: "Module not found"**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json .next
npm install
```

### Problem: CORS errors in browser

**Solution:**
1. Make sure backend is running
2. Check `.env.local` file exists with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
3. Restart frontend

### Problem: API connection timeout

**Solution:**
1. Check backend is running: http://localhost:8000
2. Check firewall isn't blocking ports
3. Try accessing API docs: http://localhost:8000/docs

### Problem: Model training takes too long

**Solution:**
```bash
# Skip training for now, use pre-trained model
# Or reduce training epochs in config/config.yaml:
training:
  epochs: 100  # Reduce from 1000 to 100
```

---

## 📊 Quick Test Workflow

### Complete Fill Operation Test

1. **Start both servers** (backend + frontend)

2. **Open frontend**: http://localhost:3000

3. **Go to Scanner page**
   - Enter UPC: `1234567890002`
   - Click "Scan"
   - Verify product loads

4. **Go to Fill Monitor page**
   - Adjust sliders:
     - Valve Timing: 1.5s
     - Pressure: 50 PSI
     - Nozzle Diameter: 5.0mm
     - Target Volume: 500mL
   - Click "Predict Fill"
   - Verify prediction shows

5. **Execute fill**
   - Enter Actual Volume: 498.5
   - Enter Actual Time: 2.1
   - Check "Vision Detection"
   - Click "Log Fill Result"
   - Verify success message

6. **Check monitoring**
   - Go to Equipment Health page
   - Verify component health shows
   - Go to SPC Control page
   - Note: Need 20+ fills for charts

7. **Search anomalies**
   - Go to Anomaly Database page
   - Select "foam_overflow"
   - Click "Search Solutions"
   - Verify solutions display

---

## 🎯 Success Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Python dependencies installed
- [ ] Node.js dependencies installed
- [ ] Database initialized
- [ ] Model trained
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Can access http://localhost:3000
- [ ] Integration test passes (8/8)
- [ ] Can scan UPC code
- [ ] Can predict fill
- [ ] Can execute fill
- [ ] Can view health status
- [ ] Can view SPC status
- [ ] Can search anomalies

---

## 🚀 Next Steps

### For Development
1. Replace mock pages with integrated versions
2. Add authentication
3. Add real-time updates
4. Customize UI theme
5. Add more products

### For Production
1. Set up production database
2. Configure environment variables
3. Deploy backend (Docker/Cloud)
4. Deploy frontend (Vercel/Netlify)
5. Set up monitoring

### For Hackathon
1. Prepare demo script
2. Create presentation slides
3. Record demo video
4. Test on different devices
5. Submit before deadline!

---

## 📞 Getting Help

### Documentation
- **Integration Guide**: `FULLSTACK_INTEGRATION.md`
- **API Docs**: http://localhost:8000/docs
- **Quick Reference**: `QUICK_REFERENCE.md`
- **Troubleshooting**: `DEPLOYMENT_CHECKLIST.md`

### Common Commands
```bash
# Start backend
python api/main.py

# Start frontend
npm run dev

# Run tests
python test_integration.py

# Check logs
# Backend: Check terminal output
# Frontend: Check browser console (F12)

# Stop servers
# Press Ctrl+C in terminal
```

### File Locations
- **Database**: `data/calibration.db`
- **Model**: `models/pinn_model.pth`
- **Anomaly DB**: `data/anomaly_db.json`
- **Config**: `config/config.yaml`
- **Logs**: Terminal output

---

## 🎉 You're Ready!

Your PINNs-UPC Calibration System is now fully set up and running!

**Access your application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

**Sample UPC codes to try:**
- `1234567890001` - Water
- `1234567890002` - Vegetable Oil
- `1234567890003` - Honey

**Good luck with your hackathon!** 🚀

---

**Last Updated**: March 2026  
**Hackathon Deadline**: Mar 19, 2026 @ 2:30am GMT+5:30
