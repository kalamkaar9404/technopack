"""
Data validation functions for the PINNs-UPC Calibration System.
"""
from typing import Tuple

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def validate_product_properties(viscosity: float, density: float, 
                                surface_tension: float, temperature: float) -> Tuple[bool, str]:
    """
    Validate product properties are within acceptable ranges.
    
    Args:
        viscosity: Viscosity in Pa·s
        density: Density in kg/m³
        surface_tension: Surface tension in N/m
        temperature: Temperature in °C
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Viscosity validation (water to honey range)
    if not (0.001 <= viscosity <= 10.0):
        return False, f"Viscosity must be between 0.001 and 10.0 Pa·s, got {viscosity}"
    
    # Density validation (light oils to concentrated solutions)
    if not (500.0 <= density <= 2000.0):
        return False, f"Density must be between 500.0 and 2000.0 kg/m³, got {density}"
    
    # Surface tension validation (typical liquids)
    if not (0.02 <= surface_tension <= 0.08):
        return False, f"Surface tension must be between 0.02 and 0.08 N/m, got {surface_tension}"
    
    # Temperature validation (operational range)
    if not (-20.0 <= temperature <= 100.0):
        return False, f"Temperature must be between -20.0 and 100.0 °C, got {temperature}"
    
    return True, ""

def validate_fill_parameters(valve_timing: float, pressure: float,
                            nozzle_diameter: float, target_volume: float) -> Tuple[bool, str]:
    """
    Validate fill parameters are within acceptable ranges.
    
    Args:
        valve_timing: Valve timing in seconds
        pressure: Pressure in PSI
        nozzle_diameter: Nozzle diameter in mm
        target_volume: Target volume in mL
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Valve timing validation
    if not (0.1 <= valve_timing <= 5.0):
        return False, f"Valve timing must be between 0.1 and 5.0 seconds, got {valve_timing}"
    
    # Pressure validation
    if not (10.0 <= pressure <= 100.0):
        return False, f"Pressure must be between 10.0 and 100.0 PSI, got {pressure}"
    
    # Nozzle diameter validation
    if not (2.0 <= nozzle_diameter <= 10.0):
        return False, f"Nozzle diameter must be between 2.0 and 10.0 mm, got {nozzle_diameter}"
    
    # Target volume validation
    if not (10.0 <= target_volume <= 5000.0):
        return False, f"Target volume must be between 10.0 and 5000.0 mL, got {target_volume}"
    
    return True, ""

def validate_accuracy_thresholds(acceptable_accuracy: float, 
                                prediction_warning: float,
                                anomaly_detection: float) -> Tuple[bool, str]:
    """
    Validate accuracy thresholds are properly configured.
    
    Args:
        acceptable_accuracy: Acceptable fill accuracy threshold (%)
        prediction_warning: Prediction warning threshold (%)
        anomaly_detection: Anomaly detection threshold (%)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # All thresholds should be positive
    if acceptable_accuracy <= 0:
        return False, f"Acceptable accuracy must be positive, got {acceptable_accuracy}"
    
    if prediction_warning <= 0:
        return False, f"Prediction warning must be positive, got {prediction_warning}"
    
    if anomaly_detection <= 0:
        return False, f"Anomaly detection must be positive, got {anomaly_detection}"
    
    # Thresholds should be in ascending order
    if not (acceptable_accuracy < prediction_warning < anomaly_detection):
        return False, (f"Thresholds must be in ascending order: "
                      f"acceptable ({acceptable_accuracy}) < "
                      f"warning ({prediction_warning}) < "
                      f"anomaly ({anomaly_detection})")
    
    return True, ""

def calculate_error_percentage(predicted: float, actual: float) -> float:
    """
    Calculate error percentage between predicted and actual values.
    
    Args:
        predicted: Predicted value
        actual: Actual value
        
    Returns:
        Error percentage
    """
    if actual == 0:
        return 100.0 if predicted != 0 else 0.0
    
    return abs((predicted - actual) / actual) * 100.0
