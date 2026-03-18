# Implementation Plan: PINNs-UPC Calibration System

## Overview

This implementation plan breaks down the PINNs-UPC Calibration System into discrete, testable coding tasks. The system combines Physics-Informed Neural Networks with a UPC product database to optimize liquid filling machine calibration. Implementation uses Python with PyTorch/DeepXDE for the PINN model, SQLite for data persistence, and Streamlit for the operator interface.

The plan follows an incremental approach: database layer → PINN model → calibration optimizer → application controller → UI → integration. Each task builds on previous work, with property-based tests placed close to implementation to catch errors early.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create directory structure (src/, tests/, data/, models/, config/)
  - Create requirements.txt with core dependencies (PyTorch, DeepXDE, SQLAlchemy, Streamlit, pytest, hypothesis)
  - Create config.yaml with system configuration (database path, model parameters, thresholds)
  - Set up pytest configuration and test fixtures directory
  - Create main entry point script (main.py)
  - _Requirements: All (foundational)_

- [ ] 2. Implement database schema and data layer
  - [x] 2.1 Create SQLAlchemy models for database schema
    - Define Product, CalibrationProfile, TrainingData, ModelVersion, AnomalyLog models
    - Implement table relationships and foreign key constraints
    - Add data validation constraints (value ranges for viscosity, density, etc.)
    - _Requirements: 1.3, 5.1, 5.2, 8.5_
  
  - [x] 2.2 Implement DatabaseLayer class with CRUD operations
    - Implement get_product(), add_product() methods
    - Implement get_calibration_profile(), save_calibration_profile() methods
    - Implement log_training_data(), get_training_data() methods
    - Implement log_anomaly(), get_model_version() methods
    - Add database initialization and connection management
    - _Requirements: 1.1, 1.2, 1.3, 1.5, 3.4, 5.1, 5.2, 8.5_
  
  - [ ]* 2.3 Write property test for product round-trip persistence
    - **Property 1: Product Round-Trip Persistence**
    - **Validates: Requirements 1.3, 1.5**
  
  - [ ]* 2.4 Write property test for product-profile association loading
    - **Property 2: Product-Profile Association Loading**
    - **Validates: Requirements 1.4**
  
  - [ ]* 2.5 Write property test for profile storage round-trip
    - **Property 7: Profile Storage Round-Trip**
    - **Validates: Requirements 3.4**
  
  - [ ]* 2.6 Write unit tests for database layer edge cases
    - Test UPC not found handling
    - Test duplicate UPC handling
    - Test foreign key constraint violations
    - Test empty database queries
    - _Requirements: 1.2_

- [ ] 3. Implement core data models and validation
  - [x] 3.1 Create dataclasses for core data structures
    - Implement Product, FillParameters, ProductProperties, FillPrediction dataclasses
    - Implement CalibrationProfile, FillRecord, AnomalyRecord, ModelVersion dataclasses
    - Add type hints and default values
    - _Requirements: 1.3, 2.4, 2.5, 5.1, 8.3_
  
  - [x] 3.2 Implement data validation functions
    - Create validate_product_properties() with range checks
    - Create validate_fill_parameters() with range checks
    - Create validate_accuracy_thresholds() function
    - Add validation error messages with acceptable ranges
    - _Requirements: 1.3, 2.4, 3.2, 4.2, 4.4_
  
  - [ ]* 3.3 Write unit tests for data validation
    - Test boundary values for all properties
    - Test invalid values rejection
    - Test validation error messages
    - _Requirements: 1.3, 2.4_

- [ ] 4. Implement PINN model with physics constraints
  - [x] 4.1 Create PINNModel class with PyTorch/DeepXDE
    - Define neural network architecture (6 layers × 32 neurons, Tanh activation)
    - Implement forward pass with 8 inputs → 2 outputs (volume, time)
    - Implement physics loss function combining MSE + Navier-Stokes + continuity residuals
    - Add automatic differentiation for physics derivatives
    - _Requirements: 2.1, 2.2, 2.4, 2.5_
  
  - [x] 4.2 Implement PINN training functionality
    - Implement train() method with physics-constrained loss
    - Add training loop with epoch tracking and loss history
    - Implement validation split and accuracy calculation
    - Add early stopping based on validation loss
    - _Requirements: 2.6, 5.3, 5.4_
  
  - [x] 4.3 Implement PINN prediction and physics validation
    - Implement predict() method with <10ms latency target
    - Implement validate_physics() method checking NS and continuity residuals
    - Add confidence scoring based on physics residuals
    - Implement batch prediction for optimization
    - _Requirements: 2.3, 2.4, 2.5, 4.1_
  
  - [x] 4.4 Implement model persistence (save/load)
    - Implement save_model() with version naming
    - Implement load_model() with error handling
    - Add model metadata storage (architecture, training config)
    - _Requirements: 5.5, 5.6_
  
  - [ ]* 4.5 Write property test for physics constraint satisfaction
    - **Property 3: Physics Constraint Satisfaction**
    - **Validates: Requirements 2.3**
  
  - [ ]* 4.6 Write property test for model input-output contract
    - **Property 4: Model Input-Output Contract**
    - **Validates: Requirements 2.4, 2.5**
  
  - [ ]* 4.7 Write unit tests for PINN model
    - Test model initialization and architecture
    - Test prediction output format
    - Test model save/load with specific versions
    - Test physics validation with known cases
    - _Requirements: 2.1, 2.2, 2.3_

