"""
Quick setup script for PINNs-UPC Calibration System
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"[OK] {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] {description} failed")
        print(e.stderr)
        return False

def main():
    """Main setup function"""
    print("""
    ============================================================
       PINNs-UPC Calibration System - Quick Setup
       Technopack Hackathon 2026
    ============================================================
    """)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("[FAIL] Python 3.9+ required")
        print(f"  Current version: {sys.version}")
        return
    
    print(f"[OK] Python version: {sys.version.split()[0]}")
    
    # Create directories
    print("\nCreating directories...")
    Path("data").mkdir(exist_ok=True)
    Path("models").mkdir(exist_ok=True)
    Path("scripts").mkdir(exist_ok=True)
    print("[OK] Directories created")
    
    # Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing dependencies"
    ):
        print("\n[WARNING] Dependency installation failed. Please install manually:")
        print("    pip install -r requirements.txt")
        return
    
    # Seed database
    if not run_command(
        f"{sys.executable} scripts/seed_data.py",
        "Seeding database with sample products"
    ):
        print("\n[WARNING] Database seeding failed")
        return
    
    # Initialize anomaly database
    print("\nInitializing anomaly database...")
    try:
        from src.anomaly import AnomalyDatabase
        anomaly_db = AnomalyDatabase()
        if len(anomaly_db.anomalies) == 0:
            anomaly_db.seed_initial_data()
        print("[OK] Anomaly database initialized")
    except Exception as e:
        print(f"[WARNING] Anomaly database initialization failed: {e}")
    
    # Train model
    if not run_command(
        f"{sys.executable} scripts/train_model.py",
        "Training initial PINN model (this may take 5-10 minutes)"
    ):
        print("\n[WARNING] Model training failed")
        return
    
    # Success message
    print(f"""
    
    ============================================================
       Setup Complete!
    ============================================================
    
    To start the application:
    
        streamlit run src/ui/app.py
    
    The UI will open at: http://localhost:8501
    
    Sample UPC codes to try:
        1234567890001 - Water
        1234567890002 - Vegetable Oil
        1234567890003 - Honey
    
    For more information, see README.md
    """)

if __name__ == "__main__":
    main()
