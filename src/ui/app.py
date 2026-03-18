"""
Streamlit UI for PINNs-UPC Calibration System
"""
import streamlit as st
import yaml
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database import DatabaseLayer
from src.models.pinn_model import PINNModel
from src.optimizer import CalibrationOptimizer
from src.controller import CalibrationController

# Page configuration
st.set_page_config(
    page_title="PINNs-UPC Calibration System",
    page_icon="🔬",
    layout="wide"
)

@st.cache_resource
def initialize_system():
    """Initialize system components with advanced features"""
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
    from src.vision import FillLevelDetector
    from src.maintenance import EquipmentHealthMonitor
    from src.quality import SPCMonitor
    from src.anomaly import AnomalyDatabase
    
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
    
    # Initialize controller with all features
    controller = CalibrationController(
        db, model, optimizer, config,
        vision_detector=vision_detector,
        health_monitor=health_monitor,
        spc_monitor=spc_monitor,
        anomaly_db=anomaly_db
    )
    
    return controller, config

# Initialize
controller, config = initialize_system()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Scanner", 
    "Fill Monitor", 
    "Equipment Health", 
    "SPC Control Chart",
    "Anomaly Database",
    "Reports"
])

# Main content
st.title("🔬 PINNs-UPC Calibration System")
st.markdown("---")

if page == "Scanner":
    st.header("📱 UPC Scanner")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        upc_code = st.text_input("Enter UPC Code", max_chars=13)
        
        if st.button("Scan Product"):
            if upc_code:
                context = controller.handle_upc_scan(upc_code)
                
                if context.status == "upc_not_found":
                    st.error(f"UPC code {upc_code} not found in database")
                    st.info("Please add product manually below")
                else:
                    st.success(f"Product loaded: {context.product.product_name}")
                    st.session_state['current_product'] = context
            else:
                st.warning("Please enter a UPC code")
    
    with col2:
        if 'current_product' in st.session_state:
            context = st.session_state['current_product']
            if context.product:
                st.subheader("Current Product")
                st.write(f"**Name:** {context.product.product_name}")
                st.write(f"**UPC:** {context.product.upc_code}")
                st.write(f"**Viscosity:** {context.product.viscosity} Pa·s")
                st.write(f"**Density:** {context.product.density} kg/m³")
                st.write(f"**Surface Tension:** {context.product.surface_tension} N/m")
                
                if context.profile:
                    st.subheader("Calibration Profile")
                    st.write(f"**Valve Timing:** {context.profile.valve_timing:.2f} s")
                    st.write(f"**Pressure:** {context.profile.pressure:.2f} PSI")
                    st.write(f"**Nozzle Diameter:** {context.profile.nozzle_diameter:.2f} mm")
                    st.write(f"**Target Volume:** {context.profile.target_volume:.2f} mL")
    
    # Add new product form
    with st.expander("Add New Product"):
        with st.form("add_product"):
            new_upc = st.text_input("UPC Code")
            new_name = st.text_input("Product Name")
            new_viscosity = st.number_input("Viscosity (Pa·s)", min_value=0.001, max_value=10.0, value=0.001)
            new_density = st.number_input("Density (kg/m³)", min_value=500.0, max_value=2000.0, value=1000.0)
            new_surface_tension = st.number_input("Surface Tension (N/m)", min_value=0.02, max_value=0.08, value=0.05)
            
            if st.form_submit_button("Add Product"):
                success = controller.db.add_product(
                    new_upc, new_name, new_viscosity, new_density, new_surface_tension
                )
                if success:
                    st.success(f"Product {new_name} added successfully!")
                else:
                    st.error("Failed to add product")

