"""
Calibration optimizer for generating and refining calibration profiles.
"""
import numpy as np
from typing import Tuple, Dict, List
from scipy.optimize import minimize
import itertools

class CalibrationOptimizer:
    """
    Optimizer for generating calibration profiles by searching parameter space.
    """
    
    def __init__(self, pinn_model, config: Dict):
        """
        Initialize calibration optimizer.
        
        Args:
            pinn_model: Trained PINN model for predictions
            config: Configuration dictionary with parameter ranges and optimization settings
        """
        self.pinn_model = pinn_model
        self.config = config
        
        # Parameter ranges
        self.param_ranges = config['calibration']['parameter_ranges']
        self.valve_timing_range = tuple(self.param_ranges['valve_timing'])
        self.pressure_range = tuple(self.param_ranges['pressure'])
        self.nozzle_diameter_range = tuple(self.param_ranges['nozzle_diameter'])
        
        # Optimization settings
        self.opt_config = config['calibration']['optimization']
        self.grid_resolution = self.opt_config['grid_resolution']
        self.max_iterations = self.opt_config['max_iterations']
        self.convergence_tolerance = self.opt_config['convergence_tolerance']
        
        # Physics tolerance
        self.physics_tolerance = 0.05  # 5% residual threshold
    
    def generate_profile(self, viscosity: float, density: float, 
                        surface_tension: float, temperature: float,
                        target_volume: float) -> Tuple[Dict, float]:
        """
        Generate optimal calibration profile for new product.
        
        Args:
            viscosity: Product viscosity in Pa·s
            density: Product density in kg/m³
            surface_tension: Product surface tension in N/m
            temperature: Operating temperature in °C
            target_volume: Target fill volume in mL
            
        Returns:
            Tuple of (optimal_parameters_dict, expected_accuracy)
        """
        print(f"Generating calibration profile for target volume: {target_volume} mL")
        
        # Step 1: Coarse grid search
        best_params, best_error = self._grid_search(
            viscosity, density, surface_tension, temperature, target_volume
        )
        
        print(f"Grid search complete. Best error: {best_error:.4f}%")
        
        # Step 2: Fine-tune with gradient-based optimization
        optimal_params, final_error = self._gradient_optimization(
            best_params, viscosity, density, surface_tension, temperature, target_volume
        )
        
        print(f"Optimization complete. Final error: {final_error:.4f}%")
        
        # Clip parameters to valid ranges
        optimal_params = self._clip_parameters(optimal_params)
        
        # Calculate expected accuracy
        expected_accuracy = 100.0 - final_error
        
        param_dict = {
            'valve_timing': optimal_params[0],
            'pressure': optimal_params[1],
            'nozzle_diameter': optimal_params[2]
        }
        
        return param_dict, expected_accuracy
    
    def _grid_search(self, viscosity: float, density: float, surface_tension: float,
                    temperature: float, target_volume: float) -> Tuple[np.ndarray, float]:
        """
        Perform coarse grid search over parameter space.
        
        Returns:
            Tuple of (best_parameters, best_error_percentage)
        """
        # Create grid
        valve_timings = np.linspace(self.valve_timing_range[0], 
                                    self.valve_timing_range[1], 
                                    self.grid_resolution)
        pressures = np.linspace(self.pressure_range[0], 
                               self.pressure_range[1], 
                               self.grid_resolution)
        nozzle_diameters = np.linspace(self.nozzle_diameter_range[0], 
                                       self.nozzle_diameter_range[1], 
                                       self.grid_resolution)
        
        best_error = float('inf')
        best_params = None
        evaluated_count = 0
        
        # Evaluate all combinations
        for vt, p, nd in itertools.product(valve_timings, pressures, nozzle_diameters):
            # Predict with PINN
            pred_volume, pred_time, confidence, physics_valid = self.pinn_model.predict(
                vt, p, nd, viscosity, density, surface_tension, temperature, target_volume
            )
            
            # Skip if physics constraints violated
            if not physics_valid:
                continue
            
            # Calculate error
            error = abs(pred_volume - target_volume) / target_volume * 100.0
            
            if error < best_error:
                best_error = error
                best_params = np.array([vt, p, nd])
            
            evaluated_count += 1
        
        print(f"Evaluated {evaluated_count} parameter combinations")
        
        if best_params is None:
            # Fallback to center of parameter space
            best_params = np.array([
                np.mean(self.valve_timing_range),
                np.mean(self.pressure_range),
                np.mean(self.nozzle_diameter_range)
            ])
            best_error = 10.0  # Assume 10% error for fallback
        
        return best_params, best_error
    
    def _gradient_optimization(self, initial_params: np.ndarray,
                              viscosity: float, density: float, surface_tension: float,
                              temperature: float, target_volume: float) -> Tuple[np.ndarray, float]:
        """
        Fine-tune parameters using gradient-based optimization.
        
        Returns:
            Tuple of (optimal_parameters, final_error_percentage)
        """
        def objective(params):
            """Objective function to minimize"""
            vt, p, nd = params
            
            # Predict with PINN
            pred_volume, _, _, physics_valid = self.pinn_model.predict(
                vt, p, nd, viscosity, density, surface_tension, temperature, target_volume
            )
            
            # Penalize physics violations
            if not physics_valid:
                return 1000.0
            
            # Return absolute error
            return abs(pred_volume - target_volume)
        
        # Bounds for parameters
        bounds = [
            self.valve_timing_range,
            self.pressure_range,
            self.nozzle_diameter_range
        ]
        
        # Optimize
        result = minimize(
            objective,
            initial_params,
            method='L-BFGS-B',
            bounds=bounds,
            options={'maxiter': self.max_iterations}
        )
        
        optimal_params = result.x
        final_error = result.fun / target_volume * 100.0
        
        return optimal_params, final_error
    
    def _clip_parameters(self, params: np.ndarray) -> np.ndarray:
        """Clip parameters to valid ranges"""
        clipped = np.array([
            np.clip(params[0], self.valve_timing_range[0], self.valve_timing_range[1]),
            np.clip(params[1], self.pressure_range[0], self.pressure_range[1]),
            np.clip(params[2], self.nozzle_diameter_range[0], self.nozzle_diameter_range[1])
        ])
        return clipped

    
    def refine_profile(self, current_params: Dict, recent_fill_data: List[Dict],
                      viscosity: float, density: float, surface_tension: float,
                      temperature: float, target_volume: float) -> Tuple[Dict, float]:
        """
        Refine existing profile based on actual fill data.
        
        Args:
            current_params: Current calibration parameters
            recent_fill_data: List of recent fill records with actual volumes
            viscosity: Product viscosity
            density: Product density
            surface_tension: Product surface tension
            temperature: Operating temperature
            target_volume: Target fill volume
            
        Returns:
            Tuple of (refined_parameters_dict, expected_accuracy)
        """
        if not recent_fill_data:
            return current_params, 99.0
        
        # Calculate average error from recent fills
        total_error = 0.0
        for fill in recent_fill_data:
            actual_volume = fill['actual_volume']
            error = abs(actual_volume - target_volume) / target_volume * 100.0
            total_error += error
        
        avg_error = total_error / len(recent_fill_data)
        
        # If error is acceptable, keep current parameters
        if avg_error <= self.convergence_tolerance * 100:
            return current_params, 100.0 - avg_error
        
        # Otherwise, re-optimize starting from current parameters
        initial_params = np.array([
            current_params['valve_timing'],
            current_params['pressure'],
            current_params['nozzle_diameter']
        ])
        
        optimal_params, final_error = self._gradient_optimization(
            initial_params, viscosity, density, surface_tension, temperature, target_volume
        )
        
        optimal_params = self._clip_parameters(optimal_params)
        
        refined_dict = {
            'valve_timing': optimal_params[0],
            'pressure': optimal_params[1],
            'nozzle_diameter': optimal_params[2]
        }
        
        expected_accuracy = 100.0 - final_error
        
        return refined_dict, expected_accuracy

    
    def recommend_adjustment(self, current_params: Dict, predicted_volume: float,
                           target_volume: float, viscosity: float, density: float,
                           surface_tension: float, temperature: float) -> Dict:
        """
        Suggest parameter adjustments when prediction exceeds error threshold.
        
        Args:
            current_params: Current fill parameters
            predicted_volume: Predicted fill volume
            target_volume: Target fill volume
            viscosity: Product viscosity
            density: Product density
            surface_tension: Product surface tension
            temperature: Operating temperature
            
        Returns:
            Dictionary of adjusted parameters
        """
        error = predicted_volume - target_volume
        error_percentage = abs(error) / target_volume * 100.0
        
        # Scale adjustment based on error magnitude
        adjustment_scale = min(error_percentage / 10.0, 0.5)  # Max 50% adjustment
        
        # Start with current parameters
        adjusted = current_params.copy()
        
        if error > 0:  # Overfilling
            # Reduce valve timing or pressure
            adjusted['valve_timing'] = max(
                self.valve_timing_range[0],
                current_params['valve_timing'] * (1.0 - adjustment_scale * 0.1)
            )
            adjusted['pressure'] = max(
                self.pressure_range[0],
                current_params['pressure'] * (1.0 - adjustment_scale * 0.1)
            )
        else:  # Underfilling
            # Increase valve timing or pressure
            adjusted['valve_timing'] = min(
                self.valve_timing_range[1],
                current_params['valve_timing'] * (1.0 + adjustment_scale * 0.1)
            )
            adjusted['pressure'] = min(
                self.pressure_range[1],
                current_params['pressure'] * (1.0 + adjustment_scale * 0.1)
            )
        
        # Verify adjusted parameters with PINN
        pred_volume, _, _, physics_valid = self.pinn_model.predict(
            adjusted['valve_timing'],
            adjusted['pressure'],
            adjusted['nozzle_diameter'],
            viscosity, density, surface_tension, temperature, target_volume
        )
        
        # If physics invalid, return original parameters
        if not physics_valid:
            return current_params
        
        return adjusted
