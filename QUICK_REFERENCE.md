# Quick Reference Guide

## 🚀 Getting Started (3 Steps)

```bash
# 1. Setup (one time, ~10 minutes)
python setup.py

# 2. Run UI
streamlit run src/ui/app.py

# 3. Try it out
# - Scanner page: Enter UPC 1234567890002
# - Fill Monitor: Click "Predict Fill" then "Log Fill Result"
# - Explore other pages
```

## 📱 UI Pages

| Page | Purpose | Key Features |
|------|---------|--------------|
| **Scanner** | Load products | UPC scanning, product database |
| **Fill Monitor** | Execute fills | Prediction, vision detection, anomaly warnings |
| **Equipment Health** | Monitor equipment | Component health, maintenance schedule |
| **SPC Control Chart** | Quality monitoring | Control charts, rule violations, Cpk |
| **Anomaly Database** | Search solutions | Similar issues, community solutions |

## 🎯 Sample UPC Codes

| UPC | Product | Viscosity | Notes |
|-----|---------|-----------|-------|
| 1234567890001 | Water | 0.001 Pa·s | Thin liquid, fast fill |
| 1234567890002 | Vegetable Oil | 0.065 Pa·s | Medium viscosity |
| 1234567890003 | Honey | 6.0 Pa·s | Thick liquid, slow fill |
| 1234567890004 | Milk | 0.002 Pa·s | Thin liquid |
| 1234567890005 | Soda | 0.001 Pa·s | Carbonated, foam risk |

## 🔧 Common Tasks

### Add New Product
1. Go to Scanner page
2. Expand "Add New Product"
3. Fill in UPC, name, viscosity, density, surface tension
4. Click "Add Product"

### Execute Fill with All Features
1. Scanner page: Scan UPC
2. Fill Monitor page:
   - Adjust parameters
   - Click "Predict Fill" → See anomaly warnings
   - Enable "Simulate Vision Detection"
   - Enter actual volume/time
   - Click "Log Fill Result" → See vision results

### Check Equipment Health
1. Equipment Health page
2. View component health scores
3. Check active alerts
4. Review maintenance schedule

### Monitor Quality
1. SPC Control Chart page
2. View control chart (need 20+ fills)
3. Check for rule violations
4. Review process capability (Cpk)

### Search for Solutions
1. Anomaly Database page
2. Select issue type (foam_overflow, clog, drift, etc.)
3. Click "Search Solutions"
4. View community-validated solutions

## 🎬 Demo Scripts

```bash
# Basic demo (core features)
python demo.py

# Advanced features demo (4 features standalone)
python demo_advanced.py

# Integrated demo (all features working together)
python demo_integrated.py
```

## 📊 Key Metrics

### Vision Detection
- **Confidence**: >70% = reliable
- **Image Quality**: good/poor/blocked
- **Foam Detection**: Yes/No

### Equipment Health
- **Health Score**: 
  - 98-100% = Good ✅
  - 95-98% = Warning ⚠️
  - <95% = Critical ❌
- **Failure Prediction**: Days until failure

### SPC Monitoring
- **Control Limits**: ±3σ (UCL/LCL)
- **Warning Limits**: ±2σ
- **Cpk**: 
  - >1.33 = Excellent
  - 1.0-1.33 = Adequate
  - <1.0 = Poor

### Anomaly Database
- **Similarity Threshold**: 70%
- **Effectiveness**: 0-100%
- **Upvotes**: Community validation

## 🐛 Troubleshooting

### "No trained model found"
```bash
python scripts/train_model.py
```

### "Database not found"
```bash
python scripts/seed_data.py
```

### "Anomaly database empty"
```python
from src.anomaly import AnomalyDatabase
db = AnomalyDatabase()
db.seed_initial_data()
```

### UI won't start
```bash
pip install -r requirements.txt
streamlit run src/ui/app.py
```

## 📁 Project Structure

```
pinns-upc-calibration/
├── src/
│   ├── controller/          # Main orchestrator
│   ├── database/            # UPC product database
│   ├── models/              # PINN model
│   ├── optimizer/           # Calibration optimizer
│   ├── vision/              # Computer vision (Feature 1)
│   ├── maintenance/         # Health monitoring (Feature 5)
│   ├── quality/             # SPC monitoring (Feature 10)
│   ├── anomaly/             # Anomaly database (Feature 16)
│   └── ui/                  # Streamlit UI
├── scripts/                 # Setup scripts
├── config/                  # Configuration
├── data/                    # Database files
├── models/                  # Trained models
└── tests/                   # Test files
```

## 🎓 Key Concepts

### Physics-Informed Neural Networks (PINNs)
- Combines AI learning with physics laws
- Requires less training data
- More accurate predictions
- Respects physical constraints (Navier-Stokes, continuity)

### UPC Database
- Instant product recognition
- Pre-configured calibration profiles
- Eliminates manual setup time

### Computer Vision
- Real-time fill verification
- Foam detection
- Quality assurance

### Predictive Maintenance
- Component health tracking
- Failure prediction
- Maintenance scheduling

### Statistical Process Control
- Western Electric rules
- Control charts
- Process capability

### Anomaly Database
- Anonymized issue sharing
- Similarity matching
- Community solutions

## 💡 Tips

1. **Run setup.py first** - It initializes everything
2. **Use demo scripts** - They show how features work
3. **Try different products** - Each has unique behavior
4. **Simulate multiple fills** - Monitoring needs data
5. **Check all UI pages** - Each shows different insights

## 📞 Support

- Documentation: See `README.md`
- Setup Guide: See `SETUP_ADVANCED.md`
- Integration Details: See `INTEGRATION_COMPLETE.md`
- Submission Info: See `HACKATHON_SUBMISSION.md`

## ⏰ Hackathon Info

- **Event**: Technopack Hackathon 2026
- **Deadline**: Mar 19, 2026 @ 2:30am GMT+5:30
- **Judging**: Creativity
- **Prize**: $10,000

Good luck! 🍀
