"""
Integration test script for PINNs-UPC Calibration System
Tests the full stack: Frontend API → Backend API → Python Services
"""
import requests
import json
import time

API_URL = "http://localhost:8000"

def test_health_check():
    """Test if backend is running"""
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"   ✓ Backend is online: {response.json()}")
        return True
    except Exception as e:
        print(f"   ✗ Backend not responding: {e}")
        return False

def test_get_products():
    """Test getting all products"""
    print("\n2. Testing get products...")
    try:
        response = requests.get(f"{API_URL}/api/products")
        data = response.json()
        print(f"   ✓ Found {len(data['products'])} products")
        for p in data['products'][:3]:
            print(f"     - {p['product_name']} ({p['upc_code']})")
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def test_scan_upc():
    """Test UPC scanning"""
    print("\n3. Testing UPC scan...")
    try:
        response = requests.post(
            f"{API_URL}/api/scan",
            json={"upc_code": "1234567890002"}
        )
        data = response.json()
        print(f"   ✓ Scanned: {data['product']['product_name']}")
        print(f"     Viscosity: {data['product']['viscosity']} Pa·s")
        if data['profile']:
            print(f"     Profile: {data['profile']['valve_timing']}s, {data['profile']['pressure']} PSI")
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def test_predict_fill():
    """Test fill prediction"""
    print("\n4. Testing fill prediction...")
    try:
        # First scan a product
        requests.post(f"{API_URL}/api/scan", json={"upc_code": "1234567890002"})
        
        # Then predict
        response = requests.post(
            f"{API_URL}/api/predict",
            json={
                "valve_timing": 1.5,
                "pressure": 50.0,
                "nozzle_diameter": 5.0,
                "target_volume": 500.0
            }
        )
        data = response.json()
        pred = data['prediction']
        print(f"   ✓ Predicted volume: {pred['predicted_volume']:.2f} mL")
        print(f"     Predicted time: {pred['predicted_time']:.2f} s")
        print(f"     Confidence: {pred['confidence']*100:.1f}%")
        
        if 'similar_anomalies' in pred and pred['similar_anomalies']:
            print(f"     ⚠ Found {len(pred['similar_anomalies'])} similar anomalies")
        
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def test_execute_fill():
    """Test fill execution"""
    print("\n5. Testing fill execution...")
    try:
        # First scan a product
        requests.post(f"{API_URL}/api/scan", json={"upc_code": "1234567890002"})
        
        # Then execute
        response = requests.post(
            f"{API_URL}/api/execute",
            json={
                "valve_timing": 1.5,
                "pressure": 50.0,
                "nozzle_diameter": 5.0,
                "target_volume": 500.0,
                "actual_volume": 498.5,
                "actual_time": 2.1,
                "use_vision": True
            }
        )
        data = response.json()
        print(f"   ✓ Executed fill: {data['actual_volume']:.2f} mL")
        print(f"     Anomaly detected: {data['anomaly_detected']}")
        
        if 'vision' in data:
            vision = data['vision']
            print(f"     📷 Vision: {vision['detected_volume']:.2f} mL (confidence: {vision['confidence']*100:.0f}%)")
            print(f"        Foam: {vision['has_foam']}, Quality: {vision['image_quality']}")
        
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def test_health_monitoring():
    """Test equipment health monitoring"""
    print("\n6. Testing health monitoring...")
    try:
        response = requests.get(f"{API_URL}/api/health")
        data = response.json()
        
        print(f"   ✓ Component health:")
        for component, health in data['components'].items():
            print(f"     - {component.title()}: {health['health_score']:.1f}%")
        
        if data['alerts']:
            print(f"   ⚠ Active alerts: {len(data['alerts'])}")
            for alert in data['alerts'][:2]:
                print(f"     - {alert['severity'].upper()}: {alert['message']}")
        
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def test_spc_monitoring():
    """Test SPC monitoring"""
    print("\n7. Testing SPC monitoring...")
    try:
        response = requests.get(f"{API_URL}/api/spc")
        data = response.json()
        
        print(f"   ✓ SPC status:")
        if data['chart_data']['status'] == 'ok':
            print(f"     Control chart: {data['chart_data']['num_points']} points")
        else:
            print(f"     Control chart: {data['chart_data']['status']}")
        
        if data['capability']['status'] == 'ok':
            print(f"     Cpk: {data['capability']['cpk']:.2f} ({data['capability']['capability']})")
        
        if data['alerts']:
            print(f"   ⚠ SPC alerts: {len(data['alerts'])}")
        
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def test_anomaly_database():
    """Test anomaly database"""
    print("\n8. Testing anomaly database...")
    try:
        # Get statistics
        response = requests.get(f"{API_URL}/api/anomalies")
        data = response.json()
        stats = data['statistics']
        
        print(f"   ✓ Anomaly database:")
        print(f"     Total anomalies: {stats['total_anomalies']}")
        print(f"     Average effectiveness: {stats['average_effectiveness']*100:.0f}%")
        print(f"     Issue types: {', '.join(stats['issue_types'].keys())}")
        
        # Search for solutions
        response = requests.get(f"{API_URL}/api/anomalies?issue_type=foam_overflow")
        data = response.json()
        if 'solutions' in data and data['solutions']:
            print(f"     Found {len(data['solutions'])} solutions for foam_overflow")
        
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def main():
    print("="*70)
    print("  PINNs-UPC Calibration System - Integration Test")
    print("="*70)
    
    print("\nMake sure the backend is running:")
    print("  python api/main.py")
    print("\nStarting tests in 2 seconds...")
    time.sleep(2)
    
    tests = [
        test_health_check,
        test_get_products,
        test_scan_upc,
        test_predict_fill,
        test_execute_fill,
        test_health_monitoring,
        test_spc_monitoring,
        test_anomaly_database
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*70)
    print("  Test Results")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Integration is working correctly.")
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Check the output above.")
    
    print("\nNext steps:")
    print("1. Start the frontend: npm run dev")
    print("2. Open http://localhost:3000")
    print("3. Test the UI manually")

if __name__ == "__main__":
    main()
