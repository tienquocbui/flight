from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime, timedelta
from typing import List, Dict
import os

from models.waypoint import Waypoint, WaypointType
from models.flight import Flight
from models.airspace import Airspace
from algorithms.conflict_detection import detect_conflicts
from algorithms.pathfinding import a_star_search

app = FastAPI(title="Air Traffic Control API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, limit origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
airspace = Airspace()
flights: List[Flight] = []

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in nautical miles using Haversine formula"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 3440.065  # Earth's radius in nautical miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def load_data():
    """Load initial data from JSON files"""
    try:
        # Get the directory where api.py is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # Load airspace data
        airspace_file = os.path.join(project_root, 'data', 'airspace_data.json')
        with open(airspace_file, 'r', encoding='utf-8') as f:
            airspace_data = json.load(f)
            
        # Add waypoints - handle new structure (array instead of object)
        waypoints = {}
        if isinstance(airspace_data['waypoints'], list):
            # New structure: waypoints is an array
            for wp_info in airspace_data['waypoints']:
                waypoint = Waypoint(
                    name=wp_info['name'],
                    latitude=wp_info['lat'],
                    longitude=wp_info['lon'],
                    wp_type=WaypointType.FIX
                )
                waypoints[wp_info['name']] = waypoint
                airspace.add_waypoint(waypoint)
        else:
            # Old structure: waypoints is an object
            for wp_name, wp_info in airspace_data['waypoints'].items():
                waypoint = Waypoint(
                    name=wp_name,
                    latitude=wp_info['lat'],
                    longitude=wp_info['lon'],
                    wp_type=WaypointType.FIX
                )
                waypoints[wp_name] = waypoint
                airspace.add_waypoint(waypoint)
        
        # Add edges/connections from JSON
        for edge in airspace_data.get('edges', []):
            source = edge['source']
            target = edge['target']
            distance = edge.get('distance_nm', 0)
            
            if source in waypoints and target in waypoints:
                airspace.add_route(source, target, distance, "AUTO", "BIDIRECTIONAL")
        
        # Load flight plans
        flight_file = os.path.join(project_root, 'data', 'flight_plans.json')
        with open(flight_file, 'r', encoding='utf-8') as f:
            flight_plans = json.load(f)
        
        base_time = datetime.strptime("2025-01-19", "%Y-%m-%d")
        
        for plan in flight_plans:
            try:
                # Parse route - handle both formats
                route_str = plan['Tuyến bay (từ - đến)']
                if '→' in route_str:
                    route = [wp.strip() for wp in route_str.split('→')]
                else:
                    route = [wp.strip() for wp in route_str.split('-')]
                
                # Parse flight level
                fl_str = plan['Mực bay']
                if fl_str.startswith('FL'):
                    fl = int(fl_str[2:])
                else:
                    fl = int(fl_str)
                
                # Parse entry time
                time_str = plan['Giờ vào FIR']
                hours, minutes = map(int, time_str.split(':'))
                entry_time = base_time + timedelta(hours=hours, minutes=minutes)
                
                flight = Flight(
                    callsign=plan['Tên tàu bay'],
                    route=route,
                    speed=float(plan['Tốc độ (Kts)']),
                    flight_level=fl,
                    entry_time=entry_time
                )
                
                # Calculate estimated times using actual distances
                distances = {}
                for i in range(len(route)-1):
                    wp1, wp2 = route[i], route[i+1]
                    if wp1 in airspace.waypoints and wp2 in airspace.waypoints:
                        wp1_data = airspace.waypoints[wp1]
                        wp2_data = airspace.waypoints[wp2]
                        dist = calculate_distance(
                            wp1_data.latitude, wp1_data.longitude,
                            wp2_data.latitude, wp2_data.longitude
                        )
                        distances[(wp1, wp2)] = dist
                
                flight.calculate_estimated_times(distances)
                flights.append(flight)
                
            except Exception as e:
                print(f"Error loading flight {plan.get('Tên tàu bay', 'Unknown')}: {e}")
                continue
                
        print(f"Loaded {len(airspace.waypoints)} waypoints and {len(flights)} flights from real database")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        # Create some default data if files not found
        create_default_data()

def create_default_data():
    """Create default airspace data if JSON files are not available"""
    # Add some default waypoints
    default_waypoints = [
        ("A", 10.0, 106.0),
        ("B", 10.5, 106.5),
        ("C", 11.0, 107.0),
        ("D", 10.8, 106.8),
    ]
    
    for name, lat, lon in default_waypoints:
        wp = Waypoint(name=name, latitude=lat, longitude=lon, wp_type=WaypointType.FIX)
        airspace.add_waypoint(wp)
    
    # Add connections
    for i in range(len(default_waypoints)-1):
        wp1_name = default_waypoints[i][0]
        wp2_name = default_waypoints[i+1][0]
        wp1 = airspace.waypoints[wp1_name]
        wp2 = airspace.waypoints[wp2_name]
        distance = calculate_distance(wp1.latitude, wp1.longitude, wp2.latitude, wp2.longitude)
        airspace.add_route(wp1_name, wp2_name, distance, "DEFAULT", "BIDIRECTIONAL")

@app.on_event("startup")
async def startup_event():
    load_data()

@app.get("/")
async def root():
    return {
        "message": "Air Traffic Control API",
        "version": "1.0.0",
        "waypoints_count": len(airspace.waypoints),
        "flights_count": len(flights)
    }

@app.get("/airspace")
async def get_airspace():
    """Get airspace data including waypoints and routes"""
    routes = []
    for wp_name, route_list in airspace.routes.items():
        for neighbor, distance, airway, direction in route_list:
            routes.append({
                "from": wp_name,
                "to": neighbor,
                "distance": distance,
                "airway": airway,
                "direction": direction
            })
    
    return {
        "waypoints": [
            {
                "name": wp.name,
                "latitude": wp.latitude,
                "longitude": wp.longitude,
                "type": wp.type.value
            }
            for wp in airspace.waypoints.values()
        ],
        "routes": routes
    }

@app.get("/flights")
async def get_flights():
    """Get all flights with their routes and timelines"""
    return [
        {
            "callsign": f.callsign,
            "route": f.route,
            "speed": f.speed,
            "flight_level": f.flight_level,
            "entry_time": f.entry_time.isoformat(),
            "timeline": {
                wp: time.isoformat() 
                for wp, time in f.estimated_times.items()
            }
        }
        for f in flights
    ]

@app.post("/flights")
async def add_flight(flight_data: dict):
    """Add a new flight to the system"""
    try:
        route = flight_data['route']
        if isinstance(route, str):
            route = [wp.strip() for wp in route.split(',')]
        
        entry_time = datetime.fromisoformat(flight_data['entry_time'])
        
        # Validate route waypoints exist
        for wp in route:
            if wp not in airspace.waypoints:
                raise HTTPException(
                    status_code=400,
                    detail=f"Waypoint {wp} not found in airspace"
                )
        
        new_flight = Flight(
            callsign=flight_data['callsign'],
            route=route,
            speed=float(flight_data['speed']),
            flight_level=int(flight_data['flight_level']),
            entry_time=entry_time
        )
        
        # Calculate distances for timeline
        distances = {}
        for i in range(len(route)-1):
            wp1, wp2 = route[i], route[i+1]
            wp1_data = airspace.waypoints[wp1]
            wp2_data = airspace.waypoints[wp2]
            dist = calculate_distance(
                wp1_data.latitude, wp1_data.longitude,
                wp2_data.latitude, wp2_data.longitude
            )
            distances[(wp1, wp2)] = dist
            
        new_flight.calculate_estimated_times(distances)
        flights.append(new_flight)
        return {"message": "Flight added successfully", "callsign": new_flight.callsign}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/conflicts")
async def get_conflicts():
    """Detect all conflicts between current flights"""
    conflicts = detect_conflicts(flights)
    
    # Convert datetime objects to ISO format strings
    for conflict in conflicts:
        if 'start_time' in conflict:
            conflict['start_time'] = conflict['start_time'].isoformat()
        if 'end_time' in conflict:
            conflict['end_time'] = conflict['end_time'].isoformat()
        if 'time' in conflict:
            conflict['time'] = conflict['time'].isoformat()
    
    return conflicts

@app.post("/suggest_path")
async def suggest_path(data: dict):
    """Find an alternative path for a flight to avoid conflicts"""
    callsign = data['callsign']
    start = data['start']
    goal = data['goal']
    
    # Validate waypoints
    if start not in airspace.waypoints or goal not in airspace.waypoints:
        raise HTTPException(
            status_code=400,
            detail="Invalid start or goal waypoint"
        )
    
    # Find the flight
    flight = next((f for f in flights if f.callsign == callsign), None)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # Get other flights for conflict checking
    other_flights = [f for f in flights if f.callsign != callsign]
    
    # Try to find alternative path using enhanced A* search
    from algorithms.pathfinding import find_alternative_path
    
    new_path = find_alternative_path(airspace, flight, start, goal, other_flights)
    
    if not new_path:
        raise HTTPException(status_code=404, detail="No alternative path found")
    
    # Calculate total distance of the new path
    total_distance = 0
    for i in range(len(new_path) - 1):
        wp1, wp2 = new_path[i], new_path[i+1]
        wp1_data = airspace.waypoints[wp1]
        wp2_data = airspace.waypoints[wp2]
        dist = calculate_distance(
            wp1_data.latitude, wp1_data.longitude,
            wp2_data.latitude, wp2_data.longitude
        )
        total_distance += dist
    
    return {
        "new_path": new_path,
        "total_distance_nm": round(total_distance, 2),
        "waypoints_count": len(new_path),
        "original_start": start,
        "original_goal": goal
    }

@app.post("/load_test_data")
async def load_test_data():
    """Load test data with conflicts for demonstration"""
    global flights, airspace
    
    # Clear existing data
    flights.clear()
    airspace = Airspace()
    
    # Import test functions
    from test_conflicts import create_test_airspace, create_conflict_test_flights
    
    # Create test airspace and flights
    airspace = create_test_airspace()
    test_flights = create_conflict_test_flights()
    flights.extend(test_flights)
    
    return {
        "message": "Test data loaded successfully",
        "waypoints_count": len(airspace.waypoints),
        "flights_count": len(flights)
    }

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    conflicts = detect_conflicts(flights)
    
    conflict_types = {}
    for conflict in conflicts:
        conflict_type = conflict['type']
        if conflict_type not in conflict_types:
            conflict_types[conflict_type] = 0
        conflict_types[conflict_type] += 1
    
    return {
        "waypoints_count": len(airspace.waypoints),
        "flights_count": len(flights),
        "conflicts_count": len(conflicts),
        "conflict_types": conflict_types,
        "routes_count": sum(len(routes) for routes in airspace.routes.values())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
