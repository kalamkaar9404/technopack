"""
Computer Vision Fill Level Detection System
Feature 1: Real-time visual verification of fill levels
"""
import numpy as np
import cv2
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class FillDetectionResult:
    """Result from vision-based fill detection"""
    detected_volume: float  # mL
    confidence: float  # 0-1
    liquid_height: float  # mm
    has_foam: bool
    image_quality: str  # good/poor/blocked

class FillLevelDetector:
    """
    Computer vision system for detecting fill levels in bottles.
    Uses edge detection and contour analysis to measure liquid height.
    """
    
    def __init__(self, bottle_geometry: dict):
        """
        Initialize fill detector.
        
        Args:
            bottle_geometry: Dict with bottle dimensions
                - diameter_mm: Bottle diameter
                - height_mm: Total bottle height
                - ml_per_mm: Volume per mm of height
        """
        self.bottle_geometry = bottle_geometry
        self.calibration_factor = bottle_geometry.get('ml_per_mm', 10.0)
        
        # Vision parameters
        self.min_confidence = 0.7
        self.foam_threshold = 20  # Pixel intensity difference
        
    def detect_fill_level(self, image: np.ndarray, 
                         target_volume: float) -> FillDetectionResult:
        """
        Detect fill level from camera image.
        
        Args:
            image: Camera image (numpy array)
            target_volume: Expected volume in mL
            
        Returns:
            FillDetectionResult with detected volume and confidence
        """
        # Check image quality
        quality = self._check_image_quality(image)
        if quality == "blocked":
            return FillDetectionResult(
                detected_volume=0.0,
                confidence=0.0,
                liquid_height=0.0,
                has_foam=False,
                image_quality="blocked"
            )
        
        # Detect liquid surface
        liquid_height, confidence = self._detect_liquid_surface(image)
        
        # Calculate volume from height
        detected_volume = liquid_height * self.calibration_factor
        
        # Detect foam
        has_foam = self._detect_foam(image, liquid_height)
        
        return FillDetectionResult(
            detected_volume=detected_volume,
            confidence=confidence,
            liquid_height=liquid_height,
            has_foam=has_foam,
            image_quality=quality
        )
    
    def _check_image_quality(self, image: np.ndarray) -> str:
        """Check if image is suitable for analysis"""
        if image is None or image.size == 0:
            return "blocked"
        
        # Check brightness
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        mean_brightness = np.mean(gray)
        
        if mean_brightness < 30:
            return "poor"  # Too dark
        elif mean_brightness > 225:
            return "poor"  # Too bright
        else:
            return "good"
    
    def _detect_liquid_surface(self, image: np.ndarray) -> Tuple[float, float]:
        """
        Detect liquid surface using edge detection.
        
        Returns:
            Tuple of (height_mm, confidence)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find horizontal edges (liquid surface)
        horizontal_edges = self._find_horizontal_edges(edges)
        
        if len(horizontal_edges) == 0:
            return 0.0, 0.0
        
        # Get strongest horizontal edge (likely liquid surface)
        surface_y = horizontal_edges[0]
        
        # Convert pixel position to height in mm
        image_height = image.shape[0]
        bottle_height_mm = self.bottle_geometry['height_mm']
        
        # Calculate height from bottom
        height_mm = (image_height - surface_y) / image_height * bottle_height_mm
        
        # Confidence based on edge strength
        confidence = min(1.0, len(horizontal_edges) / 10.0)
        
        return height_mm, confidence
    
    def _find_horizontal_edges(self, edges: np.ndarray) -> list:
        """Find horizontal edges in edge-detected image"""
        horizontal_edges = []
        
        # Scan each row
        for y in range(edges.shape[0]):
            row = edges[y, :]
            edge_count = np.sum(row > 0)
            
            # If significant horizontal edge detected
            if edge_count > edges.shape[1] * 0.3:  # 30% of width
                horizontal_edges.append(y)
        
        return horizontal_edges
    
    def _detect_foam(self, image: np.ndarray, liquid_height: float) -> bool:
        """
        Detect foam on liquid surface.
        Foam appears as lighter, textured region above liquid.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Get region above liquid surface
        image_height = image.shape[0]
        bottle_height_mm = self.bottle_geometry['height_mm']
        
        surface_y = int(image_height * (1 - liquid_height / bottle_height_mm))
        
        if surface_y < 10 or surface_y >= image_height - 10:
            return False
        
        # Compare intensity above and below surface
        above_surface = gray[max(0, surface_y-10):surface_y, :]
        below_surface = gray[surface_y:min(image_height, surface_y+10), :]
        
        if above_surface.size == 0 or below_surface.size == 0:
            return False
        
        intensity_diff = np.mean(above_surface) - np.mean(below_surface)
        
        # Foam is lighter than liquid
        return intensity_diff > self.foam_threshold
    
    def simulate_camera_image(self, actual_volume: float, 
                             has_foam: bool = False,
                             noise_level: float = 0.02) -> np.ndarray:
        """
        Simulate camera image for testing (when no real camera available).
        
        Args:
            actual_volume: Actual fill volume in mL
            has_foam: Whether foam is present
            noise_level: Amount of noise to add (0-1)
            
        Returns:
            Simulated grayscale image
        """
        # Create blank image (640x480)
        image = np.ones((480, 640), dtype=np.uint8) * 200  # Light background
        
        # Calculate liquid height
        liquid_height = actual_volume / self.calibration_factor
        bottle_height = self.bottle_geometry['height_mm']
        
        # Convert to pixel position
        surface_y = int(480 * (1 - liquid_height / bottle_height))
        
        # Draw liquid (darker region below surface)
        image[surface_y:, :] = 100  # Dark liquid
        
        # Add foam if present
        if has_foam:
            foam_height = int(20 + np.random.rand() * 20)  # 20-40 pixels
            image[max(0, surface_y-foam_height):surface_y, :] = 150  # Lighter foam
        
        # Add noise
        noise = np.random.normal(0, noise_level * 255, image.shape)
        image = np.clip(image + noise, 0, 255).astype(np.uint8)
        
        # Add some texture
        image = cv2.GaussianBlur(image, (3, 3), 0)
        
        return image
    
    def verify_fill_accuracy(self, detected_volume: float, 
                            target_volume: float,
                            tolerance: float = 1.0) -> Tuple[bool, float]:
        """
        Verify if detected fill is within tolerance.
        
        Args:
            detected_volume: Volume detected by vision
            target_volume: Target volume
            tolerance: Acceptable error percentage
            
        Returns:
            Tuple of (is_accurate, error_percentage)
        """
        error_pct = abs(detected_volume - target_volume) / target_volume * 100.0
        is_accurate = error_pct <= tolerance
        
        return is_accurate, error_pct