- [ ] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement calibration optimizer
  - [x] 6.1 Create CalibrationOptimizer class with parameter search
    - Implement grid search over parameter ranges (valve_timing, pressure, nozzle_diameter)
    - Implement objective function minimizing |predicted_volume - target_volume|
    - Add physics constraint checking during optimization
    - Implement parameter clipping to valid ranges
    - _Requirements: 3.1, 3.2, 3.3_
  
  - [x] 6.2 Implement profile generation and refinement
    - Implement generate_profile() for new products
    - Implement refine_profile() using recent fill data
    - Add expected accuracy calculation
    - Implement convergence checking (0.1% tolerance)
    - _Requirements: 3.1, 3.2, 3.5_
  
  - [x] 6.3 Implement parameter adjustment recommendations
    - Implement recommend_adjustment() for high-error predictions
    - Add gradient-based parameter adjustment using PINN gradients
    - Implement adjustment magnitude scaling based on error size
    - _Requirements: 4.2_
  
  - [ ]* 6.4 Write property test for automatic profile generation
    - **Property 5: Automatic Profile Generation**
    - **Validates: Requirements 3.1**
  
  - [ ]* 6.5 Write property test for calibration optimization quality
    - **Property 6: Calibration Optimization Quality**
    - **Validates: Requirements 3.2**
  
  - [ ]* 6.6 Write property test for high-error prediction recommendations
    - **Property 8: High-Error Prediction Recommendations**
    - **Validates: Requirements 4.2**
  
  - [ ]* 6.7 Write unit tests for calibration optimizer
    - Test optimization convergence with simple cases
    - Test parameter constraint handling
    - Test optimization failure recovery
    - _Requirements: 3.1, 3.2, 4.2_

- [ ] 7. Implement application controller and business logic
  - [x] 7.1 Create CalibrationController class
    - Initialize with database, PINN model, and optimizer dependencies
    - Implement component coordination and state management
    - Add error handling and logging infrastructure
    - _Requirements: All (orchestration)_
  
  - [x] 7.2 Implement UPC scan handling and product loading
    - Implement handle_upc_scan() with <500ms latency target
    - Add product retrieval from database
    - Add calibration profile loading
    - Implement manual property entry fallback for unknown UPCs
    - Add ProductContext creation for UI
    - _Requirements: 1.1, 1.2, 1.4_
  
  - [x] 7.3 Implement fill prediction workflow
    - Implement predict_fill() with <200ms latency target
    - Add PINN model prediction invocation
    - Add error threshold checking (2% warning)
    - Add parameter adjustment recommendation when needed
    - Create PredictionResult with alerts
    - _Requirements: 4.1, 4.2, 4.5_
  
  - [x] 7.4 Implement fill execution monitoring and logging
    - Implement execute_fill() with actual volume monitoring
    - Add prediction vs actual comparison (3% anomaly threshold)
    - Add training data logging for every fill
    - Add anomaly detection and logging
    - Implement retraining trigger check (50 samples threshold)
    - _Requirements: 4.3, 4.4, 5.1, 5.2, 8.1_
  
  - [x] 7.5 Implement product switching logic
    - Implement switch_product() with <1s latency target
    - Add property difference calculation (20% threshold)
    - Add cleaning confirmation prompt when needed
    - Add product history tracking (last 10 products)
    - _Requirements: 7.1, 7.2, 7.3, 7.4_
  
  - [ ] 7.6 Implement model retraining workflow
    - Implement trigger_retraining() with data accumulation check
    - Add PINN model retraining invocation
    - Add validation accuracy check (95% threshold)
    - Add accuracy improvement check (5% threshold)
    - Implement model version update and activation
    - Add model version history management
    - _Requirements: 5.3, 5.4, 5.5, 5.6_
  
  - [ ]* 7.7 Write property test for training data persistence
    - **Property 10: Training Data Persistence**
    - **Validates: Requirements 5.1, 5.2**
  
  - [ ]* 7.8 Write property test for anomaly detection and logging
    - **Property 9: Anomaly Detection and Logging**
    - **Validates: Requirements 4.4, 8.5**
  
  - [ ]* 7.9 Write property test for product context switching
    - **Property 17: Product Context Switching**
    - **Validates: Requirements 7.1**
  
  - [ ]* 7.10 Write property test for cleaning prompt on property change
    - **Property 20: Cleaning Prompt on Significant Property Change**
    - **Validates: Requirements 7.4**
  
  - [ ]* 7.11 Write property test for anomaly alert generation
    - **Property 22: Anomaly Alert Generation**
    - **Validates: Requirements 8.1, 8.2, 8.3**
  
  - [ ]* 7.12 Write unit tests for controller workflows
    - Test UPC scan with valid/invalid codes
    - Test fill prediction with various error levels
    - Test product switching scenarios
    - Test retraining trigger and execution
    - _Requirements: 1.1, 1.2, 4.1, 4.2, 7.1, 5.3_

