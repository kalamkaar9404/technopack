"""
Application controller orchestrating calibration system components.
"""
import time
import logging
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductContext:
    """Context for currently active product"""
    def __init__(self, product, profile, status: str = "ready"):
        self.product = product
        self.profile = profile
        self.status = status

class PredictionResult:
    """Result of fill prediction"""
    def __init__(self, prediction, recommendation=None, alert=None):
        self.prediction = prediction
        self.recommendation = recommendation
        self.alert = alert

class FillExecution:
    """Result of fill execution"""
    def __init__(self, actual_volume: float, actual_time: float, anomaly_detected: bool = False):
        self.actual_volume = actual_volume
        self.actual_time = actual_time
        self.anomaly_detected = anomaly_detected

class CalibrationController:
    """
    Main controller orchestrating business logic and component coordination.
    Integrates vision detection, health monitoring, SPC, and anomaly database.
    """
    
    def __init__(self, database_layer, pinn_model, optimizer, config: Dict,
                 vision_detector=None, health_monitor=None, 
                 spc_monitor=None, anomaly_db=None):
        """
        Initialize controller with dependencies.
        
        Args:
            database_layer: DatabaseLayer instance
            pinn_model: PINNModel instance
            optimizer: CalibrationOptimizer instance
            config: System configuration dictionary
            vision_detector: FillLevelDetector instance (optional)
            health_monitor: EquipmentHealthMonitor instance (optional)
            spc_monitor: SPCMonitor instance (optional)
            anomaly_db: AnomalyDatabase instance (optional)
        """
        self.db = database_layer
        self.pinn_model = pinn_model
        self.optimizer = optimizer
        self.config = config
        
        # Advanced features
        self.vision_detector = vision_detector
        self.health_monitor = health_monitor
        self.spc_monitor = spc_monitor
        self.anomaly_db = anomaly_db
        
        # Thresholds from config
        self.acceptable_accuracy = config['thresholds']['acceptable_accuracy']
        self.prediction_warning = config['thresholds']['prediction_warning']
        self.anomaly_detection = config['thresholds']['anomaly_detection']
        self.retraining_trigger = config['thresholds']['retraining_trigger']
        
        # Product history (last 10 products)
        self.product_history = deque(maxlen=10)
        
        # Current context
        self.current_context = None
        
        # Anomaly counter for consecutive anomalies
        self.consecutive_anomalies = 0
        
        logger.info("CalibrationController initialized with advanced features")

    
    def handle_upc_scan(self, upc_code: str) -> ProductContext:
        """
        Process UPC scan: retrieve product, load profile, update UI context.
        
        Args:
            upc_code: Scanned UPC code
            
        Returns:
            ProductContext with product, profile, and status
        """
        start_time = time.time()
        
        # Retrieve product from database
        product = self.db.get_product(upc_code)
        
        if product is None:
            logger.warning(f"UPC code not found: {upc_code}")
            return ProductContext(None, None, "upc_not_found")
        
        # Load calibration profile
        profile = self.db.get_calibration_profile(upc_code)
        
        if profile is None:
            logger.info(f"No calibration profile found for {product.product_name}, generating...")
            # Generate new profile
            params, accuracy = self.optimizer.generate_profile(
                product.viscosity,
                product.density,
                product.surface_tension,
                25.0,  # Default temperature
                500.0  # Default target volume
            )
            
            # Save to database
            self.db.save_calibration_profile(
                upc_code,
                params['valve_timing'],
                params['pressure'],
                params['nozzle_diameter'],
                500.0,
                accuracy
            )
            
            # Reload profile
            profile = self.db.get_calibration_profile(upc_code)
        
        # Create context
        context = ProductContext(product, profile, "ready")
        self.current_context = context
        
        # Add to history
        self.product_history.append({
            'upc_code': upc_code,
            'product_name': product.product_name,
            'timestamp': datetime.now()
        })
        
        elapsed = (time.time() - start_time) * 1000
        logger.info(f"UPC scan processed in {elapsed:.2f}ms")
        
        return context

    
    def predict_fill(self, valve_timing: float, pressure: float, nozzle_diameter: float,
                    target_volume: float, temperature: float = 25.0) -> PredictionResult:
        """
        Generate fill prediction and check against thresholds.
        Also checks anomaly database for similar past issues.
        
        Args:
            valve_timing: Valve timing in seconds
            pressure: Pressure in PSI
            nozzle_diameter: Nozzle diameter in mm
            target_volume: Target volume in mL
            temperature: Temperature in °C
            
        Returns:
            PredictionResult with prediction, recommendation, and alert
        """
        start_time = time.time()
        
        if self.current_context is None or self.current_context.product is None:
            logger.error("No product context available")
            return PredictionResult(None, None, "No product selected")
        
        product = self.current_context.product
        
        # Get prediction from PINN
        pred_volume, pred_time, confidence, physics_valid = self.pinn_model.predict(
            valve_timing, pressure, nozzle_diameter,
            product.viscosity, product.density, product.surface_tension,
            temperature, target_volume
        )
        
        prediction = {
            'predicted_volume': pred_volume,
            'predicted_time': pred_time,
            'confidence': confidence,
            'physics_valid': physics_valid
        }
        
        # Calculate error
        error_pct = abs(pred_volume - target_volume) / target_volume * 100.0
        
        recommendation = None
        alert = None
        
        # Check anomaly database for similar conditions
        if self.anomaly_db:
            conditions = {
                'valve_timing': valve_timing,
                'pressure': pressure,
                'nozzle_diameter': nozzle_diameter
            }
            similar = self.anomaly_db.check_similar_anomalies(
                product.product_name, product.viscosity, temperature, conditions, top_k=3
            )
            
            if similar:
                logger.info(f"Found {len(similar)} similar past anomalies")
                prediction['similar_anomalies'] = similar
        
        # Check if error exceeds warning threshold
        if error_pct > self.prediction_warning:
            logger.warning(f"Prediction error {error_pct:.2f}% exceeds threshold")
            
            # Get parameter adjustment recommendation
            current_params = {
                'valve_timing': valve_timing,
                'pressure': pressure,
                'nozzle_diameter': nozzle_diameter
            }
            
            adjusted_params = self.optimizer.recommend_adjustment(
                current_params, pred_volume, target_volume,
                product.viscosity, product.density, product.surface_tension, temperature
            )
            
            recommendation = adjusted_params
            alert = f"Predicted error {error_pct:.2f}% exceeds {self.prediction_warning}% threshold"
        
        elapsed = (time.time() - start_time) * 1000
        logger.info(f"Fill prediction completed in {elapsed:.2f}ms")
        
        return PredictionResult(prediction, recommendation, alert)
    
    def execute_fill(self, valve_timing: float, pressure: float, nozzle_diameter: float,
                    target_volume: float, actual_volume: float, actual_time: float,
                    temperature: float = 25.0, camera_image=None) -> FillExecution:
        """
        Monitor fill execution, log data, detect anomalies.
        Integrates vision detection, health monitoring, and SPC.
        
        Args:
            valve_timing: Valve timing used
            pressure: Pressure used
            nozzle_diameter: Nozzle diameter used
            target_volume: Target volume
            actual_volume: Actual fill volume achieved
            actual_time: Actual fill time
            temperature: Temperature
            camera_image: Optional camera image for vision detection
            
        Returns:
            FillExecution with actual values and anomaly status
        """
        if self.current_context is None or self.current_context.product is None:
            logger.error("No product context available")
            return FillExecution(actual_volume, actual_time, False)
        
        product = self.current_context.product
        
        # Get prediction for comparison
        pred_volume, pred_time, _, _ = self.pinn_model.predict(
            valve_timing, pressure, nozzle_diameter,
            product.viscosity, product.density, product.surface_tension,
            temperature, target_volume
        )
        
        # Vision detection if available
        vision_result = None
        if self.vision_detector and camera_image is not None:
            vision_result = self.vision_detector.detect_fill_level(camera_image, target_volume)
            logger.info(f"Vision detected: {vision_result.detected_volume:.2f}mL (confidence: {vision_result.confidence:.2f})")
        
        # Calculate deviation from prediction
        deviation_pct = abs(actual_volume - pred_volume) / pred_volume * 100.0 if pred_volume > 0 else 0.0
        
        # Log training data
        self.db.log_training_data(
            product.upc_code,
            valve_timing,
            pressure,
            nozzle_diameter,
            actual_volume,
            actual_time,
            temperature
        )
        
        # Log to health monitor
        if self.health_monitor:
            params = {
                'valve_timing': valve_timing,
                'pressure': pressure,
                'nozzle_diameter': nozzle_diameter
            }
            self.health_monitor.log_fill_result(
                pred_volume, actual_volume, target_volume, params
            )
        
        # Log to SPC monitor
        if self.spc_monitor:
            self.spc_monitor.log_fill_accuracy(actual_volume, target_volume)
        
        # Check for anomaly
        anomaly_detected = False
        if deviation_pct > self.anomaly_detection:
            anomaly_detected = True
            self.consecutive_anomalies += 1
            
            # Log anomaly
            error_pct = abs(actual_volume - target_volume) / target_volume * 100.0
            self.db.log_anomaly(
                product.upc_code,
                pred_volume,
                actual_volume,
                error_pct,
                "parameter"  # Simplified classification
            )
            
            logger.warning(f"Anomaly detected: {deviation_pct:.2f}% deviation")
            
            # Check for consecutive anomalies
            if self.consecutive_anomalies >= 3:
                logger.error("3 consecutive anomalies detected - maintenance recommended")
        else:
            self.consecutive_anomalies = 0
        
        # Check if retraining needed
        training_count = len(self.db.get_training_data(product.upc_code, limit=self.retraining_trigger))
        if training_count >= self.retraining_trigger:
            logger.info(f"Retraining threshold reached: {training_count} samples")
        
        execution = FillExecution(actual_volume, actual_time, anomaly_detected)
        execution.vision_result = vision_result
        
        return execution
    
    def switch_product(self, new_upc: str, current_upc: str) -> Tuple[ProductContext, bool]:
        """
        Handle product changeover with cleaning prompt if needed.
        
        Args:
            new_upc: New product UPC code
            current_upc: Current product UPC code
            
        Returns:
            Tuple of (new_context, cleaning_required)
        """
        start_time = time.time()
        
        # Get current and new products
        current_product = self.db.get_product(current_upc) if current_upc else None
        new_product = self.db.get_product(new_upc)
        
        if new_product is None:
            return ProductContext(None, None, "upc_not_found"), False
        
        cleaning_required = False
        
        # Check if properties differ significantly (>20%)
        if current_product:
            viscosity_diff = abs(new_product.viscosity - current_product.viscosity) / current_product.viscosity
            density_diff = abs(new_product.density - current_product.density) / current_product.density
            
            if viscosity_diff > 0.2 or density_diff > 0.2:
                cleaning_required = True
                logger.info("Significant property change detected - cleaning recommended")
        
        # Load new context
        new_context = self.handle_upc_scan(new_upc)
        
        elapsed = (time.time() - start_time) * 1000
        logger.info(f"Product switch completed in {elapsed:.2f}ms")
        
        return new_context, cleaning_required
    
    def get_health_alerts(self):
        """Get current equipment health alerts"""
        if self.health_monitor:
            return self.health_monitor.check_for_alerts()
        return []
    
    def get_health_status(self):
        """Get equipment health status"""
        if self.health_monitor:
            return self.health_monitor.get_health_status()
        return {}
    
    def get_maintenance_schedule(self):
        """Get maintenance schedule"""
        if self.health_monitor:
            return self.health_monitor.get_maintenance_schedule()
        return []
    
    def get_spc_alerts(self):
        """Get SPC rule violations"""
        if self.spc_monitor:
            return self.spc_monitor.check_spc_rules()
        return []
    
    def get_spc_chart_data(self):
        """Get control chart data"""
        if self.spc_monitor:
            return self.spc_monitor.get_control_chart_data()
        return {'status': 'not_available'}
    
    def get_process_capability(self):
        """Get process capability metrics"""
        if self.spc_monitor:
            return self.spc_monitor.get_process_capability()
        return {'status': 'not_available'}
    
    def search_anomaly_solutions(self, issue_type: str):
        """Search anomaly database for solutions"""
        if self.anomaly_db:
            return self.anomaly_db.get_top_solutions(issue_type)
        return []
    
    def report_anomaly_to_db(self, issue_type: str, solution: str, effectiveness: float):
        """Report anomaly to global database"""
        if self.anomaly_db and self.current_context and self.current_context.product:
            product = self.current_context.product
            profile = self.current_context.profile
            
            conditions = {
                'valve_timing': profile.valve_timing if profile else 0,
                'pressure': profile.pressure if profile else 0,
                'nozzle_diameter': profile.nozzle_diameter if profile else 0
            }
            
            return self.anomaly_db.report_anomaly(
                product.product_name,
                product.viscosity,
                25.0,  # Default temperature
                issue_type,
                conditions,
                solution,
                effectiveness
            )
        return None
