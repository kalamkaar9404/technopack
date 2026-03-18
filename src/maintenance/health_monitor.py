"""
Equipment Health Monitoring System
Feature 5: Predictive maintenance through accuracy trend analysis
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import deque
from dataclasses import dataclass

@dataclass
class HealthAlert:
    """Equipment health alert"""
    severity: str  # info/warning/critical
    component: str  # nozzle/valve/pump/sensor
    message: str
    recommended_action: str
    days_until_failure: Optional[int]
    timestamp: datetime

@dataclass
class ComponentHealth:
    """Health status of a component"""
    component_name: str
    health_score: float  # 0-100
    accuracy_trend: List[float]
    predicted_failure_date: Optional[datetime]
    maintenance_recommended: bool

class EquipmentHealthMonitor:
    """
    Monitors equipment health by tracking accuracy trends and detecting degradation.
    Predicts component failures before they cause production issues.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize health monitor.
        
        Args:
            config: Configuration with thresholds and parameters
        """
        self.config = config
        
        # Tracking windows
        self.accuracy_history = deque(maxlen=1000)  # Last 1000 fills
        self.daily_accuracy = deque(maxlen=30)  # Last 30 days
        
        # Component tracking
        self.component_metrics = {
            'nozzle': deque(maxlen=100),
            'valve': deque(maxlen=100),
            'pump': deque(maxlen=100),
            'pressure_sensor': deque(maxlen=100)
        }
        
        # Thresholds
        self.warning_threshold = 98.0  # 98% accuracy
        self.critical_threshold = 95.0  # 95% accuracy
        self.degradation_rate_threshold = 0.5  # 0.5% per week
        
        # Alerts
        self.active_alerts = []
    
    def log_fill_result(self, predicted_volume: float, actual_volume: float,
                       target_volume: float, parameters: Dict,
                       timestamp: datetime = None):
        """
        Log fill result for health monitoring.
        
        Args:
            predicted_volume: PINN predicted volume
            actual_volume: Actual fill volume
            target_volume: Target volume
            parameters: Fill parameters used
            timestamp: When fill occurred
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Calculate accuracy
        error_pct = abs(actual_volume - target_volume) / target_volume * 100.0
        accuracy = 100.0 - error_pct
        
        # Log to history
        self.accuracy_history.append({
            'timestamp': timestamp,
            'accuracy': accuracy,
            'predicted_volume': predicted_volume,
            'actual_volume': actual_volume,
            'target_volume': target_volume,
            'parameters': parameters
        })
        
        # Analyze component-specific metrics
        self._analyze_component_health(parameters, accuracy, 
                                       predicted_volume, actual_volume)
    
    def _analyze_component_health(self, parameters: Dict, accuracy: float,
                                  predicted: float, actual: float):
        """Analyze which component might be degrading"""
        
        # Nozzle health: Affected by viscosity and flow rate
        if 'pressure' in parameters and 'nozzle_diameter' in parameters:
            flow_deviation = abs(actual - predicted) / predicted
            self.component_metrics['nozzle'].append({
                'accuracy': accuracy,
                'flow_deviation': flow_deviation,
                'pressure': parameters['pressure']
            })
        
        # Valve health: Affected by timing accuracy
        if 'valve_timing' in parameters:
            self.component_metrics['valve'].append({
                'accuracy': accuracy,
                'timing': parameters['valve_timing']
            })
        
        # Pump health: Affected by pressure stability
        if 'pressure' in parameters:
            self.component_metrics['pump'].append({
                'accuracy': accuracy,
                'pressure': parameters['pressure']
            })
        
        # Sensor health: Prediction vs actual deviation
        prediction_error = abs(predicted - actual) / actual * 100.0
        self.component_metrics['pressure_sensor'].append({
            'prediction_error': prediction_error
        })
    
    def get_health_status(self) -> Dict[str, ComponentHealth]:
        """
        Get current health status of all components.
        
        Returns:
            Dictionary of component health statuses
        """
        health_status = {}
        
        for component, metrics in self.component_metrics.items():
            if len(metrics) < 10:
                # Not enough data
                health_status[component] = ComponentHealth(
                    component_name=component,
                    health_score=100.0,
                    accuracy_trend=[],
                    predicted_failure_date=None,
                    maintenance_recommended=False
                )
                continue
            
            # Calculate health score
            health_score = self._calculate_health_score(component, metrics)
            
            # Get accuracy trend
            accuracy_trend = [m.get('accuracy', 100.0) for m in metrics if 'accuracy' in m]
            
            # Predict failure date
            failure_date = self._predict_failure_date(accuracy_trend)
            
            # Maintenance recommendation
            maintenance_needed = health_score < self.warning_threshold
            
            health_status[component] = ComponentHealth(
                component_name=component,
                health_score=health_score,
                accuracy_trend=accuracy_trend[-10:],  # Last 10 readings
                predicted_failure_date=failure_date,
                maintenance_recommended=maintenance_needed
            )
        
        return health_status
    
    def _calculate_health_score(self, component: str, metrics: deque) -> float:
        """Calculate health score (0-100) for a component"""
        
        if component == 'nozzle':
            # Nozzle health based on flow deviation
            flow_devs = [m.get('flow_deviation', 0) for m in metrics if 'flow_deviation' in m]
            if flow_devs:
                avg_deviation = np.mean(flow_devs)
                # 0% deviation = 100 score, 10% deviation = 0 score
                score = max(0, 100 - avg_deviation * 1000)
                return score
        
        elif component == 'valve':
            # Valve health based on timing accuracy
            accuracies = [m.get('accuracy', 100) for m in metrics if 'accuracy' in m]
            if accuracies:
                return np.mean(accuracies)
        
        elif component == 'pump':
            # Pump health based on pressure stability
            pressures = [m.get('pressure', 0) for m in metrics if 'pressure' in m]
            if len(pressures) > 1:
                pressure_std = np.std(pressures)
                # Low std = stable = healthy
                score = max(0, 100 - pressure_std * 2)
                return score
        
        elif component == 'pressure_sensor':
            # Sensor health based on prediction errors
            errors = [m.get('prediction_error', 0) for m in metrics if 'prediction_error' in m]
            if errors:
                avg_error = np.mean(errors)
                score = max(0, 100 - avg_error * 10)
                return score
        
        return 100.0
    
    def _predict_failure_date(self, accuracy_trend: List[float]) -> Optional[datetime]:
        """
        Predict when component will fail based on accuracy trend.
        
        Returns:
            Predicted failure date or None if no degradation detected
        """
        if len(accuracy_trend) < 10:
            return None
        
        # Linear regression to find degradation rate
        x = np.arange(len(accuracy_trend))
        y = np.array(accuracy_trend)
        
        # Fit line
        coeffs = np.polyfit(x, y, 1)
        slope = coeffs[0]  # Degradation rate per reading
        
        # If not degrading, no failure predicted
        if slope >= 0:
            return None
        
        # Current accuracy
        current_accuracy = accuracy_trend[-1]
        
        # Readings until failure (when accuracy drops below critical threshold)
        readings_until_failure = (current_accuracy - self.critical_threshold) / abs(slope)
        
        if readings_until_failure <= 0:
            return datetime.now()  # Already failed
        
        # Assume 100 fills per day
        days_until_failure = readings_until_failure / 100
        
        if days_until_failure > 365:
            return None  # Too far in future to be meaningful
        
        failure_date = datetime.now() + timedelta(days=days_until_failure)
        return failure_date
    
    def check_for_alerts(self) -> List[HealthAlert]:
        """
        Check for health alerts and return active alerts.
        
        Returns:
            List of active health alerts
        """
        alerts = []
        
        # Get health status
        health_status = self.get_health_status()
        
        for component, health in health_status.items():
            # Critical alert
            if health.health_score < self.critical_threshold:
                alerts.append(HealthAlert(
                    severity='critical',
                    component=component,
                    message=f"{component.title()} health critical: {health.health_score:.1f}%",
                    recommended_action=f"IMMEDIATE: Replace {component}",
                    days_until_failure=0,
                    timestamp=datetime.now()
                ))
            
            # Warning alert
            elif health.health_score < self.warning_threshold:
                days_until_failure = None
                if health.predicted_failure_date:
                    days_until_failure = (health.predicted_failure_date - datetime.now()).days
                
                alerts.append(HealthAlert(
                    severity='warning',
                    component=component,
                    message=f"{component.title()} health degrading: {health.health_score:.1f}%",
                    recommended_action=f"Schedule {component} maintenance",
                    days_until_failure=days_until_failure,
                    timestamp=datetime.now()
                ))
            
            # Predictive alert
            elif health.predicted_failure_date:
                days_until_failure = (health.predicted_failure_date - datetime.now()).days
                
                if days_until_failure < 30:
                    alerts.append(HealthAlert(
                        severity='info',
                        component=component,
                        message=f"{component.title()} maintenance due in {days_until_failure} days",
                        recommended_action=f"Plan {component} replacement",
                        days_until_failure=days_until_failure,
                        timestamp=datetime.now()
                    ))
        
        self.active_alerts = alerts
        return alerts
    
    def get_maintenance_schedule(self) -> List[Dict]:
        """
        Generate maintenance schedule based on component health.
        
        Returns:
            List of maintenance tasks with priorities
        """
        schedule = []
        health_status = self.get_health_status()
        
        for component, health in health_status.items():
            if health.maintenance_recommended:
                priority = 'high' if health.health_score < self.critical_threshold else 'medium'
                
                schedule.append({
                    'component': component,
                    'priority': priority,
                    'health_score': health.health_score,
                    'recommended_date': health.predicted_failure_date or datetime.now(),
                    'action': f"Inspect and service {component}"
                })
        
        # Sort by priority and date
        schedule.sort(key=lambda x: (
            0 if x['priority'] == 'high' else 1,
            x['recommended_date']
        ))
        
        return schedule
    
    def get_accuracy_trend_report(self, days: int = 7) -> Dict:
        """
        Generate accuracy trend report for specified period.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend analysis
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent data
        recent_data = [
            entry for entry in self.accuracy_history
            if entry['timestamp'] >= cutoff_date
        ]
        
        if len(recent_data) < 10:
            return {
                'status': 'insufficient_data',
                'message': f'Need at least 10 fills in last {days} days'
            }
        
        # Calculate statistics
        accuracies = [entry['accuracy'] for entry in recent_data]
        
        mean_accuracy = np.mean(accuracies)
        std_accuracy = np.std(accuracies)
        min_accuracy = np.min(accuracies)
        max_accuracy = np.max(accuracies)
        
        # Detect trend
        x = np.arange(len(accuracies))
        coeffs = np.polyfit(x, accuracies, 1)
        trend_slope = coeffs[0]
        
        if trend_slope < -self.degradation_rate_threshold:
            trend = 'degrading'
        elif trend_slope > self.degradation_rate_threshold:
            trend = 'improving'
        else:
            trend = 'stable'
        
        return {
            'status': 'ok',
            'period_days': days,
            'num_fills': len(recent_data),
            'mean_accuracy': mean_accuracy,
            'std_accuracy': std_accuracy,
            'min_accuracy': min_accuracy,
            'max_accuracy': max_accuracy,
            'trend': trend,
            'trend_slope': trend_slope,
            'health_status': 'good' if mean_accuracy >= self.warning_threshold else 'degraded'
        }
