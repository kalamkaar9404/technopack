"""
PINNs-UPC Calibration System - Integrated Demo
Demonstrates all features working together
"""
import yaml
from pathlib import Path

from src.database import DatabaseLayer
from src.models.pinn_model import PINNModel
from src.optimizer import CalibrationOptimizer
from src.controller import CalibrationController
from src.vision import FillLevelDetector
from src.maintenance import EquipmentHealthMonitor
from src.quality import SPCMonitor
from src.anomaly import AnomalyDatabase

def main():
    print("="*70)
    print("  PINNs-UPC Calibration System - Integrated Demo")
    print("  All Features: PINN + Vision + Health + SPC + Anomaly DB")
    print("="*70)
    
    # Load configuration
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize database
    print("\n1. Initializing database...")
    db = DatabaseLayer(config['database']['path'])
    db.initialize_database()
    
    # Initialize PINN model
    print("2. Loading PINN model...")
    model = PINNModel(
        hidden_layers=config['model']['architecture']['hidden_layers'],
        neurons_per_layer=config['model']['architecture']['neurons_per_layer']
    )
    
    model_path = Path(config['model']['paths']['model_dir']) / config['model']['paths']['active_model']
    if model_path.exists():
        model.load_model(str(model_path))
        print("   ✓ Model loaded")
    else:
        print("   ⚠ No trained model found - run scripts/train_model.py first")
    
    # Initialize optimizer
    print("3. Initializing optimizer...")
    optimizer = CalibrationOptimizer(model, config)
    
    # Initialize advanced features
    print("4. Initializing advanced features...")
    
    vision_detector = FillLevelDetector({
        'diameter_mm': 50,
        'height_mm': 200,
        'ml_per_mm': 10.0
    })
    print("   ✓ Vision detector ready")
    
    health_monitor = EquipmentHealthMonitor(config)
    print("   ✓ Health monitor ready")
    
    spc_monitor = SPCMonitor(target_accuracy=100.0)
    print("   ✓ SPC monitor ready")
    
    anomaly_db = AnomalyDatabase()
    if len(anomaly_db.anomalies) == 0:
        anomaly_db.seed_initial_data()
    print(f"   ✓ Anomaly database ready ({len(anomaly_db.anomalies)} anomalies)")
    
    # Initialize controller with all features
    print("5. Initializing integrated controller...")
    controller = CalibrationController(
        db, model, optimizer, config,
        vision_detector=vision_detector,
        health_monitor=health_monitor,
        spc_monitor=spc_monitor,
        anomaly_db=anomaly_db
    )
    
    print("\n" + "="*70)
    print("  DEMO: Integrated Fill Operation")
    print("="*70)
    
    # Scan product
    print("\n📱 Scanning UPC: 1234567890002 (Vegetable Oil)")
    context = controller.handle_upc_scan("1234567890002")
    
    if context.status == "ready":
        product = context.product
        profile = context.profile
        
        print(f"   Product: {product.product_name}")
        print(f"   Viscosity: {product.viscosity} Pa·s")
        print(f"   Profile: {profile.valve_timing:.2f}s, {profile.pressure:.0f} PSI, {profile.nozzle_diameter:.1f}mm")
    
    # Predict fill
    print("\n🔮 Predicting fill...")
    result = controller.predict_fill(
        valve_timing=profile.valve_timing,
        pressure=profile.pressure,
        nozzle_diameter=profile.nozzle_diameter,
        target_volume=500.0
    )
    
    pred = result.prediction
    print(f"   Predicted: {pred['predicted_volume']:.2f} mL in {pred['predicted_time']:.2f}s")
    print(f"   Confidence: {pred['confidence']*100:.1f}%")
    
    # Check for similar anomalies
    if 'similar_anomalies' in pred and pred['similar_anomalies']:
        print(f"\n⚠️  Found {len(pred['similar_anomalies'])} similar past issues:")
        for sim in pred['similar_anomalies'][:2]:
            print(f"   - {sim.issue_type}: {sim.solution[:60]}...")
    
    # Simulate fill execution with vision
    print("\n⚙️  Executing fill with vision detection...")
    actual_volume = 498.5  # Simulated actual
    
    # Simulate camera image
    camera_image = vision_detector.simulate_camera_image(actual_volume, has_foam=False)
    
    execution = controller.execute_fill(
        valve_timing=profile.valve_timing,
        pressure=profile.pressure,
        nozzle_diameter=profile.nozzle_diameter,
        target_volume=500.0,
        actual_volume=actual_volume,
        actual_time=2.1,
        camera_image=camera_image
    )
    
    print(f"   Actual: {execution.actual_volume:.2f} mL in {execution.actual_time:.2f}s")
    
    if hasattr(execution, 'vision_result') and execution.vision_result:
        vision = execution.vision_result
        print(f"   📷 Vision: {vision.detected_volume:.2f} mL (confidence: {vision.confidence*100:.0f}%)")
        if vision.has_foam:
            print("   ⚠️  Foam detected!")
    
    if execution.anomaly_detected:
        print("   ⚠️  Anomaly detected!")
    else:
        print("   ✓ Fill successful")
    
    # Simulate multiple fills for monitoring
    print("\n📊 Simulating 20 fills for monitoring...")
    import numpy as np
    
    for i in range(20):
        # Add some variation
        actual = 500.0 + np.random.normal(0, 2.0)
        
        camera_image = vision_detector.simulate_camera_image(actual)
        
        controller.execute_fill(
            valve_timing=profile.valve_timing,
            pressure=profile.pressure,
            nozzle_diameter=profile.nozzle_diameter,
            target_volume=500.0,
            actual_volume=actual,
            actual_time=2.0 + np.random.normal(0, 0.1),
            camera_image=camera_image
        )
    
    print("   ✓ 20 fills completed")
    
    # Check equipment health
    print("\n🔧 Equipment Health Status:")
    health_status = controller.get_health_status()
    for component, health in health_status.items():
        status_emoji = "✅" if health.health_score >= 98 else "⚠️" if health.health_score >= 95 else "❌"
        print(f"   {status_emoji} {component.title()}: {health.health_score:.1f}%")
    
    alerts = controller.get_health_alerts()
    if alerts:
        print(f"\n   Active alerts: {len(alerts)}")
        for alert in alerts[:3]:
            print(f"   - {alert.severity.upper()}: {alert.message}")
    
    # Check SPC
    print("\n📈 Statistical Process Control:")
    spc_alerts = controller.get_spc_alerts()
    if spc_alerts:
        print(f"   ⚠️  {len(spc_alerts)} rule violations detected")
        for alert in spc_alerts[:2]:
            print(f"   - {alert.rule_name}: {alert.message}")
    else:
        print("   ✓ Process in control")
    
    capability = controller.get_process_capability()
    if capability['status'] == 'ok':
        print(f"   Cpk: {capability['cpk']:.2f} ({capability['capability']})")
    
    # Anomaly database stats
    print("\n🌐 Anomaly Database:")
    stats = anomaly_db.get_statistics()
    print(f"   Total anomalies: {stats['total_anomalies']}")
    print(f"   Average effectiveness: {stats['average_effectiveness']*100:.0f}%")
    print(f"   Issue types: {', '.join(stats['issue_types'].keys())}")
    
    print("\n" + "="*70)
    print("  Demo Complete!")
    print("  Run 'streamlit run src/ui/app.py' to see the full UI")
    print("="*70)

if __name__ == "__main__":
    main()
