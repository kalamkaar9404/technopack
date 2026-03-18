"""
FastAPI Backend for PINNs-UPC Calibration System
Connects Next.js frontend with Python backend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import yaml
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DatabaseLayer
from src.models.pinn_model import PINNModel
from src.optimizer import CalibrationOptimizer
from src.controller import CalibrationController
from src.vision import FillLevelDetector
from src.maintenance import EquipmentHealthMonitor
from src.quality import SPCMonitor
from src.anomaly import AnomalyDatabase

# Initialize FastAPI
app = FastAPI(
    title="PINNs-UPC Calibration API",
    description="Backend API for liquid filling calibration system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global controller instance
controller = None

# Pydantic models
class UPCScanRequest(BaseModel):
    upc_code: str

class PredictFillRequest(BaseModel):
    valve_timing: float
    pressure: float
    nozzle_diameter: float
    target_volume: float
    temperature: float = 25.0

class ExecuteFillRequest(BaseModel):
    valve_timing: float
    pressure: float
    nozzle_diameter: float
    target_volume: float
    actual_volume: float
    actual_time: float
    temperature: float = 25.0
    use_vision: bool = False

class AddProductRequest(BaseModel):
    upc_code: str
    product_name: str
    viscosity: float
    density: float
    surface_tension: float

class ReportAnomalyRequest(BaseModel):
    issue_type: str
    solution: str
    effectiveness: float

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    global controller
    
    # Load config
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize database
    db = DatabaseLayer(config['database']['path'])
    db.initialize_database()
    
    # Initialize PINN model
    model = PINNModel(
        hidden_layers=config['model']['architecture']['hidden_layers'],
        neurons_per_layer=config['model']['architecture']['neurons_per_layer']
    )
    
    # Try to load existing model
    model_path = Path(config['model']['paths']['model_dir']) / config['model']['paths']['active_model']
    if model_path.exists():
        model.load_model(str(model_path))
    
    # Initialize optimizer
    optimizer = CalibrationOptimizer(model, config)
    
    # Initialize advanced features
    vision_detector = FillLevelDetector({
        'diameter_mm': 50,
        'height_mm': 200,
        'ml_per_mm': 10.0
    })
    
    health_monitor = EquipmentHealthMonitor(config)
    spc_monitor = SPCMonitor(target_accuracy=100.0)
    anomaly_db = AnomalyDatabase()
    
    # Seed anomaly database if empty
    if len(anomaly_db.anomalies) == 0:
        anomaly_db.seed_initial_data()
    
    # Initialize controller
    controller = CalibrationController(
        db, model, optimizer, config,
        vision_detector=vision_detector,
        health_monitor=health_monitor,
        spc_monitor=spc_monitor,
        anomaly_db=anomaly_db
    )
    
    print("✓ Backend initialized successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "PINNs-UPC Calibration API",
        "version": "1.0.0"
    }

@app.get("/api/products")
async def get_products():
    """Get all products"""
    products = controller.db.get_all_products()
    return {
        "products": [
            {
                "upc_code": p.upc_code,
                "product_name": p.product_name,
                "viscosity": p.viscosity,
                "density": p.density,
                "surface_tension": p.surface_tension
            }
            for p in products
        ]
    }

@app.post("/api/scan")
async def scan_upc(request: UPCScanRequest):
    """Scan UPC code and get product info"""
    context = controller.handle_upc_scan(request.upc_code)
    
    if context.status == "upc_not_found":
        raise HTTPException(status_code=404, detail="UPC code not found")
    
    return {
        "status": "success",
        "product": {
            "upc_code": context.product.upc_code,
            "product_name": context.product.product_name,
            "viscosity": context.product.viscosity,
            "density": context.product.density,
            "surface_tension": context.product.surface_tension
        },
        "profile": {
            "valve_timing": context.profile.valve_timing,
            "pressure": context.profile.pressure,
            "nozzle_diameter": context.profile.nozzle_diameter,
            "target_volume": context.profile.target_volume,
            "accuracy": context.profile.accuracy
        } if context.profile else None
    }

@app.post("/api/predict")
async def predict_fill(request: PredictFillRequest):
    """Get fill prediction from PINN"""
    result = controller.predict_fill(
        request.valve_timing,
        request.pressure,
        request.nozzle_diameter,
        request.target_volume,
        request.temperature
    )
    
    if result.prediction is None:
        raise HTTPException(status_code=400, detail="No product selected")
    
    response = {
        "prediction": result.prediction,
        "alert": result.alert,
        "recommendation": result.recommendation
    }
    
    return response

@app.post("/api/execute")
async def execute_fill(request: ExecuteFillRequest):
    """Execute fill and log results"""
    camera_image = None
    if request.use_vision and controller.vision_detector:
        # Simulate camera image
        camera_image = controller.vision_detector.simulate_camera_image(
            request.actual_volume
        )
    
    execution = controller.execute_fill(
        request.valve_timing,
        request.pressure,
        request.nozzle_diameter,
        request.target_volume,
        request.actual_volume,
        request.actual_time,
        request.temperature,
        camera_image
    )
    
    response = {
        "actual_volume": execution.actual_volume,
        "actual_time": execution.actual_time,
        "anomaly_detected": execution.anomaly_detected
    }
    
    if hasattr(execution, 'vision_result') and execution.vision_result:
        vision = execution.vision_result
        response["vision"] = {
            "detected_volume": vision.detected_volume,
            "confidence": vision.confidence,
            "liquid_height": vision.liquid_height,
            "has_foam": vision.has_foam,
            "image_quality": vision.image_quality
        }
    
    return response

@app.post("/api/products")
async def add_product(request: AddProductRequest):
    """Add new product"""
    success = controller.db.add_product(
        request.upc_code,
        request.product_name,
        request.viscosity,
        request.density,
        request.surface_tension
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add product")
    
    return {"status": "success", "message": "Product added successfully"}

@app.get("/api/health")
async def get_health_status():
    """Get equipment health status"""
    health_status = controller.get_health_status()
    alerts = controller.get_health_alerts()
    schedule = controller.get_maintenance_schedule()
    
    return {
        "components": {
            name: {
                "health_score": health.health_score,
                "accuracy_trend": health.accuracy_trend,
                "predicted_failure_date": health.predicted_failure_date.isoformat() if health.predicted_failure_date else None,
                "maintenance_recommended": health.maintenance_recommended
            }
            for name, health in health_status.items()
        },
        "alerts": [
            {
                "severity": alert.severity,
                "component": alert.component,
                "message": alert.message,
                "recommended_action": alert.recommended_action,
                "days_until_failure": alert.days_until_failure
            }
            for alert in alerts
        ],
        "maintenance_schedule": schedule
    }

@app.get("/api/spc")
async def get_spc_status():
    """Get SPC monitoring status"""
    alerts = controller.get_spc_alerts()
    chart_data = controller.get_spc_chart_data()
    capability = controller.get_process_capability()
    
    return {
        "alerts": [
            {
                "rule_name": alert.rule_name,
                "severity": alert.severity,
                "message": alert.message,
                "recommended_action": alert.recommended_action
            }
            for alert in alerts
        ],
        "chart_data": chart_data,
        "capability": capability
    }

@app.get("/api/anomalies")
async def get_anomalies(issue_type: Optional[str] = None):
    """Get anomalies from database"""
    if issue_type:
        solutions = controller.search_anomaly_solutions(issue_type)
        return {
            "solutions": [
                {
                    "anomaly_id": sol.anomaly_id,
                    "product_category": sol.product_category,
                    "viscosity_range": sol.viscosity_range,
                    "temperature_range": sol.temperature_range,
                    "issue_type": sol.issue_type,
                    "solution": sol.solution,
                    "effectiveness": sol.effectiveness,
                    "upvotes": sol.upvotes
                }
                for sol in solutions
            ]
        }
    else:
        stats = controller.anomaly_db.get_statistics()
        return {"statistics": stats}

@app.post("/api/anomalies")
async def report_anomaly(request: ReportAnomalyRequest):
    """Report new anomaly"""
    anomaly_id = controller.report_anomaly_to_db(
        request.issue_type,
        request.solution,
        request.effectiveness
    )
    
    if not anomaly_id:
        raise HTTPException(status_code=400, detail="Failed to report anomaly")
    
    return {
        "status": "success",
        "anomaly_id": anomaly_id
    }

@app.get("/api/dashboard")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    # Get recent fills
    if controller.current_context and controller.current_context.product:
        training_data = controller.db.get_training_data(
            controller.current_context.product.upc_code,
            limit=100
        )
    else:
        training_data = []
    
    # Calculate stats
    total_fills = len(training_data)
    avg_accuracy = 99.2  # Placeholder
    uptime = 98.5  # Placeholder
    
    return {
        "total_fills": total_fills,
        "avg_accuracy": avg_accuracy,
        "uptime": uptime,
        "current_product": {
            "upc_code": controller.current_context.product.upc_code,
            "product_name": controller.current_context.product.product_name
        } if controller.current_context and controller.current_context.product else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
