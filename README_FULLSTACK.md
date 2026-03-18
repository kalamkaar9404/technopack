# PINNs-UPC Calibration System - Full Stack

**Technopack Hackathon 2026 - Complete Solution**

AI-powered liquid filling calibration system with modern web interface, combining Physics-Informed Neural Networks, computer vision, predictive maintenance, and global knowledge sharing.

## 🎯 What Makes This Special

1. **Instant Recognition**: Scan UPC → Get calibration in <100ms
2. **Physics + AI**: Not just ML, but physics-informed predictions
3. **Computer Vision**: Real-time fill verification with camera
4. **Predictive**: Prevents equipment failures before they happen
5. **Quality Control**: Statistical process control with 6 Western Electric rules
6. **Global Learning**: Crowd-sourced solutions to common problems
7. **Modern UI**: Beautiful, responsive web interface

## 🚀 Quick Start (3 Steps)

### 1. Setup (One Time)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Initialize system
python setup.py
```

### 2. Start Application
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### 3. Access
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📱 Features

### Frontend (Next.js + React + TypeScript)
- **Dashboard**: System overview with real-time metrics
- **Scanner**: UPC product recognition
- **Fill Monitor**: AI predictions with vision verification
- **Equipment Health**: Predictive maintenance dashboard
- **SPC Control**: Quality monitoring with control charts
- **Anomaly Database**: Global solution sharing

### Backend (Python + FastAPI)
- **PINN Model**: Physics-informed neural network for predictions
- **Vision Detection**: Computer vision fill verification
- **Health Monitor**: Equipment degradation tracking
- **SPC Monitor**: Statistical process control
- **Anomaly Database**: Anonymized issue sharing
- **REST API**: 15+ endpoints with Swagger docs

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     Next.js Frontend (Port 3000)        │
│  Modern UI with real-time monitoring    │
└──────────────┬──────────────────────────┘
               │ REST API
┌──────────────▼──────────────────────────┐
│     FastAPI Backend (Port 8000)         │
│  API layer with automatic docs          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        Python Services                  │
│  • PINN Model (AI predictions)          │
│  • Vision Detector (camera)             │
│  • Health Monitor (maintenance)         │
│  • SPC Monitor (quality)                │
│  • Anomaly Database (knowledge)         │
└─────────────────────────────────────────┘
```

## 📊 Technology Stack

### Frontend
- Next.js 16 (React 19)
- TypeScript
- Tailwind CSS
- Shadcn/ui components
- Recharts for visualization
- Lucide React icons

### Backend
- Python 3.9+
- FastAPI (REST API)
- PyTorch (PINN model)
- OpenCV (computer vision)
- SQLAlchemy (database)
- NumPy/SciPy (calculations)

## 🎮 Usage

### 1. Scan Product
```
Enter UPC: 1234567890002
→ Loads: Vegetable Oil
→ Shows: Viscosity, Density, Surface Tension
→ Profile: Valve timing, Pressure, Nozzle diameter
```

### 2. Predict Fill
```
Adjust parameters with sliders
Click "Predict Fill"
→ AI predicts volume and time
→ Shows confidence score
→ Warns about similar past issues
```

### 3. Execute Fill
```
Enter actual volume and time
Enable vision detection
Click "Log Fill Result"
→ Vision verifies fill level
→ Logs to health monitor
→ Checks SPC rules
→ Updates anomaly database
```

### 4. Monitor Health
```
View component health scores
Check active alerts
Review maintenance schedule
→ Nozzle: 92% (warning)
→ Valve: 98% (good)
→ Pump: 99% (good)
```

### 5. Check Quality
```
View SPC control chart
Check rule violations
Review process capability
→ Cpk: 1.45 (Excellent)
→ Process in control
```

### 6. Search Solutions
```
Select issue type: foam_overflow
Click "Search Solutions"
→ Shows community solutions
→ Sorted by effectiveness
→ With upvotes
```

## 📁 Project Structure

