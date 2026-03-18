"""
Core data structures for the PINNs-UPC Calibration System.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Product:
    """Product information with physical properties"""
    upc_code: str
    product_name: str
    viscosity: float  # Pa·s
    density: float    # kg/m³
    surface_tension: float  # N/m
    temp_min: Optional[float] = None  # °C
    temp_max: Optional[float] = None  # °C

@dataclass
class FillParameters:
    """Fill operation parameters"""
    valve_timing: float  # seconds
    pressure: float      # PSI
    nozzle_diameter: float  # mm
    target_volume: float    # mL

@dataclass
class ProductProperties:
    """Physical properties of liquid product"""
    viscosity: float  # Pa·s
    density: float    # kg/m³
    surface_tension: float  # N/m
    temperature: float  # °C

@dataclass
class FillPrediction:
    """PINN model prediction result"""
    predicted_volume: float  # mL
    predicted_time: float    # seconds
    confidence: float        # 0-1
    physics_valid: bool

@dataclass
class CalibrationProfile:
    """Calibration profile for a product"""
    profile_id: Optional[int]
    upc_code: str
    fill_parameters: FillParameters
    expected_accuracy: float  # percentage
    created_at: datetime
    is_active: bool = True

@dataclass
class FillRecord:
    """Historical fill operation record"""
    upc_code: str
    fill_parameters: FillParameters
    product_properties: ProductProperties
    actual_volume: float  # mL
    actual_time: float    # seconds
    timestamp: datetime

@dataclass
class AnomalyRecord:
    """Anomaly detection record"""
    upc_code: str
    predicted_volume: float  # mL
    actual_volume: float     # mL
    error_percentage: float
    classification: str  # equipment/product/parameter
    timestamp: datetime

@dataclass
class ModelVersion:
    """PINN model version metadata"""
    version_id: int
    version_name: str
    training_samples: int
    validation_accuracy: float
    is_active: bool
    model_path: str
    created_at: datetime
