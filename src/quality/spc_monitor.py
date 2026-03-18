"""
Statistical Process Control (SPC) Monitor
Feature 10: Real-time quality monitoring with control charts
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from collections import deque
from dataclasses import dataclass

@dataclass
class SPCAlert:
    """SPC rule violation alert"""
    rule_name: str
    severity: str  # warning/critical
    message: str
    data_points: List[float]
    timestamp: datetime
    recommended_action: str

@dataclass
class ControlLimits:
    """Control chart limits"""
    upper_control_limit: float  # UCL
    center_line: float  # Target
    lower_control_limit: float  # LCL
    upper_warning_limit: float  # 2 sigma
    lower_warning_limit: float  # 2 sigma

class SPCMonitor:
    """
    Statistical Process Control monitor implementing Western Electric rules.
    Detects process variations and out-of-control conditions.
    """
    
    def __init__(self, target_accuracy: float = 100.0, 
                 control_limit_sigma: float = 3.0):
        """
        Initialize SPC monitor.
        
        Args:
            target_accuracy: Target accuracy percentage (100 = perfect)
            control_limit_sigma: Number of standard deviations for control limits
        """
        self.target_accuracy = target_accuracy
        self.control_limit_sigma = control_limit_sigma
        
        # Data storage
        self.accuracy_data = deque(maxlen=100)  # Last 100 fills
        self.error_data = deque(maxlen=100)  # Error percentages
        
        # Control limits (will be calculated from data)
        self.control_limits = None
        
        # Alert history
        self.alert_history = deque(maxlen=50)
        
        # Rule violation counters
        self.consecutive_above_center = 0
        self.consecutive_below_center = 0
        self.consecutive_increasing = 0
        self.consecutive_decreasing = 0
    
    def log_fill_accuracy(self, actual_volume: float, target_volume: float,
                         timestamp: datetime = None):
        """
        Log fill accuracy for SPC monitoring.
        
        Args:
            actual_volume: Actual fill volume
            target_volume: Target fill volume
            timestamp: When fill occurred
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Calculate error percentage
        error_pct = (actual_volume - target_volume) / target_volume * 100.0
        accuracy = 100.0 - abs(error_pct)
        
        # Log data
        self.accuracy_data.append({
            'timestamp': timestamp,
            'accuracy': accuracy,
            'error': error_pct,
            'actual': actual_volume,
            'target': target_volume
        })
        
        self.error_data.append(error_pct)
        
        # Update control limits if we have enough data
        if len(self.accuracy_data) >= 20:
            self._calculate_control_limits()
    
    def _calculate_control_limits(self):
        """Calculate control limits from recent data"""
        errors = [d['error'] for d in self.accuracy_data]
        
        # Calculate mean and standard deviation
        mean_error = np.mean(errors)
        std_error = np.std(errors)
        
        # Control limits (3 sigma)
        ucl = mean_error + self.control_limit_sigma * std_error
        lcl = mean_error - self.control_limit_sigma * std_error
        
        # Warning limits (2 sigma)
        uwl = mean_error + 2 * std_error
        lwl = mean_error - 2 * std_error
        
        self.control_limits = ControlLimits(
            upper_control_limit=ucl,
            center_line=mean_error,
            lower_control_limit=lcl,
            upper_warning_limit=uwl,
            lower_warning_limit=lwl
        )
    
    def check_spc_rules(self) -> List[SPCAlert]:
        """
        Check all SPC rules and return violations.
        
        Implements Western Electric Rules:
        1. One point beyond 3 sigma (control limits)
        2. Two out of three consecutive points beyond 2 sigma
        3. Four out of five consecutive points beyond 1 sigma
        4. Seven consecutive points on one side of center
        5. Seven consecutive points trending up or down
        
        Returns:
            List of SPC alerts
        """
        alerts = []
        
        if self.control_limits is None or len(self.error_data) < 7:
            return alerts
        
        recent_errors = list(self.error_data)[-20:]  # Last 20 points
        
        # Rule 1: Point beyond control limits
        alert = self._check_rule_1(recent_errors)
        if alert:
            alerts.append(alert)
        
        # Rule 2: 2 out of 3 beyond 2 sigma
        alert = self._check_rule_2(recent_errors)
        if alert:
            alerts.append(alert)
        
        # Rule 3: 4 out of 5 beyond 1 sigma
        alert = self._check_rule_3(recent_errors)
        if alert:
            alerts.append(alert)
        
        # Rule 4: 7 consecutive on one side
        alert = self._check_rule_4(recent_errors)
        if alert:
            alerts.append(alert)
        
        # Rule 5: 7 consecutive trending
        alert = self._check_rule_5(recent_errors)
        if alert:
            alerts.append(alert)
        
        # Rule 6: 15 consecutive within 1 sigma (process too good - possible data manipulation)
        alert = self._check_rule_6(recent_errors)
        if alert:
            alerts.append(alert)
        
        # Store alerts
        for alert in alerts:
            self.alert_history.append(alert)
        
        return alerts
    
    def _check_rule_1(self, errors: List[float]) -> Optional[SPCAlert]:
        """Rule 1: One point beyond control limits"""
        last_error = errors[-1]
        
        if last_error > self.control_limits.upper_control_limit:
            return SPCAlert(
                rule_name="Rule 1: Beyond UCL",
                severity="critical",
                message=f"Fill error {last_error:.2f}% exceeds upper control limit {self.control_limits.upper_control_limit:.2f}%",
                data_points=[last_error],
                timestamp=datetime.now(),
                recommended_action="STOP: Investigate and correct immediately"
            )
        
        if last_error < self.control_limits.lower_control_limit:
            return SPCAlert(
                rule_name="Rule 1: Beyond LCL",
                severity="critical",
                message=f"Fill error {last_error:.2f}% below lower control limit {self.control_limits.lower_control_limit:.2f}%",
                data_points=[last_error],
                timestamp=datetime.now(),
                recommended_action="STOP: Investigate and correct immediately"
            )
        
        return None
    
    def _check_rule_2(self, errors: List[float]) -> Optional[SPCAlert]:
        """Rule 2: 2 out of 3 consecutive points beyond 2 sigma"""
        if len(errors) < 3:
            return None
        
        last_3 = errors[-3:]
        beyond_2sigma = sum(
            1 for e in last_3
            if e > self.control_limits.upper_warning_limit or 
               e < self.control_limits.lower_warning_limit
        )
        
        if beyond_2sigma >= 2:
            return SPCAlert(
                rule_name="Rule 2: 2/3 beyond 2σ",
                severity="warning",
                message=f"2 out of last 3 fills beyond warning limits",
                data_points=last_3,
                timestamp=datetime.now(),
                recommended_action="Investigate process variation"
            )
        
        return None
    
    def _check_rule_3(self, errors: List[float]) -> Optional[SPCAlert]:
        """Rule 3: 4 out of 5 consecutive points beyond 1 sigma"""
        if len(errors) < 5:
            return None
        
        last_5 = errors[-5:]
        std = (self.control_limits.upper_control_limit - self.control_limits.center_line) / 3
        
        beyond_1sigma = sum(
            1 for e in last_5
            if abs(e - self.control_limits.center_line) > std
        )
        
        if beyond_1sigma >= 4:
            return SPCAlert(
                rule_name="Rule 3: 4/5 beyond 1σ",
                severity="warning",
                message=f"4 out of last 5 fills show high variation",
                data_points=last_5,
                timestamp=datetime.now(),
                recommended_action="Check for process instability"
            )
        
        return None
    
    def _check_rule_4(self, errors: List[float]) -> Optional[SPCAlert]:
        """Rule 4: 7 consecutive points on one side of center"""
        if len(errors) < 7:
            return None
        
        last_7 = errors[-7:]
        center = self.control_limits.center_line
        
        all_above = all(e > center for e in last_7)
        all_below = all(e < center for e in last_7)
        
        if all_above:
            return SPCAlert(
                rule_name="Rule 4: 7 consecutive above center",
                severity="warning",
                message="Systematic overfilling detected",
                data_points=last_7,
                timestamp=datetime.now(),
                recommended_action="Reduce pressure or timing"
            )
        
        if all_below:
            return SPCAlert(
                rule_name="Rule 4: 7 consecutive below center",
                severity="warning",
                message="Systematic underfilling detected",
                data_points=last_7,
                timestamp=datetime.now(),
                recommended_action="Increase pressure or timing"
            )
        
        return None
    
    def _check_rule_5(self, errors: List[float]) -> Optional[SPCAlert]:
        """Rule 5: 7 consecutive points trending up or down"""
        if len(errors) < 7:
            return None
        
        last_7 = errors[-7:]
        
        # Check if monotonically increasing
        increasing = all(last_7[i] < last_7[i+1] for i in range(6))
        
        # Check if monotonically decreasing
        decreasing = all(last_7[i] > last_7[i+1] for i in range(6))
        
        if increasing:
            return SPCAlert(
                rule_name="Rule 5: 7 consecutive increasing",
                severity="warning",
                message="Continuous drift toward overfilling",
                data_points=last_7,
                timestamp=datetime.now(),
                recommended_action="Equipment degradation - check nozzle/valve"
            )
        
        if decreasing:
            return SPCAlert(
                rule_name="Rule 5: 7 consecutive decreasing",
                severity="warning",
                message="Continuous drift toward underfilling",
                data_points=last_7,
                timestamp=datetime.now(),
                recommended_action="Equipment degradation - check pump/pressure"
            )
        
        return None
    
    def _check_rule_6(self, errors: List[float]) -> Optional[SPCAlert]:
        """Rule 6: 15 consecutive points within 1 sigma (suspiciously good)"""
        if len(errors) < 15:
            return None
        
        last_15 = errors[-15:]
        std = (self.control_limits.upper_control_limit - self.control_limits.center_line) / 3
        center = self.control_limits.center_line
        
        all_within_1sigma = all(
            abs(e - center) < std for e in last_15
        )
        
        if all_within_1sigma:
            return SPCAlert(
                rule_name="Rule 6: Too consistent",
                severity="warning",
                message="Process variation suspiciously low",
                data_points=last_15,
                timestamp=datetime.now(),
                recommended_action="Verify sensors and data logging"
            )
        
        return None
    
    def get_control_chart_data(self) -> Dict:
        """
        Get data for plotting control chart.
        
        Returns:
            Dictionary with chart data and limits
        """
        if self.control_limits is None:
            return {'status': 'insufficient_data'}
        
        errors = [d['error'] for d in self.accuracy_data]
        timestamps = [d['timestamp'] for d in self.accuracy_data]
        
        return {
            'status': 'ok',
            'timestamps': timestamps,
            'errors': errors,
            'ucl': self.control_limits.upper_control_limit,
            'uwl': self.control_limits.upper_warning_limit,
            'center': self.control_limits.center_line,
            'lwl': self.control_limits.lower_warning_limit,
            'lcl': self.control_limits.lower_control_limit,
            'num_points': len(errors)
        }
    
    def get_process_capability(self) -> Dict:
        """
        Calculate process capability indices (Cp, Cpk).
        
        Returns:
            Dictionary with capability metrics
        """
        if len(self.error_data) < 30:
            return {'status': 'insufficient_data'}
        
        errors = list(self.error_data)
        
        # Specification limits (assume ±1% is acceptable)
        usl = 1.0  # Upper spec limit
        lsl = -1.0  # Lower spec limit
        
        # Process statistics
        mean = np.mean(errors)
        std = np.std(errors)
        
        # Cp: Process capability (how well process fits within specs)
        cp = (usl - lsl) / (6 * std) if std > 0 else 0
        
        # Cpk: Process capability accounting for centering
        cpu = (usl - mean) / (3 * std) if std > 0 else 0
        cpl = (mean - lsl) / (3 * std) if std > 0 else 0
        cpk = min(cpu, cpl)
        
        # Interpretation
        if cpk >= 1.33:
            capability = "Excellent"
        elif cpk >= 1.0:
            capability = "Adequate"
        elif cpk >= 0.67:
            capability = "Poor"
        else:
            capability = "Inadequate"
        
        return {
            'status': 'ok',
            'cp': cp,
            'cpk': cpk,
            'capability': capability,
            'mean_error': mean,
            'std_error': std,
            'interpretation': f"Cpk={cpk:.2f} indicates {capability} process capability"
        }
    
    def get_summary_statistics(self) -> Dict:
        """Get summary statistics for recent fills"""
        if len(self.accuracy_data) == 0:
            return {'status': 'no_data'}
        
        errors = [d['error'] for d in self.accuracy_data]
        accuracies = [d['accuracy'] for d in self.accuracy_data]
        
        return {
            'status': 'ok',
            'num_fills': len(errors),
            'mean_error': np.mean(errors),
            'std_error': np.std(errors),
            'min_error': np.min(errors),
            'max_error': np.max(errors),
            'mean_accuracy': np.mean(accuracies),
            'in_control': self.control_limits is not None and 
                         abs(errors[-1]) <= abs(self.control_limits.upper_control_limit)
        }