```
pinns-upc-calibration/
├── app/                    # Next.js pages
│   ├── page.tsx           # Dashboard
│   ├── scanner/           # UPC scanner
│   ├── fill-monitor/      # Fill operations
│   ├── equipment-health/  # Health monitoring
│   ├── spc-control/       # Quality control
│   └── anomaly-database/  # Solution sharing
├── components/            # React components
├── lib/                   # API client
├── api/                   # FastAPI backend
│   └── main.py           # API server
├── src/                   # Python services
│   ├── controller/        # Main orchestrator
│   ├── models/           # PINN model
│   ├── vision/           # Computer vision
│   ├── maintenance/      # Health monitoring
│   ├── quality/          # SPC monitoring
│   └── anomaly/          # Anomaly database
├── config/               # Configuration
├── data/                 # Database files
├── models/               # Trained models
└── scripts/              # Setup scripts
```

## 🧪 Testing

### Test Backend
```bash
python test_integration.py
```

### Test Frontend
```bash
npm run lint
npm run build
```

### Manual Testing
1. Start both servers
2. Open http://localhost:3000
3. Try sample UPC: 1234567890002
4. Execute a fill operation
5. Check all monitoring pages

## 📚 Documentation

- `FULLSTACK_INTEGRATION.md` - Complete integration guide
- `INTEGRATION_SUMMARY.md` - Quick integration overview
- `INTEGRATION_COMPLETE.md` - Backend details
- `V0_PROMPT.md` - Frontend design specs
- `QUICK_REFERENCE.md` - Quick reference
- API Docs: http://localhost:8000/docs

## 🎯 Sample Data

### Products
- `1234567890001` - Water (0.001 Pa·s)
- `1234567890002` - Vegetable Oil (0.065 Pa·s)
- `1234567890003` - Honey (6.0 Pa·s)
- `1234567890004` - Milk (0.002 Pa·s)
- `1234567890005` - Soda (0.001 Pa·s, carbonated)

### Anomalies
- Foam overflow (carbonated beverages)
- Clog (high viscosity products)
- Drift (temperature changes)
- Underfill (low pressure)
- Overfill (high pressure)

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check Python version
python --version  # Need 3.9+

# Reinstall dependencies
pip install -r requirements.txt

# Check port availability
netstat -an | grep 8000
```

### Frontend Issues
```bash
# Check Node version
node --version  # Need 18+

# Clear and reinstall
rm -rf node_modules
npm install

# Check port availability
netstat -an | grep 3000
```

### CORS Errors
- Ensure backend is running
- Check `.env.local` has correct API URL
- Verify CORS settings in `api/main.py`

## 🚀 Deployment

### Frontend (Vercel)
```bash
npm run build
vercel deploy
```

### Backend (Docker)
```bash
docker build -t pinns-upc-backend .
docker run -p 8000:8000 pinns-upc-backend
```

## 🏆 Hackathon Submission

**Event**: Technopack Hackathon 2026  
**Deadline**: Mar 19, 2026 @ 2:30am GMT+5:30  
**Prize**: $10,000  
**Judging**: Creativity

### Why This Wins

1. **Innovation**: Combines 5 cutting-edge technologies
2. **Completeness**: Full-stack working application
3. **Practicality**: Solves real industrial problem
4. **Creativity**: Unique approach with physics + AI
5. **Polish**: Professional UI and documentation

## 📞 Support

- Check API docs: http://localhost:8000/docs
- Review integration guide: `FULLSTACK_INTEGRATION.md`
- Run test script: `python test_integration.py`
- Check logs in terminal windows

## 🎉 Success Metrics

- Fill accuracy: >99%
- Equipment uptime: >98%
- Prediction confidence: >95%
- Response time: <100ms
- UI performance: 60 FPS

## 📝 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- Technopack for the hackathon opportunity
- Physics-Informed Neural Networks research
- Open source community

---

**Ready to revolutionize liquid filling calibration!** 🚀