- [ ] 8. Implement validation mode and reporting
  - [ ] 8.1 Create validation mode functionality
    - Implement validation_mode() for test fills
    - Add actual vs predicted comparison tracking
    - Implement accuracy statistics calculation (mean, std dev, max)
    - Add validation report generation
    - Implement profile flagging for excessive errors
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ] 8.2 Implement report generation
    - Implement generate_report() with report type routing
    - Add daily performance report generation
    - Add fill accuracy statistics per product
    - Implement report filtering (UPC, date range, accuracy threshold)
    - Add dashboard data preparation
    - _Requirements: 9.2, 9.4, 9.5_
  
  - [ ] 8.3 Implement data export functionality
    - Implement export_training_data() to CSV format
    - Implement export_calibration_profile() to JSON format
    - Add import functionality for round-trip verification
    - _Requirements: 9.1, 9.3_
  
  - [ ]* 8.4 Write property test for validation mode comparison
    - **Property 14: Validation Mode Comparison**
    - **Validates: Requirements 6.2**
  
  - [ ]* 8.5 Write property test for validation statistics completeness
    - **Property 15: Validation Statistics Completeness**
    - **Validates: Requirements 6.3**
  
  - [ ]* 8.6 Write property test for validation profile flagging
    - **Property 16: Validation Profile Flagging**
    - **Validates: Requirements 6.5**
  
  - [ ]* 8.7 Write property test for training data export round-trip
    - **Property 23: Training Data Export Round-Trip**
    - **Validates: Requirements 9.1**
  
  - [ ]* 8.8 Write property test for calibration profile export round-trip
    - **Property 25: Calibration Profile Export Round-Trip**
    - **Validates: Requirements 9.3**
  
  - [ ]* 8.9 Write property test for report filtering correctness
    - **Property 26: Report Filtering Correctness**
    - **Validates: Requirements 9.5**
  
  - [ ]* 8.10 Write unit tests for validation and reporting
    - Test validation mode with 20+ test fills
    - Test report generation with various filters
    - Test export/import round-trips
    - _Requirements: 6.1, 6.2, 9.1, 9.3_

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Implement Streamlit operator interface
  - [x] 10.1 Create main UI layout and navigation
    - Create app.py with Streamlit page configuration
    - Implement sidebar navigation (Scanner, Monitor, Calibration, Reports)
    - Add session state management for current product and context
    - Implement page routing logic
    - _Requirements: 10.1, 10.5_
  
  - [x] 10.2 Implement UPC scanner page
    - Create UPC input field with visual feedback
    - Add product information display (name, properties)
    - Implement manual property entry form for unknown UPCs
    - Add product addition to database functionality
    - Display current calibration profile parameters
    - _Requirements: 1.1, 1.2, 1.5, 10.1, 10.2_
  
  - [x] 10.3 Implement fill monitor page
    - Create fill parameter input controls (valve_timing, pressure, nozzle_diameter, target_volume)
    - Add prediction display with volume and time
    - Implement color-coded accuracy indicator (green ≤1%, yellow 1-2%, red >2%)
    - Add fill execution button and progress tracking
    - Display actual vs predicted comparison after fill
    - Show anomaly alerts when detected
    - _Requirements: 4.1, 4.2, 4.5, 10.2, 10.3, 10.4_
  
  - [ ] 10.4 Implement calibration settings page
    - Create product list with search/filter
    - Add calibration profile viewer and editor
    - Implement profile regeneration button
    - Add model retraining trigger and status display
    - Show model version history with rollback option
    - _Requirements: 3.5, 5.3, 5.5, 5.6, 10.5_
  
  - [ ] 10.5 Implement reports dashboard page
    - Create date range selector
    - Add product filter dropdown
    - Implement fill accuracy trend chart (Plotly)
    - Display daily performance statistics table
    - Add export buttons for CSV and JSON
    - Show validation report viewer
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
  
  - [ ]* 10.6 Write property test for active product display
    - **Property 18: Active Product Display**
    - **Validates: Requirements 7.2, 10.2**
  
  - [ ]* 10.7 Write property test for accuracy status color mapping
    - **Property 27: Accuracy Status Color Mapping**
    - **Validates: Requirements 10.4**
  
  - [ ]* 10.8 Write integration tests for UI workflows
    - Test complete UPC scan → prediction → fill workflow
    - Test product switching workflow
    - Test report generation and export
    - _Requirements: 1.1, 4.1, 7.1, 9.2_

