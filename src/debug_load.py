#!/usr/bin/env python3
"""
Debug script to test data loading
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from datetime import datetime, timedelta
from models.waypoint import Waypoint, WaypointType
from models.flight import Flight
from models.airspace import Airspace

def test_load_data():
    """Test loading data from JSON files"""
    try:
        # Get the directory where api.py is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        print(f"Project root: {project_root}")
        
        # Load airspace data
        airspace_file = os.path.join(project_root, 'data', 'airspace_data.json')
        print(f"Loading airspace from: {airspace_file}")
        
        with open(airspace_file, 'r', encoding='utf-8') as f:
            airspace_data = json.load(f)
        
        print(f"Airspace data keys: {list(airspace_data.keys())}")
        print(f"Waypoints type: {type(airspace_data['waypoints'])}")
        print(f"Number of waypoints: {len(airspace_data['waypoints'])}")
        print(f"Number of edges: {len(airspace_data.get('edges', []))}")
        
        # Test waypoint loading
        airspace = Airspace()
        waypoints = {}
        
        if isinstance(airspace_data['waypoints'], list):
            print("Processing waypoints as array...")
            for wp_info in airspace_data['waypoints']:
                print(f"Processing waypoint: {wp_info['name']}")
                waypoint = Waypoint(
                    name=wp_info['name'],
                    latitude=wp_info['lat'],
                    longitude=wp_info['lon'],
                    wp_type=WaypointType.FIX
                )
                waypoints[wp_info['name']] = waypoint
                airspace.add_waypoint(waypoint)
        else:
            print("Processing waypoints as object...")
            for wp_name, wp_info in airspace_data['waypoints'].items():
                waypoint = Waypoint(
                    name=wp_name,
                    latitude=wp_info['lat'],
                    longitude=wp_info['lon'],
                    wp_type=WaypointType.FIX
                )
                waypoints[wp_name] = waypoint
                airspace.add_waypoint(waypoint)
        
        print(f"Successfully loaded {len(airspace.waypoints)} waypoints")
        
        # Test edges loading
        for edge in airspace_data.get('edges', []):
            source = edge['source']
            target = edge['target']
            distance = edge.get('distance_nm', 0)
            
            if source in waypoints and target in waypoints:
                airspace.add_route(source, target, distance, "AUTO", "BIDIRECTIONAL")
        
        print(f"Successfully loaded {sum(len(routes) for routes in airspace.routes.values())} routes")
        
        # Test flight plans loading
        flight_file = os.path.join(project_root, 'data', 'flight_plans.json')
        print(f"Loading flights from: {flight_file}")
        
        with open(flight_file, 'r', encoding='utf-8') as f:
            flight_plans = json.load(f)
        
        print(f"Number of flight plans: {len(flight_plans)}")
        
        flights = []
        base_time = datetime.strptime("2025-01-19", "%Y-%m-%d")
        
        for i, plan in enumerate(flight_plans):
            try:
                print(f"Processing flight {i+1}: {plan.get('Tên tàu bay', 'Unknown')}")
                
                # Parse route
                route_str = plan['Tuyến bay (từ - đến)']
                if '→' in route_str:
                    route = [wp.strip() for wp in route_str.split('→')]
                else:
                    route = [wp.strip() for wp in route_str.split('-')]
                
                print(f"  Route: {route}")
                
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
                
                # Calculate estimated times
                distances = {}
                for j in range(len(route)-1):
                    wp1, wp2 = route[j], route[j+1]
                    if wp1 in airspace.waypoints and wp2 in airspace.waypoints:
                        wp1_data = airspace.waypoints[wp1]
                        wp2_data = airspace.waypoints[wp2]
                        # Simple distance calculation for now
                        distances[(wp1, wp2)] = 50  # Assume 50NM
                
                flight.calculate_estimated_times(distances)
                flights.append(flight)
                print(f"  Successfully loaded flight {flight.callsign}")
                
            except Exception as e:
                print(f"  Error loading flight {plan.get('Tên tàu bay', 'Unknown')}: {e}")
                continue
        
        print(f"Successfully loaded {len(flights)} flights")
        print("Data loading test completed successfully!")
        
    except Exception as e:
        print(f"Error in test_load_data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_load_data() 