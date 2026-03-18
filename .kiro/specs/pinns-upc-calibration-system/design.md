# Design Document: PINNs-UPC Calibration System

## Overview

The PINNs-UPC Calibration System is a hackathon MVP that combines Physics-Informed Neural Networks (PINNs) with a UPC product database to optimize liquid filling machine calibration for Technopack's semi-automatic filling equipment. The system addresses the challenge of achieving consistent fill accuracy (<1% error) across diverse liquid products with varying physical properties (viscosity, density, surface tension).

### Core Innovation

Traditional calibration relies on manual parameter tuning or purely data-driven models that require extensive training data. This system leverages PINNs to embed fluid dynamics equations (Navier-Stokes, continuity) directly into the neural network, enabling accurate predictions with limited training data while maintaining physical plausibility. Integration with a UPC database allows instant loading of product-specific properties and calibration profiles.

### Key Capabilities

- Real-time fill prediction (<200ms) before operation execution
- Automatic calibration profile generation for new products
- Physics-constrained predictions that respect fluid dynamics laws
- Continuous learning from actual fill operations
- Anomaly detection and quality assurance validation
- Multi-product handling with rapid context switching

### MVP Scope

This hackathon MVP focuses on:
- Single-machine deployment (not distributed)
- Core PINN model with Navier-Stokes and continuity constraints
- SQLite-based UPC database (scalable to PostgreSQL later)
- Web-based operator interface (Streamlit for rapid development)
- Essential calibration and prediction features
- Basic reporting and data export

Out of scope for MVP:
- Multi-machine synchronization
- Advanced anomaly classification (ML-based)
- Mobile app interface
- Cloud deployment and scaling
- Integration with ERP systems

## Architecture

### System Architecture

The system follows a modular architecture with clear separation between the PINN model, database layer, calibration engine, and user interface:

```
┌─────────────────────────────────────────────────────────────┐
│                     Operator Interface                       │
│              (Streamlit Web UI - Port 8501)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   UPC    │  │   Fill   │  │ Calibr.  │  │ Reports  │   │
│  │  Scanner │  │ Monitor  │  │ Settings │  │Dashboard │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
┌────────────────────────┴────────────────────────────────────┐
│                  Application Layer (Flask)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Calibration Controller                     │  │
│  │  - Product switching  - Validation orchestration     │  │
│  │  - Alert management   - Report generation            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────┬──────────────────┬──────────────────┬────────────────┘
      │                  │                  │
┌─────┴─────┐   ┌────────┴────────┐   ┌────┴──────────┐
│   PINN    │   │   Calibration   │   │   Database    │
│  Engine   │   │   Optimizer     │   │    Layer      │
│           │   │                 │   │               │
│ ┌───────┐ │   │ ┌─────────────┐ │   │ ┌───────────┐ │
│ │ Model │ │   │ │  Parameter  │ │   │ │    UPC    │ │
│ │Trainer│ │   │ │   Search    │ │   │ │  Products │ │
│ └───────┘ │   │ └─────────────┘ │   │ └───────────┘ │
│ ┌───────┐ │   │ ┌─────────────┐ │   │ ┌───────────┐ │
│ │Predict│ │   │ │  Profile    │ │   │ │Calibration│ │
│ │Engine │ │   │ │  Generator  │ │   │ │ Profiles  │ │
│ └───────┘ │   │ └─────────────┘ │   │ └───────────┘ │
│ ┌───────┐ │   │                 │   │ ┌───────────┐ │
│ │Physics│ │   │                 │   │ │ Training  │ │
│ │Checker│ │   │                 │   │ │   Data    │ │
│ └───────┘ │   │                 │   │ └───────────┘ │
└───────────┘   └─────────────────┘   └───────────────┘
```

### Component Responsibilities

**Operator Interface (Streamlit)**
- UPC code input and product selection
- Real-time fill monitoring with visual feedback
- Calibration settings management
- Report viewing and data export

**Application Layer (Flask)**
- Request routing and session management
- Business logic orchestration
- Alert generation and notification
- Report generation coordination

**PINN Engine**
- Neural network training with physics constraints
- Forward prediction (fill volume, time)
- Physics constraint validation
- Model versioning and persistence

**Calibration Optimizer**
- Parameter space search (grid/Bayesian)
- Profile generation for new products
- Profile refinement based on new training data
- Constraint satisfaction verification

**Database Layer**
- UPC product catalog with physical properties
- Calibration profile storage and retrieval
- Training data persistence
- Model version history

