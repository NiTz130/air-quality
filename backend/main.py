"""
Main FastAPI Application for Air Quality Monitoring System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.data_service import DataService
from fuzzy.fuzzy_controller import FuzzyController
from utils.alert_checker import AlertChecker

# Initialize FastAPI app
app = FastAPI(
    title="Air Quality Monitoring System",
    description="Real-time air quality monitoring with Fuzzy Logic Control",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
csv_path = os.path.join(os.path.dirname(__file__), "../data/dataset.csv")
data_service = DataService(csv_path)
fuzzy_controller = FuzzyController()

# Store current state
current_state = {
    "current_data": None,
    "control_output": None,
    "alerts": [],
    "last_update": None
}


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    global current_state
    print("Air Quality Monitoring System started")
    # Get initial data
    update_current_state()


def update_current_state():
    """Update current system state"""
    global current_state
    
    # Get current data
    data = data_service.get_current_record()
    current_state["current_data"] = data
    
    # Run fuzzy control
    control = fuzzy_controller.control(
        data["co2"],
        data["pm25"],
        data["humidity"],
        data["occupancy_count"]
    )
    current_state["control_output"] = control
    
    # Check alerts
    alerts = AlertChecker.generate_alerts(data)
    current_state["alerts"] = alerts
    current_state["last_update"] = datetime.now().isoformat()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Air Quality Monitoring System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/api/current-data")
async def get_current_data():
    """Get current environmental data"""
    update_current_state()
    return {
        "data": current_state["current_data"],
        "control": current_state["control_output"],
        "alerts": current_state["alerts"],
        "timestamp": current_state["last_update"]
    }


@app.get("/api/data-history/{count}")
async def get_data_history(count: int = 20):
    """Get historical data"""
    records = data_service.get_latest_records(count)
    return {
        "records": records,
        "count": len(records)
    }


@app.get("/api/all-data")
async def get_all_data(skip: int = 0, limit: int = 1000):
    """Get all historical data with pagination"""
    all_records = data_service.get_all_records()
    total = len(all_records)
    
    # Apply pagination
    paginated_records = all_records[skip:skip + limit]
    
    return {
        "records": paginated_records,
        "total": total,
        "skip": skip,
        "limit": limit,
        "returned": len(paginated_records)
    }


@app.get("/api/alerts")
async def get_alerts():
    """Get current alerts"""
    update_current_state()
    if not current_state["alerts"]:
        return {
            "alerts": [],
            "message": "Môi trường đang ổn định",
            "status": "normal"
        }
    return {
        "alerts": current_state["alerts"],
        "total": len(current_state["alerts"]),
        "status": "warning"
    }


@app.get("/api/control-output")
async def get_control_output():
    """Get fuzzy control output"""
    update_current_state()
    control = current_state["control_output"]
    
    return {
        "ventilation_level": control["ventilation_level"],
        "fan_status": control["fan_status"],
        "explanation": control["explanation"],
        "fuzzification": control["fuzzification"],
        "active_rules": control["active_rules"],
        "rule_count": control["rule_count"]
    }


@app.post("/api/fuzzy-control")
async def fuzzy_control(
    co2: float = 800,
    pm25: float = 30,
    humidity: float = 55,
    occupancy: int = 20
):
    """
    Run fuzzy control with custom parameters
    """
    control = fuzzy_controller.control(co2, pm25, humidity, occupancy)
    
    return {
        "input": {
            "co2": co2,
            "pm25": pm25,
            "humidity": humidity,
            "occupancy": occupancy
        },
        "output": {
            "ventilation_level": control["ventilation_level"],
            "fan_status": control["fan_status"],
            "explanation": control["explanation"]
        },
        "fuzzification": control["fuzzification"],
        "active_rules": control["active_rules"]
    }


@app.get("/api/system-info")
async def get_system_info():
    """Get system information"""
    return {
        "name": "Hệ thống giám sát chất lượng không khí trong phòng học",
        "version": "1.0.0",
        "description": "Điều khiển thiết bị thông gió bằng Fuzzy Logic Control",
        "features": [
            "Giám sát chỉ số môi trường theo thời gian thực",
            "Cảnh báo khi vượt ngưỡng",
            "Điều khiển quạt thông gió tự động",
            "Hiển thị dashboard trực quan",
            "Hỗ trợ dữ liệu mô phỏng từ CSV"
        ],
        "parameters": [
            "Nhiệt độ (°C)",
            "Độ ẩm (%)",
            "CO2 (ppm)",
            "PM2.5 (µg/m³)",
            "PM10 (µg/m³)",
            "TVOC (ppb)",
            "CO (ppm)",
            "Lượng người viên"
        ]
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
