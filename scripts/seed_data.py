"""
Seed database with sample products and training data.
"""
import sys
from pathlib import Path
import numpy as np
import yaml

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DatabaseLayer

def load_config():
    """Load configuration"""
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def seed_products(db: DatabaseLayer):
    """Create sample products with diverse properties"""
    products = [
        # (upc, name, viscosity, density, surface_tension, temp_min, temp_max)
        ("1234567890001", "Water", 0.001, 1000.0, 0.072, 0.0, 100.0),
        ("1234567890002", "Vegetable Oil", 0.065, 920.0, 0.032, 10.0, 80.0),
        ("1234567890003", "Honey", 6.0, 1420.0, 0.070, 15.0, 40.0),
        ("1234567890004", "Milk", 0.002, 1030.0, 0.050, 2.0, 8.0),
        ("1234567890005", "Orange Juice", 0.0015, 1045.0, 0.055, 2.0, 10.0),
        ("1234567890006", "Olive Oil", 0.081, 915.0, 0.033, 10.0, 80.0),
        ("1234567890007", "Syrup", 2.5, 1350.0, 0.065, 15.0, 50.0),
        ("1234567890008", "Vinegar", 0.0012, 1010.0, 0.060, 10.0, 30.0),
        ("1234567890009", "Soy Sauce", 0.003, 1100.0, 0.058, 10.0, 30.0),
        ("1234567890010", "Ketchup", 5.0, 1200.0, 0.062, 10.0, 40.0),
    ]
    
    print("Seeding products...")
    for upc, name, visc, dens, surf, tmin, tmax in products:
        success = db.add_product(upc, name, visc, dens, surf, tmin, tmax)
        if success:
            print(f"  + Added {name}")
        else:
            print(f"  - Failed to add {name}")

def seed_training_data(db: DatabaseLayer):
    """Generate synthetic training data"""
    print("\nGenerating synthetic training data...")
    
    products = [
        ("1234567890001", 0.001, 1000.0, 0.072),  # Water
        ("1234567890002", 0.065, 920.0, 0.032),   # Oil
        ("1234567890003", 6.0, 1420.0, 0.070),    # Honey
    ]
    
    np.random.seed(42)
    
    for upc, viscosity, density, surface_tension in products:
        # Generate 30-40 training samples per product
        n_samples = np.random.randint(30, 41)
        
        for _ in range(n_samples):
            # Random parameters within valid ranges
            valve_timing = np.random.uniform(0.5, 3.0)
            pressure = np.random.uniform(20.0, 80.0)
            nozzle_diameter = np.random.uniform(3.0, 8.0)
            temperature = np.random.uniform(15.0, 30.0)
            
            # Simulate actual volume based on physics
            # Simplified: volume ∝ (pressure * nozzle_diameter^4 * valve_timing) / viscosity
            base_volume = (pressure * (nozzle_diameter ** 4) * valve_timing) / (viscosity * 10.0)
            actual_volume = base_volume + np.random.normal(0, base_volume * 0.05)  # 5% noise
            
            # Simulate actual time
            actual_time = valve_timing + np.random.normal(0, 0.1)
            
            db.log_training_data(
                upc, valve_timing, pressure, nozzle_diameter,
                actual_volume, actual_time, temperature
            )
        
        print(f"  + Generated {n_samples} samples for UPC {upc}")

def main():
    """Main seeding function"""
    print("=" * 50)
    print("PINNs-UPC Calibration System - Database Seeding")
    print("=" * 50)
    
    # Load config
    config = load_config()
    
    # Initialize database
    db = DatabaseLayer(config['database']['path'])
    db.initialize_database()
    
    # Seed data
    seed_products(db)
    seed_training_data(db)
    
    print("\n" + "=" * 50)
    print("Database seeding complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