elif page == "Fill Monitor":
    st.header("📊 Fill Monitor")
    
    if 'current_product' not in st.session_state:
        st.warning("Please scan a product first")
    else:
        context = st.session_state['current_product']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Fill Parameters")
            valve_timing = st.slider("Valve Timing (s)", 0.1, 5.0, 1.0, 0.1)
            pressure = st.slider("Pressure (PSI)", 10.0, 100.0, 50.0, 1.0)
            nozzle_diameter = st.slider("Nozzle Diameter (mm)", 2.0, 10.0, 5.0, 0.5)
            target_volume = st.number_input("Target Volume (mL)", 10.0, 5000.0, 500.0, 10.0)
            
            if st.button("Predict Fill"):
                result = controller.predict_fill(
                    valve_timing, pressure, nozzle_diameter, target_volume
                )
                
                st.session_state['prediction_result'] = result
        
        with col2:
            if 'prediction_result' in st.session_state:
                result = st.session_state['prediction_result']
                
                if result.prediction:
                    st.subheader("Prediction")
                    pred = result.prediction
                    
                    st.metric("Predicted Volume", f"{pred['predicted_volume']:.2f} mL")
                    st.metric("Predicted Time", f"{pred['predicted_time']:.2f} s")
                    st.metric("Confidence", f"{pred['confidence']*100:.1f}%")
                    
                    # Calculate error
                    error_pct = abs(pred['predicted_volume'] - target_volume) / target_volume * 100.0
                    
                    # Color-coded accuracy indicator
                    if error_pct <= 1.0:
                        st.success(f"✅ Accuracy: {100-error_pct:.2f}% (Excellent)")
                    elif error_pct <= 2.0:
                        st.warning(f"⚠️ Accuracy: {100-error_pct:.2f}% (Acceptable)")
                    else:
                        st.error(f"❌ Accuracy: {100-error_pct:.2f}% (Poor)")
                    
                    if result.alert:
                        st.warning(result.alert)
                    
                    if result.recommendation:
                        st.info("Recommended adjustments:")
                        st.write(result.recommendation)
                    
                    # Show similar anomalies if found
                    if 'similar_anomalies' in pred and pred['similar_anomalies']:
                        with st.expander("⚠️ Similar Past Issues Found"):
                            for sim in pred['similar_anomalies']:
                                st.write(f"**{sim.issue_type}** (Similarity: {sim.similarity_score*100:.0f}%)")
                                st.write(f"Solution: {sim.solution}")
                                st.write(f"Effectiveness: {sim.effectiveness*100:.0f}% | Upvotes: {sim.upvotes}")
                                st.markdown("---")
            
            # Simulate fill execution
            st.subheader("Execute Fill")
            actual_volume = st.number_input("Actual Volume (mL)", 10.0, 5000.0, target_volume, 1.0)
            actual_time = st.number_input("Actual Time (s)", 0.1, 10.0, 2.0, 0.1)
            
            # Vision detection simulation
            use_vision = st.checkbox("Simulate Vision Detection", value=True)
            
            if st.button("Log Fill Result"):
                camera_image = None
                if use_vision and controller.vision_detector:
                    # Simulate camera image
                    camera_image = controller.vision_detector.simulate_camera_image(
                        actual_volume, has_foam=False
                    )
                
                execution = controller.execute_fill(
                    valve_timing, pressure, nozzle_diameter,
                    target_volume, actual_volume, actual_time,
                    camera_image=camera_image
                )
                
                if execution.anomaly_detected:
                    st.error("⚠️ Anomaly detected!")
                else:
                    st.success("✅ Fill logged successfully")
                
                # Show vision results
                if hasattr(execution, 'vision_result') and execution.vision_result:
                    vision = execution.vision_result
                    st.info(f"📷 Vision: {vision.detected_volume:.2f}mL (confidence: {vision.confidence*100:.0f}%)")
                    if vision.has_foam:
                        st.warning("Foam detected!")
                    if vision.image_quality != "good":
                        st.warning(f"Image quality: {vision.image_quality}")

elif page == "Equipment Health":
    st.header("🔧 Equipment Health Monitor")
    
    # Health alerts
    alerts = controller.get_health_alerts()
    
    if alerts:
        st.subheader("⚠️ Active Alerts")
        for alert in alerts:
            if alert.severity == 'critical':
                st.error(f"**{alert.component.upper()}**: {alert.message}")
            elif alert.severity == 'warning':
                st.warning(f"**{alert.component.title()}**: {alert.message}")
            else:
                st.info(f"**{alert.component.title()}**: {alert.message}")
            
            st.write(f"Action: {alert.recommended_action}")
            if alert.days_until_failure:
                st.write(f"Days until failure: {alert.days_until_failure}")
            st.markdown("---")
    else:
        st.success("✅ All equipment healthy")
    
    # Component health status
    st.subheader("Component Health")
    health_status = controller.get_health_status()
    
    if health_status:
        cols = st.columns(4)
        for idx, (component, health) in enumerate(health_status.items()):
            with cols[idx % 4]:
                # Color-coded health score
                if health.health_score >= 98:
                    st.metric(component.title(), f"{health.health_score:.1f}%", delta="Good")
                elif health.health_score >= 95:
                    st.metric(component.title(), f"{health.health_score:.1f}%", delta="Warning", delta_color="normal")
                else:
                    st.metric(component.title(), f"{health.health_score:.1f}%", delta="Critical", delta_color="inverse")
    
    # Maintenance schedule
    st.subheader("Maintenance Schedule")
    schedule = controller.get_maintenance_schedule()
    
    if schedule:
        for task in schedule:
            priority_emoji = "🔴" if task['priority'] == 'high' else "🟡"
            st.write(f"{priority_emoji} **{task['component'].title()}** - {task['action']}")
            st.write(f"Health: {task['health_score']:.1f}% | Due: {task['recommended_date'].strftime('%Y-%m-%d')}")
            st.markdown("---")
    else:
        st.info("No maintenance required")