### Data Flow

**Product Selection Flow:**
```
UPC Scan → Database Query → Product Properties Retrieved → 
Calibration Profile Loaded → UI Updated → Ready for Fill
```

**Fill Prediction Flow:**
```
Fill Parameters + Product Properties → PINN Model → 
Predicted Volume/Time → Physics Validation → 
Display to Operator → Approval/Adjustment
```

**Fill Execution Flow:**
```
Execute Fill → Monitor Actual Volume → Compare to Prediction → 
Log Training Data → Check Anomaly Threshold → 
Update UI / Generate Alert
```

**Model Training Flow:**
```
Accumulate Training Data → Trigger Threshold Reached → 
Retrain PINN → Validate on Test Set → 
Compare Accuracy → Update Active Model (if improved)
```

## Components and Interfaces

### PINN Model Component

**Purpose:** Core neural network that predicts fill outcomes while respecting fluid dynamics laws.

**Architecture:**
- Input Layer: 8 features (valve_timing, pressure, nozzle_diameter, viscosity, density, surface_tension, temperature, target_volume)
- Hidden Layers: 6 layers × 32 neurons each with Tanh activation
- Output Layer: 2 outputs (predicted_fill_volume, predicted_fill_time)
- Physics Loss: Navier-Stokes residual + Continuity residual

**Interface:**
```python
class PINNModel:
    def predict(self, fill_params: FillParameters, 
                product_props: ProductProperties) -> FillPrediction:
        """
        Predict fill outcome given parameters and product properties.
        Returns: FillPrediction(volume, time, confidence)
        Latency: <10ms
        """
        
    def train(self, training_data: List[FillRecord], 
              epochs: int = 1000) -> TrainingResult:
        """
        Train model on historical data with physics constraints.
        Returns: TrainingResult(loss_history, validation_accuracy)
        """
        
    def validate_physics(self, prediction: FillPrediction) -> PhysicsCheck:
        """
        Verify prediction satisfies Navier-Stokes and continuity.
        Returns: PhysicsCheck(ns_residual, continuity_residual, valid)
        """
        
    def save_model(self, version: str, path: str) -> None:
        """Persist model weights and architecture."""
        
    def load_model(self, version: str, path: str) -> None:
        """Load model from disk."""
```

**Physics Constraints Implementation:**

The PINN loss function combines data fitting with physics residuals:

```
Total_Loss = MSE(y_pred, y_actual) + 
             λ_ns × NS_Residual + 
             λ_cont × Continuity_Residual

where:
  NS_Residual = ||∂u/∂t + u·∇u + ∇p/ρ - ν∇²u||²
  Continuity_Residual = ||∇·u||²
  λ_ns, λ_cont = physics loss weights (tunable, typically 0.1-1.0)
```

Automatic differentiation (PyTorch autograd) computes spatial/temporal derivatives of network outputs to evaluate residuals.

### UPC Database Component

**Purpose:** Store and retrieve product properties and calibration profiles.

**Schema:**

```sql
-- Products table
CREATE TABLE products (
    upc_code VARCHAR(13) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    viscosity FLOAT NOT NULL,  -- Pa·s
    density FLOAT NOT NULL,     -- kg/m³
    surface_tension FLOAT NOT NULL,  -- N/m
    temp_min FLOAT,  -- °C
    temp_max FLOAT,  -- °C
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Calibration profiles table
CREATE TABLE calibration_profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    upc_code VARCHAR(13) REFERENCES products(upc_code),
    valve_timing FLOAT NOT NULL,  -- seconds
    pressure FLOAT NOT NULL,       -- PSI
    nozzle_diameter FLOAT NOT NULL,  -- mm
    target_volume FLOAT NOT NULL,  -- mL
    expected_accuracy FLOAT,  -- percentage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Training data table
CREATE TABLE training_data (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    upc_code VARCHAR(13) REFERENCES products(upc_code),
    valve_timing FLOAT NOT NULL,
    pressure FLOAT NOT NULL,
    nozzle_diameter FLOAT NOT NULL,
    actual_volume FLOAT NOT NULL,  -- mL
    actual_time FLOAT NOT NULL,    -- seconds
    temperature FLOAT,  -- °C
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Model versions table
CREATE TABLE model_versions (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_name VARCHAR(50) NOT NULL,
    training_samples INTEGER NOT NULL,
    validation_accuracy FLOAT NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    model_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Anomaly log table
CREATE TABLE anomaly_log (
    anomaly_id INTEGER PRIMARY KEY AUTOINCREMENT,
    upc_code VARCHAR(13) REFERENCES products(upc_code),
    predicted_volume FLOAT NOT NULL,
    actual_volume FLOAT NOT NULL,
    error_percentage FLOAT NOT NULL,
    classification VARCHAR(50),  -- equipment/product/parameter
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Interface:**
```python
class DatabaseLayer:
    def get_product(self, upc_code: str) -> Optional[Product]:
        """Retrieve product by UPC code. Returns None if not found."""
        
    def add_product(self, product: Product) -> bool:
        """Add new product to database."""
        
    def get_calibration_profile(self, upc_code: str) -> Optional[CalibrationProfile]:
        """Get active calibration profile for product."""
        
    def save_calibration_profile(self, profile: CalibrationProfile) -> int:
        """Save calibration profile, returns profile_id."""
        
    def log_training_data(self, record: FillRecord) -> None:
        """Persist fill operation data for model training."""
        
    def get_training_data(self, upc_code: Optional[str] = None, 
                          limit: int = 1000) -> List[FillRecord]:
        """Retrieve training data, optionally filtered by product."""
        
    def log_anomaly(self, anomaly: AnomalyRecord) -> None:
        """Record anomaly for analysis."""
        
    def get_model_version(self, version_name: str) -> Optional[ModelVersion]:
        """Retrieve model version metadata."""
