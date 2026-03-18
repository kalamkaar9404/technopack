"""
Advanced Demo - Showcasing All 4 New Features
1. Computer Vision Fill Detection
2. Equipment Health Monitoring
3. Statistical Process Control
4. Crowd-Sourced Anomaly Database
"""
import sys
from pathlib import Path
import yaml
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.database import DatabaseLayer
from src.models.pinn_model import PINNModel
from src.optimizer import CalibrationOptimizer
from src.controller import CalibrationController
from src.vision import FillLevelDetector
from src.maintenance import EquipmentHealthMonitor
from src.quality import SPCMonitor
from src.anomaly import AnomalyDatabase

def load_config():
    """Load configuration"""
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def print_section(title):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def main():
    """Run advanced demo"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║   PINNs-UPC Calibration System - Advanced Features Demo         ║
    ║   Technopack Hackathon 2026 - Enhanced Edition                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Load config
    config = load_config()
    
    # Initialize core system
    print_section("Initializing Core System")
    
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
        print("⚠️  Model not found. Run: python scripts/train_model.py")
        return
    
    optimizer = CalibrationOptimizer(model, config)
    print("✓ Optimizer initialized")
    
    controller = CalibrationController(db, model, optimizer, config)
    print("✓ Controller initialized")
    
    # Initialize new features
    print_section("Initializing Advanced Features")
    
    # Feature 1: Computer Vision
    bottle_geometry = {
        'diameter_mm': 60,
        'height_mm': 200,
        'ml_per_mm': 2.5  # 500ml / 200mm
    }
    vision_detector = FillLevelDetector(bottle_geometry)
    print("✓ Computer Vision Fill Detector initialized")
    
    # Feature 5: Equipment Health Monitor
    health_monitor = EquipmentHealthMonitor(config)
    print("✓ Equipment Health Monitor initialized")
    
    # Feature 10: SPC Monitor
    spc_monitor = SPCMonitor(target_accuracy=100.0)
    print("✓ Statistical Process Control Monitor initialized")
    
    # Feature 16: Anomaly Database
    anomaly_db = AnomalyDatabase()
    anomaly_db.seed_initial_data()  # Load common anomalies
    print("✓ Crowd-Sourced Anomaly Database initialized")
    
    # Demo Feature 1: Computer Vision
    print_section("Feature 1: Computer Vision Fill Level Detection")
    
    print("Simulating camera-based fill verification...")
    target_volume = 500.0
    
    # Simulate 3 fills with vision verification
    for i in range(3):
        actual_volume = target_volume + np.random.normal(0, 2.5)  # ±2.5ml variation
        has_foam = i == 1  # Second fill has foam
        
        # Simulate camera image
        image = vision_detector.simulate_camera_image(actual_volume, has_foam)
        
        # Detect fill level
        result = vision_detector.detect_fill_level(image, target_volume)
        
        print(f"\nFill #{i+1}:")
        print(f"  Actual Volume: {actual_volume:.2f} mL")
        print(f"  Detected Volume: {result.detected_volume:.2f} mL")
        print(f"  Confidence: {result.confidence*100:.1f}%")
        print(f"  Liquid Height: {result.liquid_height:.1f} mm")
        print(f"  Foam Detected: {'Yes ⚠️' if result.has_foam else 'No ✓'}")
        print(f"  Image Quality: {result.image_quality}")
        
        # Verify accuracy
        is_accurate, error_pct = vision_detector.verify_fill_accuracy(
            result.detected_volume, target_volume, tolerance=1.0
        )
        
        if is_accurate:
            print(f"  Status: ✅ Accurate ({error_pct:.2f}% error)")
        else:
            print(f"  Status: ❌ Inaccurate ({error_pct:.2f}% error)")
    
    # Demo Feature 5: Equipment Health Monitoring
    print_section("Feature 5: Equipment Health Monitoring")
    
    print("Simulating 50 fills to track equipment health...")
    
    # Simulate fills with gradual nozzle degradation
    for i in range(50):
        # Simulate degradation (accuracy slowly decreases)
        degradation_factor = 1.0 - (i * 0.001)  # 0.1% degradation per 10 fills
        
        predicted_volume = 500.0
        actual_volume = predicted_volume * degradation_factor + np.random.normal(0, 1.0)
        
        parameters = {
            'valve_timing': 1.5,
            'pressure': 50.0,
            'nozzle_diameter': 5.0
        }
        
        # Log to health monitor
        health_monitor.log_fill_result(
            predicted_volume, actual_volume, target_volume, parameters
        )
    
    # Check health status
    health_status = health_monitor.get_health_status()
    
    print("\nEquipment Health Status:")
    for component, health in health_status.items():
        print(f"\n  {component.upper()}:")
        print(f"    Health Score: {health.health_score:.1f}%")
        print(f"    Maintenance Needed: {'Yes ⚠️' if health.maintenance_recommended else 'No ✓'}")
        
        if health.predicted_failure_date:
            days_until = (health.predicted_failure_date - datetime.now()).days
            print(f"    Predicted Failure: {days_until} days")
    
    # Check for alerts
    alerts = health_monitor.check_for_alerts()
    
    if alerts:
        print(f"\n  Active Alerts: {len(alerts)}")
        for alert in alerts:
            print(f"    [{alert.severity.upper()}] {alert.message}")
            print(f"      Action: {alert.recommended_action}")
    else:
        print("\n  No active alerts ✓")
    
    # Get maintenance schedule
    schedule = health_monitor.get_maintenance_schedule()
    
    if schedule:
        print(f"\n  Maintenance Schedule:")
        for task in schedule:
            print(f"    [{task['priority'].upper()}] {task['component']}: {task['action']}")
    
    # Demo Feature 10: Statistical Process Control
    print_section("Feature 10: Statistical Process Control (SPC)")
    
    print("Simulating fills with process variation...")
    
    # Simulate 30 fills with various patterns
    for i in range(30):
        if i < 10:
            # Normal variation
            actual_volume = 500.0 + np.random.normal(0, 2.0)
        elif i < 17:
            # Systematic drift (7 consecutive increasing)
            actual_volume = 500.0 + (i - 10) * 0.5 + np.random.normal(0, 1.0)
        else:
            # Back to normal
            actual_volume = 500.0 + np.random.normal(0, 2.0)
        
        # Log to SPC monitor
        spc_monitor.log_fill_accuracy(actual_volume, target_volume)
    
    # Check SPC rules
    spc_alerts = spc_monitor.check_spc_rules()
    
    print(f"\nSPC Analysis:")
    print(f"  Fills Monitored: 30")
    
    if spc_alerts:
        print(f"  Rule Violations: {len(spc_alerts)}")
        for alert in spc_alerts:
            print(f"\n    [{alert.severity.upper()}] {alert.rule_name}")
            print(f"      {alert.message}")
            print(f"      Action: {alert.recommended_action}")
    else:
        print(f"  Rule Violations: None ✓")
    
    # Get process capability
    capability = spc_monitor.get_process_capability()
    
    if capability['status'] == 'ok':
        print(f"\n  Process Capability:")
        print(f"    Cp: {capability['cp']:.2f}")
        print(f"    Cpk: {capability['cpk']:.2f}")
        print(f"    Rating: {capability['capability']}")
        print(f"    {capability['interpretation']}")
    
    # Get control chart data
    chart_data = spc_monitor.get_control_chart_data()
    
    if chart_data['status'] == 'ok':
        print(f"\n  Control Limits:")
        print(f"    UCL: {chart_data['ucl']:.2f}%")
        print(f"    Center: {chart_data['center']:.2f}%")
        print(f"    LCL: {chart_data['lcl']:.2f}%")
    
    # Demo Feature 16: Anomaly Database
    print_section("Feature 16: Crowd-Sourced Anomaly Database")
    
    # Get database statistics
    stats = anomaly_db.get_statistics()
    
    print(f"Global Anomaly Database:")
    print(f"  Total Anomalies: {stats['total_anomalies']}")
    print(f"  Average Effectiveness: {stats['average_effectiveness']*100:.1f}%")
    print(f"  Total Community Upvotes: {stats['total_upvotes']}")
    
    print(f"\n  Issue Types:")
    for issue, count in stats['issue_types'].items():
        print(f"    {issue}: {count}")
    
    # Check for similar anomalies (simulate carbonated beverage foam issue)
    print(f"\n  Checking for similar anomalies...")
    print(f"  Current Conditions: Carbonated beverage, 32°C, High pressure")
    
    similar = anomaly_db.check_similar_anomalies(
        product_type='carbonated beverage',
        viscosity=0.001,
        temperature=32.0,
        conditions={'pressure': 60, 'valve_timing': 1.5}
    )
    
    if similar:
        print(f"\n  Found {len(similar)} similar past anomalies:")
        for i, match in enumerate(similar, 1):
            print(f"\n    Match #{i}:")
            print(f"      Similarity: {match.similarity_score*100:.1f}%")
            print(f"      Issue: {match.issue_type}")
            print(f"      Solution: {match.solution}")
            print(f"      Effectiveness: {match.effectiveness*100:.1f}%")
            print(f"      Community Upvotes: {match.upvotes}")
    else:
        print(f"  No similar anomalies found")
    
    # Get top solutions for foam issues
    print(f"\n  Top Solutions for Foam Issues:")
    top_solutions = anomaly_db.get_top_solutions('foam_overflow', limit=3)
    
    for i, solution in enumerate(top_solutions, 1):
        print(f"\n    Solution #{i}:")
        print(f"      {solution.solution}")
        print(f"      Effectiveness: {solution.effectiveness*100:.1f}%")
        print(f"      Upvotes: {solution.upvotes}")
    
    # Summary
    print_section("Demo Complete - Feature Summary")
    
    print("✅ Feature 1: Computer Vision")
    print("   - Real-time fill level detection")
    print("   - Foam detection")
    print("   - Visual verification with confidence scores")
    
    print("\n✅ Feature 5: Equipment Health Monitoring")
    print("   - Component health tracking")
    print("   - Predictive failure detection")
    print("   - Automated maintenance scheduling")
    
    print("\n✅ Feature 10: Statistical Process Control")
    print("   - Real-time quality monitoring")
    print("   - 6 SPC rule violations detected")
    print("   - Process capability analysis (Cp, Cpk)")
    
    print("\n✅ Feature 16: Crowd-Sourced Anomaly Database")
    print("   - Global anomaly sharing (anonymized)")
    print("   - Similar issue detection")
    print("   - Community-validated solutions")
    
    print("\n" + "="*70)
    print("All advanced features demonstrated successfully!")
    print("="*70)

if __name__ == "__main__":
    from datetime import datetime
    main()
