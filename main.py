"""
Main entry point for the PINNs-UPC Calibration System.
"""
import sys
import yaml
from pathlib import Path

def load_config():
    """Load system configuration from config.yaml"""
    config_path = Path("config/config.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    """Main entry point"""
    print("PINNs-UPC Calibration System")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    print(f"Configuration loaded from: config/config.yaml")
    print(f"Database path: {config['database']['path']}")
    print(f"Model directory: {config['model']['paths']['model_dir']}")
    
    print("\nTo start the Streamlit UI, run:")
    print("  streamlit run src/ui/app.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