- [ ] 11. Create seed data and initialize system
  - [x] 11.1 Create database seed data script
    - Create 10 sample products with diverse properties (water, oil, syrup, etc.)
    - Generate 5 calibration profiles per product
    - Create 100 synthetic training records for initial model training
    - Add seed data loading function
    - _Requirements: All (testing and demo)_
  
  - [x] 11.2 Train initial PINN model
    - Load seed training data
    - Train PINN model with physics constraints
    - Validate model accuracy on test set
    - Save model as version 1 (pinn_v1.pth)
    - Mark as active model in database
    - _Requirements: 2.6, 5.4, 5.5_
  
  - [ ]* 11.3 Write unit tests for seed data
    - Test seed data loading
    - Test initial model training
    - Verify database initialization
    - _Requirements: All (foundational)_

- [ ] 12. Integration testing and end-to-end validation
  - [ ]* 12.1 Write integration test for complete fill cycle
    - Test UPC scan → product load → prediction → fill execution → data logging
    - Verify all components interact correctly
    - Check latency requirements met
    - _Requirements: 1.1, 4.1, 5.1, 7.1_
  
  - [ ]* 12.2 Write integration test for model retraining workflow
    - Accumulate 50+ training samples
    - Trigger retraining
    - Validate new model
    - Verify model update if improved
    - _Requirements: 5.3, 5.4, 5.5_
  
  - [ ]* 12.3 Write integration test for anomaly detection workflow
    - Execute fills with intentional errors
    - Verify anomaly detection
    - Check alert generation
    - Verify consecutive anomaly handling (3+ fills)
    - _Requirements: 4.4, 8.1, 8.4_
  
  - [ ]* 12.4 Write property test for model retraining validation
    - **Property 11: Model Retraining Validation**
    - **Validates: Requirements 5.4**
  
  - [ ]* 12.5 Write property test for conditional model update
    - **Property 12: Conditional Model Update**
    - **Validates: Requirements 5.5**
  
  - [ ]* 12.6 Write property test for model version rollback
    - **Property 13: Model Version Rollback**
    - **Validates: Requirements 5.6**
  
  - [ ]* 12.7 Write property test for fill history tracking
    - **Property 19: Fill History Tracking**
    - **Validates: Requirements 7.3**
  
  - [ ]* 12.8 Write property test for product sequence round-trip
    - **Property 21: Product Sequence Round-Trip**
    - **Validates: Requirements 7.5**
  
  - [ ]* 12.9 Write property test for daily performance report generation
    - **Property 24: Daily Performance Report Generation**
    - **Validates: Requirements 9.2**

- [ ] 13. Performance testing and optimization
  - [ ]* 13.1 Write performance tests for latency requirements
    - Test UPC retrieval <500ms
    - Test fill prediction <200ms
    - Test product switching <1s
    - Use pytest-benchmark for measurements
    - _Requirements: 1.1, 4.1, 7.1_
  
  - [ ]* 13.2 Optimize PINN model inference if needed
    - Profile prediction latency
    - Apply model quantization if >200ms
    - Implement batch prediction optimization
    - _Requirements: 4.1_
  
  - [ ]* 13.3 Write load tests for continuous operation
    - Simulate 100 fills/hour
    - Simulate 10 product switches/minute
    - Monitor memory usage and performance
    - _Requirements: All (system stability)_

- [ ] 14. Final checkpoint and documentation
  - [x] 14.1 Create README with setup instructions
    - Document installation steps (Python, dependencies)
    - Add configuration guide (config.yaml)
    - Document how to run the application
    - Add troubleshooting section
    - _Requirements: All (deployment)_
  
  - [ ] 14.2 Create operator user guide
    - Document UPC scanning workflow
    - Document fill prediction and execution
    - Document product switching procedure
    - Document report generation and export
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ] 14.3 Final system validation
    - Run complete test suite
    - Execute validation mode with 20+ test fills
    - Verify all latency requirements met
    - Generate validation report
    - Ensure all tests pass, ask the user if questions arise.
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at logical breaks
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- Integration tests verify end-to-end workflows
- The implementation follows Python best practices with type hints and dataclasses
- PyTorch/DeepXDE provide PINN capabilities with automatic differentiation
- SQLite provides zero-configuration database for MVP
- Streamlit enables rapid UI development for hackathon timeline
- All latency requirements (<500ms UPC, <200ms prediction, <1s switching) are explicitly tested