```

### Calibration Optimizer Component

**Purpose:** Generate and refine calibration profiles by searching parameter space.

**Optimization Strategy:**
- Initial profile: Grid search over coarse parameter ranges
- Refinement: Gradient-based optimization using PINN gradients
- Constraint: Physics validation must pass (NS + continuity residuals < threshold)
- Objective: Minimize |predicted_volume - target_volume|

**Interface:**
```python
class CalibrationOptimizer:
    def generate_profile(self, product: Product, 
                        target_volume: float) -> CalibrationProfile:
        """
        Generate optimal calibration profile for new product.
        Evaluates 100+ parameter combinations.
        Returns: CalibrationProfile with expected accuracy.
        """
        
    def refine_profile(self, current_profile: CalibrationProfile,
                      recent_data: List[FillRecord]) -> CalibrationProfile:
        """
        Refine existing profile based on actual fill data.
        Returns: Updated CalibrationProfile.
        """
        
    def recommend_adjustment(self, predicted: FillPrediction,
                           target: float) -> FillParameters:
        """
        Suggest parameter adjustments when prediction exceeds error threshold.
        Returns: Adjusted FillParameters.
        """
```

**Parameter Search Space:**
```python
PARAMETER_RANGES = {
    'valve_timing': (0.1, 5.0),      # seconds
    'pressure': (10.0, 100.0),       # PSI
    'nozzle_diameter': (2.0, 10.0),  # mm
}

OPTIMIZATION_CONFIG = {
    'grid_resolution': 10,  # points per dimension for initial search
    'max_iterations': 100,
    'convergence_tolerance': 0.001,  # 0.1% volume error
    'physics_tolerance': 0.05,  # 5% residual threshold
}
```

### Application Controller Component

**Purpose:** Orchestrate business logic and coordinate between components.

**Interface:**
```python
class CalibrationController:
    def handle_upc_scan(self, upc_code: str) -> ProductContext:
        """
        Process UPC scan: retrieve product, load profile, update UI context.
        Returns: ProductContext(product, profile, status)
        Latency: <500ms (per requirement)
        """
        
    def predict_fill(self, fill_params: FillParameters) -> PredictionResult:
        """
        Generate fill prediction and check against thresholds.
        Returns: PredictionResult(prediction, recommendation, alert)
        Latency: <200ms (per requirement)
        """
        
    def execute_fill(self, fill_params: FillParameters) -> FillExecution:
        """
        Monitor fill execution, log data, detect anomalies.
        Returns: FillExecution(actual_volume, actual_time, anomaly_detected)
        """
        
    def trigger_retraining(self, upc_code: Optional[str] = None) -> RetrainingResult:
        """
        Initiate model retraining when threshold reached.
        Returns: RetrainingResult(new_version, accuracy_improvement)
        """
        
    def switch_product(self, new_upc: str, current_upc: str) -> SwitchResult:
        """
        Handle product changeover with cleaning prompt if needed.
        Returns: SwitchResult(new_context, cleaning_required)
        Latency: <1s (per requirement)
        """
        
    def generate_report(self, report_type: str, filters: Dict) -> Report:
        """
        Generate performance reports with specified filters.
        Returns: Report(data, statistics, visualizations)
        """
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Product:
    upc_code: str
    product_name: str
    viscosity: float  # Pa·s
    density: float    # kg/m³
    surface_tension: float  # N/m
    temp_min: Optional[float] = None  # °C
    temp_max: Optional[float] = None  # °C

