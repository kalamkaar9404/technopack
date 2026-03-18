"""
Quick demo script to test the PINNs-UPC Calibration System
"""
import sys
from pathlib import Path
import yaml

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.database import DatabaseLayer
from src.models.pinn_model import PINNModel
from src.optimizer import CalibrationOptimizer
from src.controller import CalibrationController

def load_config():
    """Load configuration"""
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def main():
    """Run demo"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   PINNs-UPC Calibration System - Demo                   ║
    ║   Technopack Hackathon 2026                              ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Load config
    config = load_config()
    
    # Initialize components
    print_section("Initializing System")
    
    db = DatabaseLayer(config['database']['path'])
    print("✓ Database connected")
    
    model = PINNModel(
        hidden_layers=config['model']['architecture']['hidden_layers'],
        neurons_per_layer=config['model']['architecture']['neurons_per_layer']
    )
    
    model_path = Path(config['model']['paths']['model_dir']) / config['model']['paths']['active_model']
    if model_path.exists():
        model.load_model(str(model_path))
        print("✓ PINN model loaded")
    else:
        print("⚠️  Model not found. Please run: python scripts/train_model.py")
        return
    
    optimizer = CalibrationOptimizer(model, config)
    print("✓ Optimizer initialized")
    
    controller = CalibrationController(db, model, optimizer, config)
    print("✓ Controller initialized")
    
    # Demo 1: UPC Scanning
    print_section("Demo 1: UPC Scanning")
    
    upc_water = "1234567890001"
    print(f"Scanning UPC: {upc_water} (Water)")
    
    context = controller.handle_upc_scan(upc_water)
    
    if context.status == "ready":
        print(f"✓ Product loaded: {context.product.product_name}")
        print(f"  Viscosity: {context.product.viscosity} Pa·s")
        print(f"  Density: {context.product.density} kg/m³")
        print(f"  Surface Tension: {context.product.surface_tension} N/m")
        
        if context.profile:
            print(f"\n  Calibration Profile:")
            print(f"    Valve Timing: {context.profile.valve_timing:.2f} s")
            print(f"    Pressure: {context.profile.pressure:.2f} PSI")
            print(f"    Nozzle Diameter: {context.profile.nozzle_diameter:.2f} mm")
            print(f"    Target Volume: {context.profile.target_volume:.2f} mL")
    else:
        print(f"✗ Failed to load product: {context.status}")
        return
    
    # Demo 2: Fill Prediction
    print_section("Demo 2: Fill Prediction")
    
    print("Predicting fill with parameters:")
    valve_timing = 1.5
    pressure = 50.0
    nozzle_diameter = 5.0
    target_volume = 500.0
    
    print(f"  Valve Timing: {valve_timing} s")
    print(f"  Pressure: {pressure} PSI")
    print(f"  Nozzle Diameter: {nozzle_diameter} mm")
    print(f"  Target Volume: {target_volume} mL")
    
    result = controller.predict_fill(
        valve_timing, pressure, nozzle_diameter, target_volume
    )
    
    if result.prediction:
        pred = result.prediction
        print(f"\n✓ Prediction:")
        print(f"  Predicted Volume: {pred['predicted_volume']:.2f} mL")
        print(f"  Predicted Time: {pred['predicted_time']:.2f} s")
        print(f"  Confidence: {pred['confidence']*100:.1f}%")
        print(f"  Physics Valid: {pred['physics_valid']}")
        
        error_pct = abs(pred['predicted_volume'] - target_volume) / target_volume * 100.0
        print(f"  Error: {error_pct:.2f}%")
        
        if error_pct <= 1.0:
            print(f"  Status: ✅ Excellent (≤1% error)")
        elif error_pct <= 2.0:
            print(f"  Status: ⚠️  Acceptable (1-2% error)")
        else:
            print(f"  Status: ❌ Poor (>2% error)")
        
        if result.alert:
            print(f"\n  Alert: {result.alert}")
        
        if result.recommendation:
            print(f"\n  Recommended adjustments:")
            for key, value in result.recommendation.items():
                print(f"    {key}: {value:.2f}")
    
    # Demo 3: Fill Execution
    print_section("Demo 3: Fill Execution")
    
    actual_volume = 498.5  # Simulate actual fill
    actual_time = 1.52
    
    print(f"Logging fill result:")
    print(f"  Actual Volume: {actual_volume} mL")
    print(f"  Actual Time: {actual_time} s")
    
    execution = controller.execute_fill(
        valve_timing, pressure, nozzle_diameter,
        target_volume, actual_volume, actual_time
    )
    
    print(f"\n✓ Fill logged")
    print(f"  Anomaly Detected: {execution.anomaly_detected}")
    
    if execution.anomaly_detected:
        print(f"  ⚠️  Anomaly logged for analysis")
    
    # Demo 4: Product Switching
    print_section("Demo 4: Product Switching")
    
    upc_honey = "1234567890003"
    print(f"Switching to UPC: {upc_honey} (Honey)")
    
    new_context, cleaning_required = controller.switch_product(upc_honey, upc_water)
    
    if new_context.status == "ready":
        print(f"✓ Switched to: {new_context.product.product_name}")
        print(f"  Cleaning Required: {cleaning_required}")
        
        if cleaning_required:
            print(f"  ⚠️  Significant property change detected")
            print(f"     Please clean machine before proceeding")
    
    # Summary
    print_section("Demo Complete")
    
    print("System is ready for use!")
    print("\nTo start the web interface:")
    print("  streamlit run src/ui/app.py")
    print("\nSample UPC codes:")
    print("  1234567890001 - Water")
    print("  1234567890002 - Vegetable Oil")
    print("  1234567890003 - Honey")
    print("  1234567890004 - Milk")
    print("  1234567890005 - Orange Juice")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
