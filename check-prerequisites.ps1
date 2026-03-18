# PowerShell script to check prerequisites for PINNs-UPC Calibration System

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Prerequisites Check" -ForegroundColor Cyan
Write-Host "  PINNs-UPC Calibration System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -ge 3 -and $minor -ge 9) {
            Write-Host " ✓ $pythonVersion" -ForegroundColor Green
        } else {
            Write-Host " ✗ Version too old: $pythonVersion (need 3.9+)" -ForegroundColor Red
            $allGood = $false
        }
    }
} catch {
    Write-Host " ✗ Not found" -ForegroundColor Red
    Write-Host "  → Install from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  → Make sure to check 'Add Python to PATH'" -ForegroundColor Yellow
    $allGood = $false
}

# Check pip
Write-Host "Checking pip..." -NoNewline
try {
    $pipVersion = pip --version 2>&1
    if ($pipVersion -match "pip") {
        Write-Host " ✓ $pipVersion" -ForegroundColor Green
    }
} catch {
    Write-Host " ✗ Not found" -ForegroundColor Red
    Write-Host "  → Run: python -m ensurepip --upgrade" -ForegroundColor Yellow
    $allGood = $false
}

# Check Node.js
Write-Host "Checking Node.js..." -NoNewline
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "v(\d+)") {
        $major = [int]$Matches[1]
        if ($major -ge 18) {
            Write-Host " ✓ $nodeVersion" -ForegroundColor Green
        } else {
            Write-Host " ✗ Version too old: $nodeVersion (need v18+)" -ForegroundColor Red
            $allGood = $false
        }
    }
} catch {
    Write-Host " ✗ Not found" -ForegroundColor Red
    Write-Host "  → Install from: https://nodejs.org/" -ForegroundColor Yellow
    $allGood = $false
}

# Check npm
Write-Host "Checking npm..." -NoNewline
try {
    $npmVersion = npm --version 2>&1
    Write-Host " ✓ v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host " ✗ Not found" -ForegroundColor Red
    Write-Host "  → Comes with Node.js installation" -ForegroundColor Yellow
    $allGood = $false
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✓ All prerequisites installed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. python -m pip install -r requirements.txt" -ForegroundColor White
    Write-Host "  2. npm install" -ForegroundColor White
    Write-Host "  3. python setup.py" -ForegroundColor White
    Write-Host "  4. .\start.bat" -ForegroundColor White
} else {
    Write-Host "✗ Some prerequisites are missing" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install the missing software and run this script again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "For detailed instructions, see: WINDOWS_SETUP.md" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