@dataclass
class FillParameters:
    valve_timing: float  # seconds
    pressure: float      # PSI
    nozzle_diameter: float  # mm
    target_volume: float    # mL

@dataclass
class ProductProperties:
    viscosity: float
    density: float
    surface_tension: float
    temperature: float

@dataclass
class FillPrediction:
    predicted_volume: float  # mL
    predicted_time: float    # seconds
    confidence: float        # 0-1
    physics_valid: bool

@dataclass
class CalibrationProfile:
    profile_id: Optional[int]
    upc_code: str
    fill_parameters: FillParameters
    expected_accuracy: float  # percentage
    created_at: datetime
    is_active: bool = True

@dataclass
class FillRecord:
    upc_code: str
    fill_parameters: FillParameters
    product_properties: ProductProperties
    actual_volume: float
    actual_time: float
    timestamp: datetime

@dataclass
class AnomalyRecord:
    upc_code: str
    predicted_volume: float
    actual_volume: float
    error_percentage: float
    classification: str  # equipment/product/parameter
    timestamp: datetime

@dataclass
class ModelVersion:
    version_id: int
    version_name: str
    training_samples: int
    validation_accuracy: float
    is_active: bool
    model_path: str
    created_at: datetime
```

### Data Validation Rules

**Product Properties:**
- Viscosity: 0.001 ≤ viscosity ≤ 10.0 Pa·s (water to honey range)
- Density: 500 ≤ density ≤ 2000 kg/m³ (light oils to concentrated solutions)
- Surface tension: 0.02 ≤ surface_tension ≤ 0.08 N/m (typical liquids)
- Temperature: -20 ≤ temperature ≤ 100 °C (operational range)

**Fill Parameters:**
- Valve timing: 0.1 ≤ valve_timing ≤ 5.0 seconds
- Pressure: 10 ≤ pressure ≤ 100 PSI
- Nozzle diameter: 2.0 ≤ nozzle_diameter ≤ 10.0 mm
- Target volume: 10 ≤ target_volume ≤ 5000 mL

**Accuracy Thresholds:**
- Acceptable fill accuracy: ≤ 1% error (requirement 3.2)
- Prediction warning threshold: > 2% error (requirement 4.2)
- Anomaly detection threshold: > 3% deviation (requirement 4.4)



## Technology Stack

### Core Technologies

**PINN Framework:**
- **PyTorch 2.0+**: Neural network framework with autograd for physics derivatives
- **DeepXDE 1.9+**: PINN library with built-in fluid dynamics PDEs
- Rationale: DeepXDE provides ready-made Navier-Stokes implementations, reducing development time for MVP

**Database:**
- **SQLite 3.x**: Embedded relational database
- **SQLAlchemy 2.0**: ORM for database abstraction
- Rationale: SQLite requires no separate server, perfect for single-machine MVP; easy migration to PostgreSQL later

**Optimization:**
- **SciPy 1.11+**: Scientific computing library with optimization algorithms
- **NumPy 1.24+**: Numerical computing foundation
- Rationale: Mature, well-tested optimization routines (L-BFGS, grid search)

**Web Framework:**
- **Streamlit 1.28+**: Rapid web UI development for Python
- Alternative: Flask 3.0+ with simple HTML/JS if more control needed
- Rationale: Streamlit enables functional UI in hours, ideal for hackathon timeline

**Data Processing:**
- **Pandas 2.0+**: Data manipulation and analysis
- **Matplotlib/Plotly**: Visualization for reports and dashboards
- Rationale: Standard Python data science stack, excellent for MVP reporting

### Development Environment

**Language:** Python 3.9+
**Package Management:** pip + requirements.txt (or Poetry for dependency locking)
**Version Control:** Git
**Testing:** pytest for unit tests, hypothesis for property-based tests

### Deployment Architecture (MVP)

**Single Machine Setup:**
```
┌─────────────────────────────────────────┐
│   Ubuntu 20.04 / Windows 10+ / macOS    │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Streamlit App (Port 8501)         │ │
│  │  - Serves UI                       │ │
│  │  - Handles requests                │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  PINN Engine (In-Process)          │ │
│  │  - PyTorch model                   │ │
│  │  - Inference <10ms                 │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  SQLite Database                   │ │
│  │  - calibration.db                  │ │
│  │  - File-based storage              │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Model Storage                     │ │
│  │  - models/pinn_v*.pth              │ │
│  │  - File system                     │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Hardware Requirements:**
- CPU: 4+ cores (Intel i5/AMD Ryzen 5 or better)
- RAM: 8GB minimum, 16GB recommended
- Storage: 10GB for application + data
- GPU: Optional (CUDA-capable for faster training, not required for inference)