elif page == "SPC Control Chart":
    st.header("📊 Statistical Process Control")
    
    # SPC alerts
    spc_alerts = controller.get_spc_alerts()
    
    if spc_alerts:
        st.subheader("⚠️ SPC Rule Violations")
        for alert in spc_alerts:
            if alert.severity == 'critical':
                st.error(f"**{alert.rule_name}**: {alert.message}")
            else:
                st.warning(f"**{alert.rule_name}**: {alert.message}")
            st.write(f"Action: {alert.recommended_action}")
            st.markdown("---")
    else:
        st.success("✅ Process in control")
    
    # Control chart
    st.subheader("Control Chart")
    chart_data = controller.get_spc_chart_data()
    
    if chart_data['status'] == 'ok':
        import pandas as pd
        import plotly.graph_objects as go
        
        # Create control chart
        fig = go.Figure()
        
        # Add data points
        fig.add_trace(go.Scatter(
            x=list(range(len(chart_data['errors']))),
            y=chart_data['errors'],
            mode='lines+markers',
            name='Fill Error %',
            line=dict(color='blue')
        ))
        
        # Add control limits
        fig.add_hline(y=chart_data['ucl'], line_dash="dash", line_color="red", annotation_text="UCL")
        fig.add_hline(y=chart_data['uwl'], line_dash="dot", line_color="orange", annotation_text="UWL")
        fig.add_hline(y=chart_data['center'], line_dash="solid", line_color="green", annotation_text="Center")
        fig.add_hline(y=chart_data['lwl'], line_dash="dot", line_color="orange", annotation_text="LWL")
        fig.add_hline(y=chart_data['lcl'], line_dash="dash", line_color="red", annotation_text="LCL")
        
        fig.update_layout(
            title="Fill Error Control Chart",
            xaxis_title="Fill Number",
            yaxis_title="Error %",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Collecting data... Need at least 20 fills for control chart")
    
    # Process capability
    st.subheader("Process Capability")
    capability = controller.get_process_capability()
    
    if capability['status'] == 'ok':
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Cp", f"{capability['cp']:.2f}")
        with col2:
            st.metric("Cpk", f"{capability['cpk']:.2f}")
        with col3:
            st.metric("Capability", capability['capability'])
        
        st.info(capability['interpretation'])
    else:
        st.info("Need at least 30 fills for capability analysis")

elif page == "Anomaly Database":
    st.header("🌐 Global Anomaly Database")
    
    st.write("Search for solutions to common filling issues from the global community")
    
    # Search by issue type
    issue_type = st.selectbox(
        "Issue Type",
        ["foam_overflow", "clog", "drift", "underfill", "overfill"]
    )
    
    if st.button("Search Solutions"):
        solutions = controller.search_anomaly_solutions(issue_type)
        
        if solutions:
            st.subheader(f"Top Solutions for {issue_type}")
            for sol in solutions:
                st.write(f"**Solution** (Effectiveness: {sol.effectiveness*100:.0f}%, Upvotes: {sol.upvotes})")
                st.write(sol.solution)
                st.write(f"Product: {sol.product_category} | Viscosity: {sol.viscosity_range} | Temp: {sol.temperature_range}")
                st.markdown("---")
        else:
            st.info("No solutions found for this issue type")
    
    # Report new anomaly
    with st.expander("Report New Anomaly"):
        with st.form("report_anomaly"):
            report_issue = st.selectbox("Issue Type", 
                ["foam_overflow", "clog", "drift", "underfill", "overfill"])
            report_solution = st.text_area("Solution that worked")
            report_effectiveness = st.slider("Effectiveness", 0.0, 1.0, 0.9, 0.1)
            
            if st.form_submit_button("Submit to Database"):
                anomaly_id = controller.report_anomaly_to_db(
                    report_issue, report_solution, report_effectiveness
                )
                if anomaly_id:
                    st.success(f"Anomaly reported! ID: {anomaly_id}")
                else:
                    st.error("Failed to report anomaly")
    
    # Database statistics
    if controller.anomaly_db:
        stats = controller.anomaly_db.get_statistics()
        st.subheader("Database Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Anomalies", stats['total_anomalies'])
            st.metric("Total Upvotes", stats['total_upvotes'])
        with col2:
            st.metric("Avg Effectiveness", f"{stats['average_effectiveness']*100:.0f}%")

elif page == "Reports":
    st.header("📈 Reports Dashboard")
    
    st.info("Comprehensive reporting and analytics coming soon")

# Footer
st.markdown("---")
st.markdown("PINNs-UPC Calibration System | Technopack Hackathon MVP")
