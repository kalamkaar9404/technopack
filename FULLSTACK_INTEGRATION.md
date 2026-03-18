# Full Stack Integration Guide

## Overview

The PINNs-UPC Calibration System is now a complete full-stack application:
- **Frontend**: Next.js 16 + React 19 + TypeScript + Tailwind CSS
- **Backend**: Python FastAPI + SQLAlchemy + PyTorch
- **Features**: PINN model, Vision detection, Health monitoring, SPC, Anomaly database

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Next.js Frontend                      │
│              (http://localhost:3000)                    │
│  Pages: Dashboard, Scanner, Fill Monitor, Health, etc. │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
                     │
┌────────────────────▼────────────────────────────────────┐
│                  FastAPI Backend                        │
│              (http://localhost:8000)                    │
│  Endpoints: /api/scan, /api/predict, /api/execute, etc.│
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Python Backend Services                    │
│  • CalibrationController (orchestrator)                │
│  • PINNModel (AI predictions)                          │
│  • FillLevelDetector (computer vision)                 │
│  • EquipmentHealthMonitor (predictive maintenance)     │
│  • SPCMonitor (quality control)                        │
│  • AnomalyDatabase (global knowledge)                  │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### Option 1: Automated Startup (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

This will:
1. Install Python dependencies (if needed)
2. Install Node.js dependencies (if needed)
3. Start backend API on port 8000
4. Start frontend on port 3000

### Option 2: Manual Startup

**Terminal 1 - Backend:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI backend
python api/main.py
```

**Terminal 2 - Frontend:**
```bash
# Install Node.js dependencies
npm install

# Start Next.js frontend
npm run dev
```

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **API Redoc**: http://localhost:8000/redoc

## API Endpoints

### Products
- `GET /api/products` - Get all products
- `POST /api/scan` - Scan UPC code
- `POST /api/products` - Add new product

### Fill Operations
- `POST /api/predict` - Get AI prediction
- `POST /api/execute` - Execute fill and log results

### Monitoring
- `GET /api/health` - Equipment health status
- `GET /api/spc` - SPC monitoring status
- `GET /api/anomalies` - Anomaly database
- `POST /api/anomalies` - Report new anomaly

### Dashboard
- `GET /api/dashboard` - Dashboard statistics

## Frontend Pages

### 1. Dashboard (`/`)
- System overview
- Key metrics (temperature, pressure, flow rate, uptime)
- Real-time charts
- System health summary

### 2. Scanner (`/scanner`)
- UPC code input
- Product information display
- Calibration profile preview
- Quick actions

### 3. Fill Monitor (`/fill-monitor`)
- Parameter controls (sliders)
- AI prediction display
- Vision detection results
- Fill history table
- Similar anomaly warnings

### 4. Equipment Health (`/equipment-health`)
- Component health scores
- Active alerts
- Maintenance schedule
- Accuracy trend charts

### 5. SPC Control Chart (`/spc-control`)
- Control chart visualization
- Rule violation alerts
- Process capability metrics (Cp, Cpk)

### 6. Anomaly Database (`/anomaly-database`)
- Search solutions by issue type
- Report new anomalies
- Database statistics
- Community solutions

## Integration Points

### Frontend → Backend

The frontend uses the API client (`lib/api.ts`) to communicate with the backend:

```typescript
import { api } from '@/lib/api'

// Scan UPC
const response = await api.scanUPC('1234567890001')

// Predict fill
const prediction = await api.predictFill({
  valve_timing: 1.0,
  pressure: 50,
  nozzle_diameter: 5.0,
  target_volume: 500
})

// Execute fill
const execution = await api.executeFill({
  valve_timing: 1.0,
  pressure: 50,
  nozzle_diameter: 5.0,
  target_volume: 500,
  actual_volume: 498.5,
  actual_time: 2.1,
  use_vision: true
})
```

### Backend → Python Services

The FastAPI backend (`api/main.py`) uses the Python controller:

```python
# Initialize controller with all features
controller = CalibrationController(
    db, model, optimizer, config,
    vision_detector=vision_detector,
    health_monitor=health_monitor,
    spc_monitor=spc_monitor,
    anomaly_db=anomaly_db
)

# Use controller methods
context = controller.handle_upc_scan(upc_code)
result = controller.predict_fill(...)
execution = controller.execute_fill(...)
```

## Data Flow Example

### Complete Fill Operation

1. **User scans UPC** (Frontend)
   ```
   User enters UPC → Scanner page
   ```

2. **Frontend calls API** (HTTP)
   ```
   POST /api/scan
   Body: { "upc_code": "1234567890001" }
   ```

3. **Backend processes** (Python)
   ```
   controller.handle_upc_scan(upc_code)
   → Database lookup
   → Load calibration profile
   → Return product + profile
   ```

4. **Frontend displays** (React)
   ```
   Show product properties
   Show calibration profile
   Enable "Start Fill" button
   ```

5. **User adjusts parameters** (Frontend)
   ```
   Sliders: valve_timing, pressure, nozzle_diameter
   Input: target_volume
   ```

6. **User clicks "Predict Fill"** (Frontend)
   ```
   POST /api/predict
   Body: { valve_timing, pressure, nozzle_diameter, target_volume }
   ```

7. **Backend predicts** (Python)
   ```
   controller.predict_fill(...)
   → PINN model prediction
   → Check anomaly database
   → Return prediction + warnings
   ```

8. **Frontend shows prediction** (React)
   ```
   Display predicted volume, time, confidence
   Show similar anomalies (if any)
   Show recommendations
   ```

9. **User executes fill** (Frontend)
   ```
   Enter actual_volume, actual_time
   Enable vision detection
   POST /api/execute
   ```

10. **Backend executes** (Python)
    ```
    controller.execute_fill(...)
    → Vision detection (if enabled)
    → Log to health monitor
    → Log to SPC monitor
    → Check for anomalies
    → Return results
    ```

11. **Frontend shows results** (React)
    ```
    Display actual vs predicted
    Show vision detection results
    Show anomaly status
    Update fill history
    ```

## Environment Variables

### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (Python)
No environment variables needed - uses `config/config.yaml`

## Configuration

### Backend Config (`config/config.yaml`)
```yaml
database:
  path: "./data/calibration.db"

model:
  architecture:
    hidden_layers: 6
    neurons_per_layer: 64

thresholds:
  acceptable_accuracy: 99.0
  prediction_warning: 2.0
  anomaly_detection: 5.0
  retraining_trigger: 100
```

### Frontend Config (`next.config.mjs`)
```javascript
const nextConfig = {
  // Configuration here
}
```

## Development

### Hot Reload
- **Frontend**: Automatic (Next.js dev server)
- **Backend**: Manual restart needed (or use `uvicorn --reload`)

### Debugging

**Frontend:**
- Browser DevTools
- React DevTools extension
- Console logs

**Backend:**
- FastAPI automatic docs at `/docs`
- Python print statements
- Logging to console

## Testing

### Frontend
```bash
npm run lint
npm run build  # Test production build
```

### Backend
```bash
# Run Python tests
pytest

# Run demo scripts
python demo.py
python demo_integrated.py
```

### API Testing
Use the Swagger UI at http://localhost:8000/docs to test endpoints interactively.

## Deployment

### Frontend (Vercel)
```bash
npm run build
# Deploy to Vercel
```

### Backend (Docker)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api/main.py"]
```

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt

# Check if port 8000 is available
netstat -an | grep 8000
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 is available
netstat -an | grep 3000
```

### CORS errors
Make sure the backend CORS middleware includes your frontend URL:
```python
allow_origins=["http://localhost:3000"]
```

### API connection errors
Check that:
1. Backend is running on port 8000
2. Frontend `.env.local` has correct API URL
3. No firewall blocking connections

## Next Steps

1. **Replace mock pages with integrated versions**
   - Copy `app/scanner/page-integrated.tsx` to `app/scanner/page.tsx`
   - Create similar integrated versions for other pages

2. **Add authentication**
   - Implement JWT tokens
   - Add user management

3. **Add real-time updates**
   - WebSocket support
   - Live monitoring

4. **Add data persistence**
   - Save user preferences
   - Export reports

5. **Production deployment**
   - Set up CI/CD
   - Configure production database
   - Add monitoring and logging

## Support

For issues or questions:
- Check API docs: http://localhost:8000/docs
- Review logs in terminal
- Check `INTEGRATION_COMPLETE.md` for backend details
- Check `V0_PROMPT.md` for frontend design specs
