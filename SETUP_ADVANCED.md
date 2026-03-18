# Complete Setup Guide - Advanced PINNs-UPC Calibration System

## 🎯 What's New in This Version

This enhanced version includes 4 powerful new features:

1. **Computer Vision Fill Level Detection** - Visual verification of fills
2. **Equipment Health Monitoring** - Predictive maintenance
3. **Statistical Process Control (SPC)** - Real-time quality monitoring
4. **Crowd-Sourced Anomaly Database** - Global learning from anomalies

---

## 📋 Prerequisites

- **Python 3.9+** (Check: `python --version`)
- **pip** package manager
- **10GB** free disk space
- **8GB RAM** minimum (16GB recommended)
- **Webcam** (optional, for real camera integration)

---

## 🚀 Quick Setup (5 Minutes)

### Option 1: Automated Setup (Recommended)

```bash
# Run automated setup
python setup.py
```

This will:
1. Install all dependencies (including OpenCV for vision)
2. Create database with sample products
3. Train initial PINN model
4. Seed anomaly database
5. Verify installation

### Option 2: Manual Setup

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Seed database
python scripts/seed_data.py

# Step 3: Train model
python scripts/train_model.py

# Step 4: Run advanced demo
python demo_advanced.py
```

---

## 📦 New Dependencies

The advanced version adds:

```
opencv-python>=4.8.0  # Computer vision
Pillow>=10.0.0        # Image processing
```

All other dependencies remain the same.

---

## 🎮 Running the System

### 1. Basic Demo (Original Features)

```bash
python demo.py
```

Shows:
- UPC scanning
- PINN predictions
- Fill execution
- Product switching

### 2. Advanced Demo (All Features)

```bash
python demo_advanced.py
```

Shows:
- Computer vision fill detection
- Equipment health monitoring
- SPC rule violations
- Anomaly database matching

### 3. Web Interface (Full System)

```bash
streamlit run src/ui/app.py
```

Access at: `http://localhost:8501`

---

## 🔬 Feature-by-Feature Setup

### Feature 1: Computer Vision Fill Level Detection

**No additional setup required!**

The system uses simulated camera images for demo purposes.

**For real camera integration:**

```python
# In your code
import cv2
from src.vision import FillLevelDetector

# Initialize detector
detector = FillLevelDetector(bottle_geometry={
    'diameter_mm': 60,
    'height_mm': 200,
    'ml_per_mm': 2.5
})

# Capture from camera
cap = cv2.VideoCapture(0)  # 0 = default camera
ret, frame = cap.read()

# Detect fill level
result = detector.detect_fill_level(frame, target_volume=500.0)

print(f"Detected: {result.detected_volume:.2f} mL")
print(f"Confidence: {result.confidence*100:.1f}%")
print(f"Foam: {result.has_foam}")
```

**Camera Setup Tips:**
- Mount camera directly above filling station
- Ensure good lighting (avoid shadows)
- Use fixed focus lens
- Calibrate bottle geometry for your bottles

---

### Feature 5: Equipment Health Monitoring

**Automatic - No setup required!**

The system automatically tracks:
- Nozzle wear
- Valve degradation
- Pump stability
- Sensor accuracy

**Usage:**

```python
from src.maintenance import EquipmentHealthMonitor

# Initialize
health_monitor = EquipmentHealthMonitor(config)

# Log each fill
health_monitor.log_fill_result(
    predicted_volume=500.0,
    actual_volume=498.5,
    target_volume=500.0,
    parameters={'pressure': 50, 'valve_timing': 1.5}
)

# Check health
health_status = health_monitor.get_health_status()
alerts = health_monitor.check_for_alerts()
schedule = health_monitor.get_maintenance_schedule()
```

**Interpreting Health Scores:**
- **100-98%**: Excellent - No action needed
- **98-95%**: Good - Monitor closely
- **95-90%**: Warning - Schedule maintenance
- **<90%**: Critical - Immediate action required

---

### Feature 10: Statistical Process Control (SPC)

**Automatic - No setup required!**

Implements 6 Western Electric rules:
1. Point beyond control limits (3σ)
2. 2/3 points beyond warning limits (2σ)
3. 4/5 points beyond 1σ
4. 7 consecutive points on one side
5. 7 consecutive points trending
6. 15 consecutive points too consistent

**Usage:**

```python
from src.quality import SPCMonitor

# Initialize
spc_monitor = SPCMonitor(target_accuracy=100.0)

# Log each fill
spc_monitor.log_fill_accuracy(
    actual_volume=498.5,
    target_volume=500.0
)

# Check for violations
alerts = spc_monitor.check_spc_rules()

# Get control chart data
chart_data = spc_monitor.get_control_chart_data()

# Get process capability
capability = spc_monitor.get_process_capability()
```

**Understanding Cpk Values:**
- **Cpk ≥ 1.33**: Excellent (Six Sigma capable)
- **Cpk ≥ 1.0**: Adequate (meets specifications)
- **Cpk ≥ 0.67**: Poor (improvement needed)
- **Cpk < 0.67**: Inadequate (immediate action)

---

### Feature 16: Crowd-Sourced Anomaly Database

**Automatic seeding on first run!**

Database location: `./data/anomaly_db.json`

**Usage:**

