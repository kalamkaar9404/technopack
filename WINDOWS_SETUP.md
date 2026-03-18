# Windows Setup Guide

## 🔧 Issue: pip not found

You're seeing this error because Python is either:
1. Not installed on your system
2. Not added to your Windows PATH

Let's fix this step by step.

---

## Step 1: Install Python

### Option A: Download Python Installer (Recommended)

1. **Download Python 3.11**
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.11.x" (latest version)
   - Save the installer

2. **Run the Installer**
   - Double-click the downloaded file
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" ✓
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation**
   - Open a NEW PowerShell window (important!)
   - Run:
     ```powershell
     python --version
     ```
   - Should show: `Python 3.11.x`

   - Run:
     ```powershell
     pip --version
     ```
   - Should show: `pip 23.x.x`

### Option B: Using Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.11"
3. Click "Get" or "Install"
4. Wait for installation
5. Open new PowerShell and verify (see above)

---

## Step 2: Install Node.js

1. **Download Node.js**
   - Go to: https://nodejs.org/
   - Download "LTS" version (recommended)
   - Run the installer
   - Click "Next" through all steps
   - Click "Install"

2. **Verify Installation**
   - Open a NEW PowerShell window
   - Run:
     ```powershell
     node --version
     ```
   - Should show: `v18.x.x` or higher

   - Run:
     ```powershell
     npm --version
     ```
   - Should show: `9.x.x` or higher

---

## Step 3: Navigate to Project

```powershell
# Change to your project directory
cd C:\Users\khush\mogan\techno_pack
```

---

## Step 4: Install Python Dependencies

```powershell
# Install Python packages
python -m pip install -r requirements.txt

# If that doesn't work, try:
py -m pip install -r requirements.txt

# Or with full path:
C:\Users\khush\AppData\Local\Programs\Python\Python311\python.exe -m pip install -r requirements.txt
```

**This will take 2-5 minutes**

---

## Step 5: Install Node.js Dependencies

```powershell
# Install Node packages
npm install

# If you get permission errors, try:
npm install --force
```

**This will take 3-7 minutes**

---

## Step 6: Initialize System

```powershell
# Run setup script
python setup.py

# If that doesn't work:
py setup.py
```

**This will take 5-10 minutes** (trains AI model)

---

## Step 7: Launch Application

### Option A: Using Batch File
```powershell
# Double-click start.bat in File Explorer
# Or run in PowerShell:
.\start.bat
```

### Option B: Manual Launch

**Terminal 1 - Backend:**
```powershell
python api/main.py
```

**Terminal 2 - Frontend (new PowerShell window):**
```powershell
npm run dev
```

---

## Step 8: Access Application

Open your browser:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Problem: "python is not recognized"

**Solution 1: Add Python to PATH manually**

1. Search for "Environment Variables" in Windows
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "System variables", find "Path"
5. Click "Edit"
6. Click "New"
7. Add: `C:\Users\khush\AppData\Local\Programs\Python\Python311`
8. Click "New" again
9. Add: `C:\Users\khush\AppData\Local\Programs\Python\Python311\Scripts`
10. Click "OK" on all windows
11. **Close and reopen PowerShell**

**Solution 2: Use py launcher**
```powershell
# Instead of 'python', use 'py'
py --version
py -m pip install -r requirements.txt
py setup.py
py api/main.py
```

### Problem: "Execution Policy" error

```powershell
# Run PowerShell as Administrator
# Then run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try again
npm install
```

### Problem: "Access Denied" or permission errors

```powershell
# Run PowerShell as Administrator
# Right-click PowerShell → "Run as Administrator"
# Then run your commands
```

### Problem: Port already in use

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Same for port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Problem: npm install fails

```powershell
# Clear npm cache
npm cache clean --force

# Delete node_modules
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json

# Try again
npm install
```

---

## 📝 Quick Command Reference

### Check if installed:
```powershell
python --version
pip --version
node --version
npm --version
```

### Install dependencies:
```powershell
python -m pip install -r requirements.txt
npm install
```

### Initialize system:
```powershell
python setup.py
```

### Start backend:
```powershell
python api/main.py
```

### Start frontend (new window):
```powershell
npm run dev
```

### Test integration:
```powershell
python test_integration.py
```

---

## 🎯 Alternative: Use Python from Microsoft Store

If you're having PATH issues, the Microsoft Store version automatically handles PATH:

1. Open Microsoft Store
2. Search "Python 3.11"
3. Install
4. Close and reopen PowerShell
5. Try: `python --version`

---

## 🔍 Verify Everything is Working

Run this command to check all prerequisites:

```powershell
# Check Python
python --version
if ($?) { Write-Host "✓ Python installed" -ForegroundColor Green } else { Write-Host "✗ Python not found" -ForegroundColor Red }

# Check pip
pip --version
if ($?) { Write-Host "✓ pip installed" -ForegroundColor Green } else { Write-Host "✗ pip not found" -ForegroundColor Red }

# Check Node
node --version
if ($?) { Write-Host "✓ Node.js installed" -ForegroundColor Green } else { Write-Host "✗ Node.js not found" -ForegroundColor Red }

# Check npm
npm --version
if ($?) { Write-Host "✓ npm installed" -ForegroundColor Green } else { Write-Host "✗ npm not found" -ForegroundColor Red }
```

---

## 📞 Still Having Issues?

### Check Python Installation Location

```powershell
# Find where Python is installed
where.exe python

# Or
Get-Command python | Select-Object -ExpandProperty Definition
```

### Check if Python is in PATH

```powershell
$env:Path -split ';' | Select-String -Pattern 'Python'
```

### Reinstall Python with PATH

1. Uninstall Python from "Add or Remove Programs"
2. Download fresh installer from python.org
3. Run installer
4. ✓ Check "Add Python to PATH"
5. Click "Install Now"
6. Restart PowerShell

---

## ✅ Success Checklist

- [ ] Python 3.11+ installed
- [ ] pip working (`pip --version`)
- [ ] Node.js 18+ installed
- [ ] npm working (`npm --version`)
- [ ] Can run `python --version`
- [ ] Can run `pip --version`
- [ ] Can run `node --version`
- [ ] Can run `npm --version`
- [ ] Python dependencies installed
- [ ] Node dependencies installed
- [ ] System initialized (`python setup.py`)
- [ ] Backend starts (`python api/main.py`)
- [ ] Frontend starts (`npm run dev`)

---

## 🚀 Once Everything is Installed

Follow the main setup guide:
```powershell
# 1. Install dependencies
python -m pip install -r requirements.txt
npm install

# 2. Initialize
python setup.py

# 3. Launch
.\start.bat
```

---

**Need more help?** Check `COMPLETE_SETUP_GUIDE.md` for detailed instructions.
