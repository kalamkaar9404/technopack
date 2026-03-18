"""
Train initial PINN model with seed data.
"""
import sys
from pathlib import Path
import numpy as np
import yaml

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DatabaseLayer
from src.models.pinn_model import PINNModel

def load_config():
    """Load configuration"""
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def prepare_training_data(db: DatabaseLayer):
    """Prepare training data from database"""
    print("Loading training data from database...")
    
    # Get all training data
    records = db.get_training_data(limit=10000)
    
    if len(records) == 0:
        print("No training data found! Please run seed_data.py first.")
        return None, None, None, None
    
    print(f"Found {len(records)} training records")
    
    # Prepare input and target arrays
    inputs = []
    targets = []
    
    for record in records:
        # Get product properties
        product = db.get_product(record.upc_code)
        if product is None:
            continue
        
        # Input: [valve_timing, pressure, nozzle_diameter, viscosity, density, 
        #         surface_tension, temperature, target_volume]
        # For training, we use actual_volume as the "target" volume
        input_row = [
            record.valve_timing,
            record.pressure,
            record.nozzle_diameter,
            product.viscosity,
            product.density,
            product.surface_tension,
            record.temperature if record.temperature else 25.0,
            record.actual_volume  # Use actual as target for training
        ]
        
        # Target: [actual_volume, actual_time]
        target_row = [record.actual_volume, record.actual_time]
        
        inputs.append(input_row)
        targets.append(target_row)
    
    # Convert to numpy arrays
    inputs = np.array(inputs, dtype=np.float32)
    targets = np.array(targets, dtype=np.float32)
    
    # Split into train/validation (80/20)
    n_train = int(0.8 * len(inputs))
    
    train_inputs = inputs[:n_train]
    train_targets = targets[:n_train]
    val_inputs = inputs[n_train:]
    val_targets = targets[n_train:]
    
    print(f"Training samples: {len(train_inputs)}")
    print(f"Validation samples: {len(val_inputs)}")
    
    return train_inputs, train_targets, val_inputs, val_targets

def main():
    """Main training function"""
    print("=" * 50)
    print("PINNs-UPC Calibration System - Model Training")
    print("=" * 50)
    
    # Load config
    config = load_config()
    
    # Initialize database
    db = DatabaseLayer(config['database']['path'])
    
    # Prepare data
    train_inputs, train_targets, val_inputs, val_targets = prepare_training_data(db)
    
    if train_inputs is None:
        return
    
    # Initialize model
    print("\nInitializing PINN model...")
    model = PINNModel(
        hidden_layers=config['model']['architecture']['hidden_layers'],
        neurons_per_layer=config['model']['architecture']['neurons_per_layer']
    )
    
    # Train model
    print("\nTraining model...")
    history = model.train_model(
        train_inputs, train_targets,
        val_inputs, val_targets,
        epochs=config['model']['training']['epochs'],
        learning_rate=config['model']['training']['learning_rate'],
        early_stopping_patience=50
    )
    
    # Calculate validation accuracy
    val_accuracy = model.calculate_validation_accuracy(val_inputs, val_targets)
    print(f"\nValidation Accuracy: {val_accuracy:.2f}%")
    
    # Save model
    model_dir = config['model']['paths']['model_dir']
    version_name = "pinn_v1"
    model_path = model.save_model(version_name, model_dir)
    
    # Save model version to database
    db.save_model_version(
        version_name=version_name,
        training_samples=len(train_inputs),
        validation_accuracy=val_accuracy,
        model_path=model_path,
        set_active=True
    )
    
    print("\n" + "=" * 50)
    print("Model training complete!")
    print(f"Model saved to: {model_path}")
    print(f"Validation accuracy: {val_accuracy:.2f}%")
    print("=" * 50)

if __name__ == "__main__":
    main()