### External Dependencies

**UPC Scanner Integration:**
- USB barcode scanner (HID keyboard emulation)
- No special drivers needed (appears as keyboard input)

**Machine Interface (Future):**
- Serial/USB connection to filling machine controller
- For MVP: Manual parameter entry, simulated fills

### Configuration Management

**Configuration File (config.yaml):**
```yaml
database:
  path: "./data/calibration.db"
  
model:
  architecture:
    hidden_layers: 6
    neurons_per_layer: 32
    activation: "tanh"
  training:
    epochs: 1000
    learning_rate: 0.001
    physics_weight_ns: 0.5
    physics_weight_continuity: 0.5
  paths:
    model_dir: "./models"
    active_model: "pinn_v1.pth"
    
calibration:
  parameter_ranges:
    valve_timing: [0.1, 5.0]
    pressure: [10.0, 100.0]
    nozzle_diameter: [2.0, 10.0]
  optimization:
    grid_resolution: 10
    max_iterations: 100
    convergence_tolerance: 0.001
    
thresholds:
  acceptable_accuracy: 1.0  # percent
  prediction_warning: 2.0   # percent
  anomaly_detection: 3.0    # percent
  retraining_trigger: 50    # new samples
  
ui:
  port: 8501
  refresh_rate: 1.0  # seconds
```

## Error Handling

### Error Categories and Strategies

**1. Data Input Errors**

**UPC Not Found (Requirement 1.2):**
- Error: UPC code not in database
- Handling: Prompt operator to enter product properties manually
- UI: Modal dialog with property input fields
- Logging: Log unknown UPC attempts for database expansion

**Invalid Product Properties:**
- Error: Properties outside validation ranges
- Handling: Reject input, display validation error with acceptable ranges
- Recovery: Allow operator to correct values

**Scanner Hardware Failure:**
- Error: No input from scanner device
- Handling: Fall back to manual UPC entry via keyboard
- UI: Display warning banner, enable text input field

**2. Model Prediction Errors**

**Physics Constraint Violation:**
- Error: Prediction violates Navier-Stokes or continuity (residual > 5%)
- Handling: Flag prediction as low confidence, recommend conservative parameters
- Logging: Log violation for model debugging
- UI: Display warning icon, show physics residual values

**Prediction Timeout:**
- Error: Inference exceeds 200ms latency requirement
- Handling: Return cached prediction from last similar parameters
- Logging: Log timeout event for performance analysis
- Recovery: Trigger model optimization (pruning/quantization)

**Model Load Failure:**
- Error: Cannot load model file (corrupted, missing)
- Handling: Fall back to previous model version
- Logging: Critical error log, alert administrator
- Recovery: Model version rollback mechanism

**3. Calibration Optimization Errors**

**Optimization Convergence Failure:**
- Error: Cannot find parameters meeting accuracy target after 100 iterations
- Handling: Return best-effort parameters with accuracy warning
- UI: Display "Calibration suboptimal" warning, show expected accuracy
- Logging: Log optimization failure with product properties

**Parameter Constraint Violation:**
- Error: Optimizer suggests parameters outside machine limits
- Handling: Clip parameters to valid ranges, re-optimize
- Recovery: Tighten optimization constraints

**4. Database Errors**

**Database Connection Failure:**
- Error: Cannot open SQLite database file
- Handling: Attempt to create new database with schema
- Recovery: If creation fails, operate in read-only mode with in-memory cache
- Logging: Critical error, alert administrator

**Data Integrity Violation:**
- Error: Foreign key constraint violation, duplicate primary key
- Handling: Reject operation, display error to user
- Logging: Log data integrity error with details
- Recovery: Provide data correction interface for administrators

**Write Failure (Disk Full):**
- Error: Cannot write training data or model
- Handling: Alert operator, continue operation without persistence
- UI: Display persistent warning banner
- Recovery: Prompt for disk cleanup or alternate storage path

