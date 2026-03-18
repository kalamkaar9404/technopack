# Quick Start - 5 Minutes

## 🚀 Fastest Way to Launch

### Prerequisites Check
```bash
python --version  # Need 3.9+
node --version    # Need 18+
```

### 1. Install Dependencies (First Time Only)
```bash
pip install -r requirements.txt
npm install
python setup.py
```

### 2. Launch Application
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh && ./start.sh
```

### 3. Access Application
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Test It
```bash
python test_integration.py
```

---

## 📝 Command Cheat Sheet

### Installation
```bash
# Python packages
pip install -r requirements.txt

# Node packages
npm install

# Initialize system
python setup.py
```

### Running
```bash
# Backend (Terminal 1)
python api/main.py

# Frontend (Terminal 2)
npm run dev

# Or use automated script
start.bat  # Windows
./start.sh # Linux/Mac
```

### Testing
```bash
# Integration test
python test_integration.py

# Frontend lint
npm run lint

# Frontend build
npm run build
```

### Demos
```bash
# Basic demo
python demo.py

# Advanced features
python demo_advanced.py

# Integrated system
python demo_integrated.py
```

---

## 🎯 Sample UPC Codes

| UPC | Product | Type |
|-----|---------|------|
| `1234567890001` | Water | Thin liquid |
| `1234567890002` | Vegetable Oil | Medium |
| `1234567890003` | Honey | Thick liquid |
| `1234567890004` | Milk | Thin liquid |
| `1234567890005` | Soda | Carbonated |

---

## 🔧 Quick Fixes

### Backend won't start
```bash
pip install --upgrade -r requirements.txt
python setup.py
```

### Frontend won't start
```bash
rm -rf node_modules .next
npm install
```

### CORS errors
```bash
# Check .env.local exists with:
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

---

## 📱 Quick Test Flow

1. Open http://localhost:3000
2. Go to Scanner page
3. Enter UPC: `1234567890002`
4. Click "Scan"
5. Go to Fill Monitor
6. Click "Predict Fill"
7. Enter actual values
8. Click "Log Fill Result"
9. ✅ Success!

---

## 📚 Full Documentation

- **Complete Setup**: `COMPLETE_SETUP_GUIDE.md`
- **Integration**: `FULLSTACK_INTEGRATION.md`
- **API Reference**: http://localhost:8000/docs
- **Troubleshooting**: `DEPLOYMENT_CHECKLIST.md`

---

**Ready in 5 minutes!** 🚀
