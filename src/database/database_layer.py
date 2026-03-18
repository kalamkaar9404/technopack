"""
Database layer providing CRUD operations for the calibration system.
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, Product, CalibrationProfile, TrainingData, ModelVersion, AnomalyLog

class DatabaseLayer:
    """Database layer for managing calibration system data"""
    
    def __init__(self, db_path: str):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def initialize_database(self):
        """Create all tables if they don't exist"""
        Base.metadata.create_all(self.engine)
    
    def _get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    # Product operations
    def get_product(self, upc_code: str) -> Optional[Product]:
        """
        Retrieve product by UPC code.
        
        Args:
            upc_code: UPC code to search for
            
        Returns:
            Product object if found, None otherwise
        """
        session = self._get_session()
        try:
            return session.query(Product).filter(Product.upc_code == upc_code).first()
        finally:
            session.close()
    
    def add_product(self, upc_code: str, product_name: str, viscosity: float,
                   density: float, surface_tension: float, 
                   temp_min: Optional[float] = None, 
                   temp_max: Optional[float] = None) -> bool:
        """
        Add new product to database.
        
        Args:
            upc_code: UPC code
            product_name: Product name
            viscosity: Viscosity in Pa·s
            density: Density in kg/m³
            surface_tension: Surface tension in N/m
            temp_min: Minimum temperature in °C
            temp_max: Maximum temperature in °C
            
        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            product = Product(
                upc_code=upc_code,
                product_name=product_name,
                viscosity=viscosity,
                density=density,
                surface_tension=surface_tension,
                temp_min=temp_min,
                temp_max=temp_max
            )
            session.add(product)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error adding product: {e}")
            return False
        finally:
            session.close()
    
    # Calibration profile operations
    def get_calibration_profile(self, upc_code: str) -> Optional[CalibrationProfile]:
        """
        Get active calibration profile for product.
        
        Args:
            upc_code: UPC code of product
            
        Returns:
            Active CalibrationProfile if found, None otherwise
        """
        session = self._get_session()
        try:
            return session.query(CalibrationProfile).filter(
                CalibrationProfile.upc_code == upc_code,
                CalibrationProfile.is_active == True
            ).first()
        finally:
            session.close()
    
    def save_calibration_profile(self, upc_code: str, valve_timing: float,
                                pressure: float, nozzle_diameter: float,
                                target_volume: float, 
                                expected_accuracy: Optional[float] = None) -> int:
        """
        Save calibration profile.
        
        Args:
            upc_code: UPC code of product
            valve_timing: Valve timing in seconds
            pressure: Pressure in PSI
            nozzle_diameter: Nozzle diameter in mm
            target_volume: Target volume in mL
            expected_accuracy: Expected accuracy percentage
            
        Returns:
            Profile ID of saved profile
        """
        session = self._get_session()
        try:
            # Deactivate existing profiles for this product
            session.query(CalibrationProfile).filter(
                CalibrationProfile.upc_code == upc_code
            ).update({CalibrationProfile.is_active: False})
            
            # Create new profile
            profile = CalibrationProfile(
                upc_code=upc_code,
                valve_timing=valve_timing,
                pressure=pressure,
                nozzle_diameter=nozzle_diameter,
                target_volume=target_volume,
                expected_accuracy=expected_accuracy,
                is_active=True
            )
            session.add(profile)
            session.commit()
            return profile.profile_id
        except Exception as e:
            session.rollback()
            print(f"Error saving calibration profile: {e}")
            return -1
        finally:
            session.close()
    
    # Training data operations
    def log_training_data(self, upc_code: str, valve_timing: float, pressure: float,
                         nozzle_diameter: float, actual_volume: float, 
                         actual_time: float, temperature: Optional[float] = None) -> None:
        """
        Persist fill operation data for model training.
        
        Args:
            upc_code: UPC code of product
            valve_timing: Valve timing in seconds
            pressure: Pressure in PSI
            nozzle_diameter: Nozzle diameter in mm
            actual_volume: Actual fill volume in mL
            actual_time: Actual fill time in seconds
            temperature: Temperature in °C
        """
        session = self._get_session()
        try:
            record = TrainingData(
                upc_code=upc_code,
                valve_timing=valve_timing,
                pressure=pressure,
                nozzle_diameter=nozzle_diameter,
                actual_volume=actual_volume,
                actual_time=actual_time,
                temperature=temperature
            )
            session.add(record)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error logging training data: {e}")
        finally:
            session.close()
    
    def get_training_data(self, upc_code: Optional[str] = None, 
                         limit: int = 1000) -> List[TrainingData]:
        """
        Retrieve training data, optionally filtered by product.
        
        Args:
            upc_code: Optional UPC code to filter by
            limit: Maximum number of records to return
            
        Returns:
            List of TrainingData records
        """
        session = self._get_session()
        try:
            query = session.query(TrainingData)
            if upc_code:
                query = query.filter(TrainingData.upc_code == upc_code)
            return query.order_by(TrainingData.timestamp.desc()).limit(limit).all()
        finally:
            session.close()
    
    # Anomaly operations
    def log_anomaly(self, upc_code: str, predicted_volume: float, 
                   actual_volume: float, error_percentage: float,
                   classification: Optional[str] = None) -> None:
        """
        Record anomaly for analysis.
        
        Args:
            upc_code: UPC code of product
            predicted_volume: Predicted fill volume in mL
            actual_volume: Actual fill volume in mL
            error_percentage: Error percentage
            classification: Anomaly classification (equipment/product/parameter)
        """
        session = self._get_session()
        try:
            anomaly = AnomalyLog(
                upc_code=upc_code,
                predicted_volume=predicted_volume,
                actual_volume=actual_volume,
                error_percentage=error_percentage,
                classification=classification
            )
            session.add(anomaly)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error logging anomaly: {e}")
        finally:
            session.close()
    
    # Model version operations
    def get_model_version(self, version_name: str) -> Optional[ModelVersion]:
        """
        Retrieve model version metadata.
        
        Args:
            version_name: Name of model version
            
        Returns:
            ModelVersion object if found, None otherwise
        """
        session = self._get_session()
        try:
            return session.query(ModelVersion).filter(
                ModelVersion.version_name == version_name
            ).first()
        finally:
            session.close()
    
    def get_active_model_version(self) -> Optional[ModelVersion]:
        """Get the currently active model version"""
        session = self._get_session()
        try:
            return session.query(ModelVersion).filter(
                ModelVersion.is_active == True
            ).first()
        finally:
            session.close()
    
    def save_model_version(self, version_name: str, training_samples: int,
                          validation_accuracy: float, model_path: str,
                          set_active: bool = False) -> int:
        """
        Save model version metadata.
        
        Args:
            version_name: Name of model version
            training_samples: Number of training samples used
            validation_accuracy: Validation accuracy percentage
            model_path: Path to model file
            set_active: Whether to set this as active model
            
        Returns:
            Version ID of saved model
        """
        session = self._get_session()
        try:
            if set_active:
                # Deactivate all existing models
                session.query(ModelVersion).update({ModelVersion.is_active: False})
            
            version = ModelVersion(
                version_name=version_name,
                training_samples=training_samples,
                validation_accuracy=validation_accuracy,
                model_path=model_path,
                is_active=set_active
            )
            session.add(version)
            session.commit()
            return version.version_id
        except Exception as e:
            session.rollback()
            print(f"Error saving model version: {e}")
            return -1
        finally:
            session.close()