```python
from src.anomaly import AnomalyDatabase

# Initialize
anomaly_db = AnomalyDatabase()

# Report new anomaly
anomaly_id = anomaly_db.report_anomaly(
    product_type='carbonated beverage',
    viscosity=0.001,
    temperature=32.0,
    issue_type='foam_overflow',
    conditions={'pressure': 60, 'valve_timing': 1.5},
    solution='Reduce fill speed by 30%',
    effectiveness=0.95
)

# Check for similar issues
similar = anomaly_db.check_similar_anomalies(
    product_type='carbonated beverage',
    viscosity=0.001,
    temperature=32.0,
    conditions={'pressure': 60}
)

# Get top solutions
solutions = anomaly_db.get_top_solutions('foam_overflow')
```

**Privacy Protection:**
- Product names → Categories (thin/medium/thick liquid)
- Exact values → Ranges (50-60 PSI, not 55 PSI)
- No factory/customer information shared
- All data anonymized before storage

---

## 🧪 Testing the Features

### Test 1: Computer Vision

```bash
python -c "
from src.vision import FillLevelDetector
import numpy as np

detector = FillLevelDetector({
    'diameter_mm': 60,
    'height_mm': 200,
    'ml_per_mm': 2.5
})

# Simulate fill
image = detector.simulate_camera_image(500.0, has_foam=False)
result = detector.detect_fill_level(image, 500.0)

print(f'Detected: {result.detected_volume:.2f} mL')
print(f'Confidence: {result.confidence*100:.1f}%')
"
```

### Test 2: Equipment Health

```bash
python -c "
from src.maintenance import EquipmentHealthMonitor
import yaml

with open('config/config.yaml') as f:
    config = yaml.safe_load(f)

monitor = EquipmentHealthMonitor(config)

# Simulate 10 fills
for i in range(10):
    monitor.log_fill_result(500.0, 498.0 + i*0.1, 500.0, {})

health = monitor.get_health_status()
print(f'Components monitored: {len(health)}')
"
```

### Test 3: SPC Monitor

```bash
python -c "
from src.quality import SPCMonitor

spc = SPCMonitor()

# Simulate 20 fills
for i in range(20):
    spc.log_fill_accuracy(500.0 + i*0.2, 500.0)

alerts = spc.check_spc_rules()
print(f'SPC alerts: {len(alerts)}')
"
```

### Test 4: Anomaly Database

```bash
python -c "
from src.anomaly import AnomalyDatabase

db = AnomalyDatabase()
db.seed_initial_data()

stats = db.get_statistics()
print(f'Total anomalies: {stats[\"total_anomalies\"]}')
"
```

---

## 📊 Performance Benchmarks

### Original System:
- UPC Retrieval: ~50ms
- Fill Prediction: ~10ms
- Product Switching: ~100ms

### With Advanced Features:
- UPC Retrieval: ~50ms (unchanged)
- Fill Prediction: ~10ms (unchanged)
- **+ Vision Detection: ~30ms**
- **+ Health Check: ~5ms**
- **+ SPC Check: ~2ms**
- **+ Anomaly Check: ~10ms**

**Total overhead: ~47ms** (still well under 200ms requirement)

---

## 🐛 Troubleshooting

### Issue: OpenCV not installing

**Windows:**
```bash
pip install opencv-python --upgrade
```

**Linux:**
```bash
sudo apt-get install python3-opencv
pip install opencv-python
```

**Mac:**
```bash
brew install opencv
pip install opencv-python
```

### Issue: Camera not detected

```python
import cv2

# List available cameras
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} available")
        cap.release()
```

### Issue: Anomaly database not saving

Check permissions:
```bash
# Ensure data directory is writable
chmod 755 data/
```

### Issue: SPC alerts not triggering

Need at least 20 fills for control limits:
```python
spc_monitor = SPCMonitor()

# Log 20+ fills first
for i in range(25):
    spc_monitor.log_fill_accuracy(actual, target)

# Now check rules
alerts = spc_monitor.check_spc_rules()
```

---

## 📈 Integration with Existing System

All new features integrate seamlessly:

```python
# Your existing code
controller = CalibrationController(db, model, optimizer, config)
context = controller.handle_upc_scan("1234567890001")
result = controller.predict_fill(1.5, 50.0, 5.0, 500.0)

# Add new features
from src.vision import FillLevelDetector
from src.maintenance import EquipmentHealthMonitor
from src.quality import SPCMonitor
from src.anomaly import AnomalyDatabase

vision = FillLevelDetector(bottle_geometry)
health = EquipmentHealthMonitor(config)
spc = SPCMonitor()
anomalies = AnomalyDatabase()

# Use together
prediction = result.prediction
vision_result = vision.detect_fill_level(camera_image, 500.0)

# Log to all monitors
health.log_fill_result(prediction['predicted_volume'], 
                       vision_result.detected_volume, 500.0, {})
spc.log_fill_accuracy(vision_result.detected_volume, 500.0)

# Check for issues
health_alerts = health.check_for_alerts()
spc_alerts = spc.check_spc_rules()
similar_anomalies = anomalies.check_similar_anomalies(...)
```

---

## 🎯 Next Steps

1. **Run the advanced demo:**
   ```bash
   python demo_advanced.py
   ```

2. **Explore the web interface:**
   ```bash
   streamlit run src/ui/app.py
   ```

3. **Integrate with your hardware:**
   - Connect camera for vision
   - Add sensors for health monitoring
   - Configure SPC thresholds

4. **Contribute to anomaly database:**
   - Report issues you encounter
   - Upvote solutions that work
   - Help the community learn

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review demo scripts for examples
3. See inline code documentation

---

**Built with ❤️ for Technopack Hackathon 2026**

*Now with Computer Vision, Predictive Maintenance, SPC, and Global Anomaly Learning!*
