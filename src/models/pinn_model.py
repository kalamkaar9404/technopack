"""
Physics-Informed Neural Network (PINN) model for liquid filling prediction.
"""
import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, List, Dict
from pathlib import Path

class PINNModel(nn.Module):
    """
    Physics-Informed Neural Network for predicting fill outcomes.
    
    Architecture: 8 inputs → 6 hidden layers (32 neurons each) → 2 outputs
    Physics constraints: Navier-Stokes and continuity equations
    """
    
    def __init__(self, hidden_layers: int = 6, neurons_per_layer: int = 32):
        """
        Initialize PINN model.
        
        Args:
            hidden_layers: Number of hidden layers
            neurons_per_layer: Neurons per hidden layer
        """
        super(PINNModel, self).__init__()
        
        self.hidden_layers = hidden_layers
        self.neurons_per_layer = neurons_per_layer
        
        # Input: 8 features (valve_timing, pressure, nozzle_diameter, 
        #                    viscosity, density, surface_tension, temperature, target_volume)
        # Output: 2 values (predicted_fill_volume, predicted_fill_time)
        
        layers = []
        
        # Input layer
        layers.append(nn.Linear(8, neurons_per_layer))
        layers.append(nn.Tanh())
        
        # Hidden layers
        for _ in range(hidden_layers - 1):
            layers.append(nn.Linear(neurons_per_layer, neurons_per_layer))
            layers.append(nn.Tanh())
        
        # Output layer
        layers.append(nn.Linear(neurons_per_layer, 2))
        
        self.network = nn.Sequential(*layers)
        
        # Physics loss weights
        self.lambda_ns = 0.5  # Navier-Stokes weight
        self.lambda_cont = 0.5  # Continuity weight
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the network.
        
        Args:
            x: Input tensor of shape (batch_size, 8)
            
        Returns:
            Output tensor of shape (batch_size, 2)
        """
        return self.network(x)
    
    def compute_physics_loss(self, inputs: torch.Tensor, outputs: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Compute physics-based loss using Navier-Stokes and continuity equations.
        
        This is a simplified physics loss for the MVP. In a full implementation,
        we would use automatic differentiation to compute spatial/temporal derivatives.
        
        Args:
            inputs: Input tensor (batch_size, 8)
            outputs: Output tensor (batch_size, 2)
            
        Returns:
            Tuple of (ns_residual, continuity_residual)
        """
        # Extract parameters
        valve_timing = inputs[:, 0]
        pressure = inputs[:, 1]
        nozzle_diameter = inputs[:, 2]
        viscosity = inputs[:, 3]
        density = inputs[:, 4]
        surface_tension = inputs[:, 5]
        temperature = inputs[:, 6]
        target_volume = inputs[:, 7]
        
        predicted_volume = outputs[:, 0]
        predicted_time = outputs[:, 1]
        
        # Simplified Navier-Stokes residual
        # Flow rate should be consistent with pressure, viscosity, and nozzle diameter
        # Q = (π * d^4 * ΔP) / (128 * μ * L) (Hagen-Poiseuille for laminar flow)
        # Simplified: flow_rate ∝ (pressure * nozzle_diameter^4) / viscosity
        expected_flow_rate = (pressure * torch.pow(nozzle_diameter, 4)) / (viscosity * 100.0)
        actual_flow_rate = predicted_volume / (predicted_time + 1e-6)
        ns_residual = torch.mean(torch.pow(expected_flow_rate - actual_flow_rate, 2))
        
        # Simplified continuity residual
        # Volume should match: V = Q * t
        continuity_check = predicted_volume - (actual_flow_rate * predicted_time)
        continuity_residual = torch.mean(torch.pow(continuity_check, 2))
        
        return ns_residual, continuity_residual
    
    def compute_total_loss(self, inputs: torch.Tensor, outputs: torch.Tensor, 
                          targets: torch.Tensor) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Compute total loss combining data fitting and physics constraints.
        
        Args:
            inputs: Input tensor (batch_size, 8)
            outputs: Model predictions (batch_size, 2)
            targets: Ground truth (batch_size, 2)
            
        Returns:
            Tuple of (total_loss, loss_components_dict)
        """
        # Data fitting loss (MSE)
        mse_loss = nn.MSELoss()(outputs, targets)
        
        # Physics losses
        ns_residual, continuity_residual = self.compute_physics_loss(inputs, outputs)
        
        # Total loss
        total_loss = mse_loss + self.lambda_ns * ns_residual + self.lambda_cont * continuity_residual
        
        loss_components = {
            'mse': mse_loss.item(),
            'ns_residual': ns_residual.item(),
            'continuity_residual': continuity_residual.item(),
            'total': total_loss.item()
        }
        
        return total_loss, loss_components

    
    def train_model(self, train_data: np.ndarray, train_targets: np.ndarray,
                   val_data: np.ndarray, val_targets: np.ndarray,
                   epochs: int = 1000, learning_rate: float = 0.001,
                   early_stopping_patience: int = 50) -> Dict[str, List[float]]:
        """
        Train the PINN model with physics constraints.
        
        Args:
            train_data: Training input data (n_samples, 8)
            train_targets: Training targets (n_samples, 2)
            val_data: Validation input data (n_val, 8)
            val_targets: Validation targets (n_val, 2)
            epochs: Number of training epochs
            learning_rate: Learning rate for optimizer
            early_stopping_patience: Epochs to wait before early stopping
            
        Returns:
            Dictionary containing loss history
        """
        # Convert to tensors
        train_inputs = torch.FloatTensor(train_data)
        train_targets_tensor = torch.FloatTensor(train_targets)
        val_inputs = torch.FloatTensor(val_data)
        val_targets_tensor = torch.FloatTensor(val_targets)
        
        # Optimizer
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        
        # Training history
        history = {
            'train_loss': [],
            'val_loss': [],
            'train_mse': [],
            'val_mse': [],
            'ns_residual': [],
            'continuity_residual': []
        }
        
        best_val_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(epochs):
            # Training
            self.train()
            optimizer.zero_grad()
            
            train_outputs = self.forward(train_inputs)
            train_loss, train_components = self.compute_total_loss(
                train_inputs, train_outputs, train_targets_tensor
            )
            
            train_loss.backward()
            optimizer.step()
            
            # Validation
            self.eval()
            with torch.no_grad():
                val_outputs = self.forward(val_inputs)
                val_loss, val_components = self.compute_total_loss(
                    val_inputs, val_outputs, val_targets_tensor
                )
            
            # Record history
            history['train_loss'].append(train_components['total'])
            history['val_loss'].append(val_components['total'])
            history['train_mse'].append(train_components['mse'])
            history['val_mse'].append(val_components['mse'])
            history['ns_residual'].append(train_components['ns_residual'])
            history['continuity_residual'].append(train_components['continuity_residual'])
            
            # Early stopping
            if val_components['total'] < best_val_loss:
                best_val_loss = val_components['total']
                patience_counter = 0
            else:
                patience_counter += 1
            
            if patience_counter >= early_stopping_patience:
                print(f"Early stopping at epoch {epoch}")
                break
            
            # Print progress every 100 epochs
            if (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch+1}/{epochs} - "
                      f"Train Loss: {train_components['total']:.4f}, "
                      f"Val Loss: {val_components['total']:.4f}")
        
        return history
    
    def calculate_validation_accuracy(self, val_data: np.ndarray, 
                                     val_targets: np.ndarray,
                                     tolerance: float = 0.05) -> float:
        """
        Calculate validation accuracy as percentage of predictions within tolerance.
        
        Args:
            val_data: Validation input data (n_val, 8)
            val_targets: Validation targets (n_val, 2)
            tolerance: Acceptable error tolerance (default 5%)
            
        Returns:
            Validation accuracy as percentage
        """
        self.eval()
        with torch.no_grad():
            val_inputs = torch.FloatTensor(val_data)
            val_targets_tensor = torch.FloatTensor(val_targets)
            
            predictions = self.forward(val_inputs)
            
            # Calculate relative errors
            errors = torch.abs((predictions - val_targets_tensor) / (val_targets_tensor + 1e-6))
            
            # Count predictions within tolerance
            within_tolerance = (errors <= tolerance).all(dim=1).sum().item()
            total = val_data.shape[0]
            
            accuracy = (within_tolerance / total) * 100.0
            
        return accuracy

    
    def predict(self, valve_timing: float, pressure: float, nozzle_diameter: float,
               viscosity: float, density: float, surface_tension: float,
               temperature: float, target_volume: float) -> Tuple[float, float, float, bool]:
        """
        Predict fill outcome given parameters and product properties.
        
        Args:
            valve_timing: Valve timing in seconds
            pressure: Pressure in PSI
            nozzle_diameter: Nozzle diameter in mm
            viscosity: Viscosity in Pa·s
            density: Density in kg/m³
            surface_tension: Surface tension in N/m
            temperature: Temperature in °C
            target_volume: Target volume in mL
            
        Returns:
            Tuple of (predicted_volume, predicted_time, confidence, physics_valid)
        """
        self.eval()
        with torch.no_grad():
            # Prepare input
            input_data = torch.FloatTensor([[
                valve_timing, pressure, nozzle_diameter,
                viscosity, density, surface_tension,
                temperature, target_volume
            ]])
            
            # Get prediction
            output = self.forward(input_data)
            predicted_volume = output[0, 0].item()
            predicted_time = output[0, 1].item()
            
            # Validate physics
            physics_valid, ns_res, cont_res = self.validate_physics(input_data, output)
            
            # Calculate confidence based on physics residuals
            # Lower residuals = higher confidence
            max_residual = max(ns_res, cont_res)
            confidence = max(0.0, min(1.0, 1.0 - max_residual / 0.1))
            
        return predicted_volume, predicted_time, confidence, physics_valid
    
    def validate_physics(self, inputs: torch.Tensor, outputs: torch.Tensor,
                        tolerance: float = 0.05) -> Tuple[bool, float, float]:
        """
        Verify prediction satisfies Navier-Stokes and continuity equations.
        
        Args:
            inputs: Input tensor (batch_size, 8)
            outputs: Output tensor (batch_size, 2)
            tolerance: Physics residual tolerance (default 5%)
            
        Returns:
            Tuple of (is_valid, ns_residual, continuity_residual)
        """
        ns_residual, continuity_residual = self.compute_physics_loss(inputs, outputs)
        
        ns_res = ns_residual.item()
        cont_res = continuity_residual.item()
        
        # Check if residuals are within tolerance
        is_valid = (ns_res <= tolerance) and (cont_res <= tolerance)
        
        return is_valid, ns_res, cont_res
    
    def batch_predict(self, input_data: np.ndarray) -> np.ndarray:
        """
        Batch prediction for optimization.
        
        Args:
            input_data: Input array of shape (n_samples, 8)
            
        Returns:
            Predictions array of shape (n_samples, 2)
        """
        self.eval()
        with torch.no_grad():
            inputs = torch.FloatTensor(input_data)
            outputs = self.forward(inputs)
            return outputs.numpy()

    
    def save_model(self, version_name: str, model_dir: str = "./models") -> str:
        """
        Save model weights and architecture.
        
        Args:
            version_name: Version name for the model
            model_dir: Directory to save model
            
        Returns:
            Path to saved model file
        """
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        
        model_path = Path(model_dir) / f"{version_name}.pth"
        
        # Save model state and architecture info
        torch.save({
            'model_state_dict': self.state_dict(),
            'hidden_layers': self.hidden_layers,
            'neurons_per_layer': self.neurons_per_layer,
            'lambda_ns': self.lambda_ns,
            'lambda_cont': self.lambda_cont
        }, model_path)
        
        print(f"Model saved to {model_path}")
        return str(model_path)
    
    def load_model(self, model_path: str) -> bool:
        """
        Load model from disk.
        
        Args:
            model_path: Path to model file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            checkpoint = torch.load(model_path)
            
            # Verify architecture matches
            if (checkpoint['hidden_layers'] != self.hidden_layers or
                checkpoint['neurons_per_layer'] != self.neurons_per_layer):
                print(f"Warning: Model architecture mismatch")
                return False
            
            # Load state
            self.load_state_dict(checkpoint['model_state_dict'])
            self.lambda_ns = checkpoint['lambda_ns']
            self.lambda_cont = checkpoint['lambda_cont']
            
            self.eval()
            print(f"Model loaded from {model_path}")
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    @staticmethod
    def create_from_checkpoint(model_path: str) -> 'PINNModel':
        """
        Create a new model instance from a checkpoint file.
        
        Args:
            model_path: Path to model checkpoint
            
        Returns:
            New PINNModel instance with loaded weights
        """
        checkpoint = torch.load(model_path)
        
        model = PINNModel(
            hidden_layers=checkpoint['hidden_layers'],
            neurons_per_layer=checkpoint['neurons_per_layer']
        )
        
        model.load_state_dict(checkpoint['model_state_dict'])
        model.lambda_ns = checkpoint['lambda_ns']
        model.lambda_cont = checkpoint['lambda_cont']
        model.eval()
        
        return model
