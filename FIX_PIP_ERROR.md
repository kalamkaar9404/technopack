# Fix "pip is not recognized" Error

## 🔴 Your Current Error

```
pip : The term 'pip' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

This means Python is not installed or not in your Windows PATH.

---

## ✅ Quick Fix (5 Minutes)

### Step 1: Install Python

1. **Download Python**
   - Open browser
   - Go to: https://www.python.org/downloads/
   - Click the big yellow button "Download Python 3.11.x"
   - Save the file

2. **Install Python**
   - Find the downloaded file (usually in Downloads folder)
   - Double-click to run
   - ⚠️ **CRITICAL**: Check the box "Add Python to PATH" ✓
   - Click "Install Now"
   - Wait 2-3 minutes
   - Click "Close"

3. **Verify Installation**
   - Close your current PowerShell window
   - Open a NEW PowerShell window (important!)
   - Type:
     ```powershell
     python --version
     ```
   - Should show: `Python 3.11.x`

### Step 2: Try Again

Now in your NEW PowerShell window:

```powershell
# Navigate to project
cd C:\Users\khush\mogan\techno_pack

# Install Python packages
python -m pip install -r requirements.txt

# Install Node packages (if Node.js is installed)
npm install
```

---

## 🔍 Check Prerequisites

Run this to check what's installed:

```powershell
# Check Python
python --version

# Check pip
python -m pip --version

# Check Node.js
node --version

# Check npm
npm --version
```

---

## 📝 Complete Installation Order

### 1. Install Python (if not installed)
- Download: https://www.python.org/downloads/
- ✓ Check "Add Python to PATH"
- Install

### 2. Install Node.js (if not installed)
- Download: https://nodejs.org/
- Install (default options)

### 3. Close and Reopen PowerShell
- This is important to load new PATH

### 4. Install Project Dependencies
```powershell
cd C:\Users\khush\mogan\techno_pack
python -m pip install -r requirements.txt
npm install
```

### 5. Initialize System
```powershell
python setup.py
```

### 6. Launch
```powershell
.\start.bat
```

---

## 🐛 Alternative Commands

If `python` doesn't work, try these:

```powershell
# Try py launcher
py --version
py -m pip install -r requirements.txt

# Try python3
python3 --version
python3 -m pip install -r requirements.txt

# Try with full path (adjust version number)
C:\Users\khush\AppData\Local\Programs\Python\Python311\python.exe --version
```

---

## 🎯 Quick Test

After installing Python, run this:

```powershell
# This should work now
python --version
python -m pip --version

# If both work, you're ready!
python -m pip install -r requirements.txt
```

---

## 📞 Still Not Working?

### Option 1: Use Microsoft Store Python

1. Open Microsoft Store
2. Search "Python 3.11"
3. Click "Get"
4. Wait for installation
5. Close and reopen PowerShell
6. Try: `python --version`

### Option 2: Check PATH Manually

1. Press Windows key
2. Type "environment variables"
3. Click "Edit the system environment variables"
4. Click "Environment Variables"
5. Under "System variables", find "Path"
6. Click "Edit"
7. Look for entries containing "Python"
8. If missing, click "New" and add:
   - `C:\Users\khush\AppData\Local\Programs\Python\Python311`
   - `C:\Users\khush\AppData\Local\Programs\Python\Python311\Scripts`
9. Click OK on all windows
10. Close and reopen PowerShell

---

## ✅ Success Checklist

Run these commands. All should work:

```powershell
python --version          # Should show Python 3.11.x
python -m pip --version   # Should show pip version
node --version            # Should show v18.x or higher
npm --version             # Should show version number
```

If all work, proceed with:

```powershell
python -m pip install -r requirements.txt
npm install
python setup.py
.\start.bat
```

---

## 🚀 After Everything is Installed

Your application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

**Need more help?** See `WINDOWS_SETUP.md` for detailed troubleshooting.
