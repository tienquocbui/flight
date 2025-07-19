from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
from src.models.waypoint import Waypoint, WaypointType
from src.models.flight import Flight
from src.algorithms.conflict_detection import detect_conflicts
from src.algorithms.pathfinding import ConflictAwareAStar

app = Flask(__name__)
CORS(app)

# Load data
def load_airspace_data():
    with open('data/airspace_data-2.json', 'r') as f:
        return json.load(f)

def load_flight_plans():
    with open('data/flight_plans-2.json', 'r') as f:
        return json.load(f)

def parse_time(time_str):
    """Parse time string in format 'HH:MM' to datetime"""
    hours, minutes = map(int, time_str.split(':'))
    return datetime.now().replace(hour=hours, minute=minutes, second=0, microsecond=0)

def parse_flight_level(fl_str):
    """Parse flight level string 'FLXXX' to integer"""
    return int(fl_str[2:])

def parse_route(route_str):
    """Parse route string 'A → B → C' to list ['A', 'B', 'C']"""
    return [wp.strip() for wp in route_str.split('→')]

@app.route('/api/waypoints')
def get_waypoints():
    airspace_data = load_airspace_data()
    return jsonify(airspace_data['waypoints'])

@app.route('/api/flights')
def get_flights():
    flight_plans = load_flight_plans()
    return jsonify(flight_plans)

@app.route('/api/conflicts')
def get_conflicts():
    flight_plans = load_flight_plans()
    airspace_data = load_airspace_data()
    
    # Convert flight plans to Flight objects
    flights = []
    for plan in flight_plans:
        route = parse_route(plan['Tuyến bay (từ - đến)'])
        flight = Flight(
            callsign=plan['Tên tàu bay'],
            route=route,
            speed=float(plan['Tốc độ (Kts)']),
            flight_level=parse_flight_level(plan['Mực bay']),
            entry_time=parse_time(plan['Giờ vào FIR'])
        )
        
        # Calculate estimated times based on speed and distances
        waypoint_distances = {}  # You need to implement this based on your data
        flight.calculate_estimated_times(waypoint_distances)
        flights.append(flight)
    
    # Detect conflicts
    conflicts = detect_conflicts(flights)
    return jsonify(conflicts)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