**5. Training and Model Update Errors**

**Training Divergence:**
- Error: Loss increases during training, model not converging
- Handling: Stop training, keep previous model active
- Logging: Log training metrics, hyperparameters
- Recovery: Adjust learning rate, physics weights, retry

**Validation Accuracy Below Threshold:**
- Error: Retrained model achieves <95% validation accuracy (Requirement 5.4)
- Handling: Reject new model, keep current model active
- UI: Display "Model update failed" notification
- Logging: Log validation results, training data statistics

**Insufficient Training Data:**
- Error: Retraining triggered but <20 samples available
- Handling: Defer retraining until more data collected
- UI: Display "Collecting data for model improvement" status

**6. Anomaly Detection Errors**

**Consecutive Anomalies (Requirement 8.4):**
- Error: Three consecutive fills exceed 2% error threshold
- Handling: Generate maintenance alert, pause automatic fills
- UI: Display red alert banner, recommend machine inspection
- Logging: Log anomaly sequence with parameters and outcomes

**Sensor Malfunction:**
- Error: Actual volume reading is physically impossible (negative, >10x target)
- Handling: Flag as sensor error, exclude from training data
- UI: Display "Sensor check required" warning
- Logging: Log sensor error for maintenance

### Error Response Format

All errors follow a consistent structure for logging and UI display:

```python
@dataclass
class SystemError:
    error_code: str          # e.g., "UPC_NOT_FOUND", "PHYSICS_VIOLATION"
    severity: str            # "INFO", "WARNING", "ERROR", "CRITICAL"
    message: str             # Human-readable description
    context: Dict[str, Any]  # Relevant data (UPC, parameters, etc.)
    timestamp: datetime
    recovery_action: Optional[str]  # Suggested next step
```

### Logging Strategy

**Log Levels:**
- DEBUG: Detailed diagnostic information (prediction values, residuals)
- INFO: Normal operations (UPC scans, fills completed, model updates)
- WARNING: Recoverable issues (prediction warnings, suboptimal calibration)
- ERROR: Operation failures (database errors, model load failures)
- CRITICAL: System-level failures (database corruption, no model available)

**Log Destinations:**
- Console: INFO and above during development
- File: All levels to rotating log files (calibration.log, max 10MB, 5 backups)
- Database: Anomalies and errors to anomaly_log table for analysis

## Testing Strategy

### Testing Approach

The system requires a dual testing strategy combining traditional unit tests with property-based tests. Unit tests verify specific examples and edge cases, while property-based tests validate universal correctness properties across randomized inputs. This combination ensures both concrete behavior verification and comprehensive input coverage.

### Unit Testing

**Scope:**
- Component interfaces and integration points
- Specific edge cases (empty database, boundary values)
- Error handling paths
- UI interactions and state management

**Framework:** pytest with fixtures for database and model mocking

**Key Test Areas:**

1. **Database Layer Tests:**
   - Test product CRUD operations with specific UPC codes
   - Test calibration profile retrieval and storage
   - Test training data logging with timestamp verification
   - Test foreign key constraints and data integrity
   - Edge case: Empty database, duplicate UPC handling

2. **PINN Model Tests:**
   - Test model loading and saving with specific versions
   - Test prediction output format and value ranges
   - Test physics validation with known valid/invalid cases
   - Edge case: Model file corruption, missing model

3. **Calibration Optimizer Tests:**
   - Test profile generation with specific product properties
   - Test parameter adjustment recommendations
   - Test convergence with simple optimization problems
   - Edge case: Optimization failure, infeasible constraints

4. **Controller Tests:**
   - Test UPC scan handling with valid/invalid codes
   - Test product switching with cleaning prompt logic
   - Test anomaly detection with consecutive error sequences
   - Test report generation with specific date ranges

**Test Configuration:**
- Use in-memory SQLite database for test isolation
- Mock PINN model with deterministic predictions for controller tests
- Fixtures for common test data (products, profiles, fill records)

### Property-Based Testing

**Framework:** Hypothesis (Python property-based testing library)

**Configuration:**
- Minimum 100 iterations per property test (due to randomization)
- Each test tagged with reference to design document property
- Generators for valid product properties, fill parameters, and training data

**Test Generators:**

