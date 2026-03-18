"""
SQLAlchemy database models for the PINNs-UPC Calibration System.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Product(Base):
    """Product table storing UPC codes and physical properties"""
    __tablename__ = 'products'
    
    upc_code = Column(String(13), primary_key=True)
    product_name = Column(String(255), nullable=False)
    viscosity = Column(Float, nullable=False)  # Pa·s
    density = Column(Float, nullable=False)     # kg/m³
    surface_tension = Column(Float, nullable=False)  # N/m
    temp_min = Column(Float)  # °C
    temp_max = Column(Float)  # °C
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    calibration_profiles = relationship("CalibrationProfile", back_populates="product")
    training_data = relationship("TrainingData", back_populates="product")
    anomalies = relationship("AnomalyLog", back_populates="product")
    
    # Data validation constraints
    __table_args__ = (
        CheckConstraint('viscosity >= 0.001 AND viscosity <= 10.0', name='check_viscosity'),
        CheckConstraint('density >= 500.0 AND density <= 2000.0', name='check_density'),
        CheckConstraint('surface_tension >= 0.02 AND surface_tension <= 0.08', name='check_surface_tension'),
        CheckConstraint('temp_min >= -20.0 AND temp_min <= 100.0', name='check_temp_min'),
        CheckConstraint('temp_max >= -20.0 AND temp_max <= 100.0', name='check_temp_max'),
    )

class CalibrationProfile(Base):
    """Calibration profiles table storing optimized fill parameters"""
    __tablename__ = 'calibration_profiles'
    
    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    upc_code = Column(String(13), ForeignKey('products.upc_code'), nullable=False)
    valve_timing = Column(Float, nullable=False)  # seconds
    pressure = Column(Float, nullable=False)       # PSI
    nozzle_diameter = Column(Float, nullable=False)  # mm
    target_volume = Column(Float, nullable=False)  # mL
    expected_accuracy = Column(Float)  # percentage
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    product = relationship("Product", back_populates="calibration_profiles")
    
    # Data validation constraints
    __table_args__ = (
        CheckConstraint('valve_timing >= 0.1 AND valve_timing <= 5.0', name='check_valve_timing'),
        CheckConstraint('pressure >= 10.0 AND pressure <= 100.0', name='check_pressure'),
        CheckConstraint('nozzle_diameter >= 2.0 AND nozzle_diameter <= 10.0', name='check_nozzle_diameter'),
        CheckConstraint('target_volume >= 10.0 AND target_volume <= 5000.0', name='check_target_volume'),
    )

class TrainingData(Base):
    """Training data table storing historical fill operations"""
    __tablename__ = 'training_data'
    
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    upc_code = Column(String(13), ForeignKey('products.upc_code'), nullable=False)
    valve_timing = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    nozzle_diameter = Column(Float, nullable=False)
    actual_volume = Column(Float, nullable=False)  # mL
    actual_time = Column(Float, nullable=False)    # seconds
    temperature = Column(Float)  # °C
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="training_data")

class ModelVersion(Base):
    """Model versions table tracking PINN model history"""
    __tablename__ = 'model_versions'
    
    version_id = Column(Integer, primary_key=True, autoincrement=True)
    version_name = Column(String(50), nullable=False, unique=True)
    training_samples = Column(Integer, nullable=False)
    validation_accuracy = Column(Float, nullable=False)
    is_active = Column(Boolean, default=False)
    model_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AnomalyLog(Base):
    """Anomaly log table storing detected fill anomalies"""
    __tablename__ = 'anomaly_log'
    
    anomaly_id = Column(Integer, primary_key=True, autoincrement=True)
    upc_code = Column(String(13), ForeignKey('products.upc_code'), nullable=False)
    predicted_volume = Column(Float, nullable=False)
    actual_volume = Column(Float, nullable=False)
    error_percentage = Column(Float, nullable=False)
    classification = Column(String(50))  # equipment/product/parameter
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="anomalies")