```python
from hypothesis import given, strategies as st

# Product property generators
products = st.builds(
    Product,
    upc_code=st.text(min_size=12, max_size=13, alphabet=st.characters(whitelist_categories=('Nd',))),
    product_name=st.text(min_size=1, max_size=100),
    viscosity=st.floats(min_value=0.001, max_value=10.0),
    density=st.floats(min_value=500.0, max_value=2000.0),
    surface_tension=st.floats(min_value=0.02, max_value=0.08),
    temp_min=st.floats(min_value=-20.0, max_value=50.0),
    temp_max=st.floats(min_value=50.0, max_value=100.0)
)

# Fill parameter generators
fill_parameters = st.builds(
    FillParameters,
    valve_timing=st.floats(min_value=0.1, max_value=5.0),
    pressure=st.floats(min_value=10.0, max_value=100.0),
    nozzle_diameter=st.floats(min_value=2.0, max_value=10.0),
    target_volume=st.floats(min_value=10.0, max_value=5000.0)
)
```

**Property Test Coverage:**

The property-based tests will be written during implementation phase based on the Correctness Properties section below. Each correctness property will map to one or more property-based tests with appropriate generators and assertions.

### Integration Testing

**Scope:**
- End-to-end workflows (UPC scan → prediction → fill → logging)
- Database + Model + Controller integration
- UI + Backend integration

**Approach:**
- Use test database with seed data
- Use trained model (small, fast version for testing)
- Simulate UPC scanner input
- Verify complete data flow and state changes

**Key Integration Tests:**
1. Complete fill cycle: Scan → Predict → Execute → Log
2. Product switching: Switch → Load profile → Verify context
3. Model retraining: Accumulate data → Trigger → Validate → Update
4. Anomaly detection: Execute bad fills → Detect → Alert → Log

### Performance Testing

**Latency Requirements:**
- UPC retrieval: <500ms (Requirement 1.1)
- Fill prediction: <200ms (Requirement 4.1)
- Product switching: <1s (Requirement 7.1)

**Test Approach:**
- Use pytest-benchmark for timing measurements
- Test with realistic database sizes (100-1000 products)
- Test with production-size model
- Measure p50, p95, p99 latencies

**Load Testing:**
- Simulate rapid product switching (10 switches/minute)
- Simulate continuous fill operations (100 fills/hour)
- Monitor memory usage and model inference time

### Validation Testing (Requirement 6)

**Validation Mode Tests:**
- Execute 20+ test fills with known parameters
- Compare actual vs predicted volumes
- Calculate accuracy statistics (mean error, std dev, max deviation)
- Generate validation report
- Verify report format and content

**Acceptance Criteria:**
- Mean error ≤ 1%
- Standard deviation ≤ 0.5%
- Maximum deviation ≤ 2%
- All physics constraints satisfied

### Test Data Management

**Seed Data:**
- 10 sample products with diverse properties (water, oil, syrup, etc.)
- 5 calibration profiles per product
- 100 historical fill records for initial training

**Test Database:**
- Separate test database file (test_calibration.db)
- Reset before each test suite run
- Seed data loaded from fixtures

**Model Artifacts:**
- Small test model (2 layers × 8 neurons) for fast testing
- Pre-trained on synthetic data
- Stored in tests/fixtures/test_model.pth



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Product Round-Trip Persistence

*For any* valid product with all required properties (UPC code, name, viscosity, density, surface tension, temperature range), adding it to the database then retrieving it by UPC code should return a product with identical property values.

**Validates: Requirements 1.3, 1.5**

### Property 2: Product-Profile Association Loading

*For any* product that has an associated calibration profile in the database, retrieving the product properties should also load the corresponding calibration profile.

**Validates: Requirements 1.4**

### Property 3: Physics Constraint Satisfaction

*For any* fill prediction generated by the PINN model, the physics validation check should confirm that both Navier-Stokes and continuity equation residuals are within 5% tolerance.

**Validates: Requirements 2.3**

### Property 4: Model Input-Output Contract

*For any* valid combination of product properties (viscosity, density, surface tension, temperature) and fill parameters (valve timing, pressure, nozzle diameter, target volume), the PINN model should accept the inputs without error and return a prediction containing both fill volume and fill time values.

**Validates: Requirements 2.4, 2.5**

### Property 5: Automatic Profile Generation

*For any* new product added to the system without an existing calibration profile, the system should automatically generate an initial calibration profile using PINN model predictions.

**Validates: Requirements 3.1**

### Property 6: Calibration Optimization Quality

*For any* calibration profile generated by the optimization process, the predicted fill accuracy error should be at most 1% when evaluated with the PINN model.

**Validates: Requirements 3.2**

### Property 7: Profile Storage Round-Trip

*For any* optimized calibration profile, storing it in association with a product UPC code then retrieving it by that UPC should return a profile with identical parameter values.

**Validates: Requirements 3.4**

### Property 8: High-Error Prediction Recommendations

*For any* fill prediction where the predicted fill accuracy exceeds 2% error from the target volume, the system should provide recommended adjusted fill parameters.

**Validates: Requirements 4.2**

### Property 9: Anomaly Detection and Logging

*For any* completed fill operation where the actual fill volume deviates from the prediction by more than 3%, the system should both detect the anomaly and log it with all associated fill parameters, product properties, timestamp, and deviation magnitude.

**Validates: Requirements 4.4, 8.5**

### Property 10: Training Data Persistence

*For any* completed fill operation, the system should record training data containing all fill parameters, product properties, actual fill volume, timestamp, and product UPC association.

**Validates: Requirements 5.1, 5.2**

### Property 11: Model Retraining Validation

*For any* PINN model retraining operation, the validation results against the held-out test set should achieve at least 95% accuracy before the model is considered for deployment.

**Validates: Requirements 5.4**

### Property 12: Conditional Model Update

*For any* model retraining that improves prediction accuracy by more than 5% compared to the current active model, the system should update the active model to the new version.

**Validates: Requirements 5.5**

### Property 13: Model Version Rollback

*For any* model version saved in the version history, the system should be able to retrieve and restore it as the active model, effectively rolling back to that version.

**Validates: Requirements 5.6**

### Property 14: Validation Mode Comparison

*For any* test fill executed in validation mode with known parameters, the system should compare the actual fill volume against the PINN model prediction and record the comparison result.

**Validates: Requirements 6.2**

### Property 15: Validation Statistics Completeness

*For any* validation run, the calculated fill accuracy statistics should include mean error, standard deviation, and maximum deviation across all test fills.

**Validates: Requirements 6.3**

### Property 16: Validation Profile Flagging

*For any* validation run where fill accuracy exceeds acceptable thresholds (>1% mean error or >2% max deviation), the system should flag the associated calibration profile for review.

**Validates: Requirements 6.5**

### Property 17: Product Context Switching

*For any* different UPC code scanned while a product is active, the system should switch to the new product's calibration profile and update the operator interface context.

**Validates: Requirements 7.1**

### Property 18: Active Product Display

*For any* product currently active in the system, the operator interface should display the product name and key product properties (viscosity, density, surface tension).

**Validates: Requirements 7.2, 10.2**

### Property 19: Fill History Tracking

*For any* sequence of fill operations, the system should maintain a retrievable history of the last 10 products filled with their timestamps.

**Validates: Requirements 7.3**

### Property 20: Cleaning Prompt on Significant Property Change

*For any* product switch where the new product's properties (viscosity, density, or surface tension) differ from the previous product by more than 20%, the system should prompt the operator for machine cleaning confirmation.

**Validates: Requirements 7.4**

### Property 21: Product Sequence Round-Trip

*For any* saved product sequence for batch operations, loading the sequence should restore the exact same ordered list of products with their associated parameters.

**Validates: Requirements 7.5**

### Property 22: Anomaly Alert Generation

*For any* fill operation where fill accuracy exceeds the 2% error threshold, the system should generate an alert containing timestamp, deviation magnitude, and anomaly classification (equipment/product/parameter).

**Validates: Requirements 8.1, 8.2, 8.3**

### Property 23: Training Data Export Round-Trip

*For any* set of training data, exporting to CSV format then importing should preserve all fill parameters, product properties, actual volumes, and timestamps.

**Validates: Requirements 9.1**

### Property 24: Daily Performance Report Generation

*For any* day with completed fill operations, the system should generate a performance report showing fill accuracy statistics (mean, std dev, max error) grouped by product.

**Validates: Requirements 9.2**

### Property 25: Calibration Profile Export Round-Trip

*For any* calibration profile, exporting to JSON format then importing should preserve all parameter values, UPC association, and metadata.

**Validates: Requirements 9.3**

### Property 26: Report Filtering Correctness

*For any* report filtered by product UPC, date range, or accuracy threshold, all returned results should match the specified filter criteria and no matching records should be excluded.

**Validates: Requirements 9.5**

### Property 27: Accuracy Status Color Mapping

*For any* fill accuracy value, the UI color indicator should be green for ≤1% error, yellow for 1-2% error, and red for >2% error.

**Validates: Requirements 10.4**

