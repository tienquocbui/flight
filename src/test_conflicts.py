#!/usr/bin/env python3
"""
Script để test các trường hợp xung đột khác nhau
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from models.waypoint import Waypoint, WaypointType
from models.flight import Flight
from models.airspace import Airspace
from algorithms.conflict_detection import detect_conflicts

def create_test_airspace():
    """Tạo airspace test với các waypoints"""
    airspace = Airspace()
    
    # Tạo các waypoints test
    waypoints = [
        ("A", 10.0, 106.0),
        ("B", 10.5, 106.5), 
        ("C", 11.0, 107.0),
        ("D", 10.8, 106.8),
        ("E", 11.2, 106.2),
        ("F", 10.2, 107.2),
    ]
    
    for name, lat, lon in waypoints:
        wp = Waypoint(name=name, latitude=lat, longitude=lon, wp_type=WaypointType.FIX)
        airspace.add_waypoint(wp)
    
    # Tạo routes
    routes = [
        ("A", "B", 50),
        ("B", "C", 60),
        ("A", "D", 40),
        ("D", "E", 45),
        ("C", "F", 55),
        ("E", "F", 35),
    ]
    
    for from_wp, to_wp, distance in routes:
        airspace.add_route(from_wp, to_wp, distance, "TEST", "BIDIRECTIONAL")
    
    return airspace

def create_conflict_test_flights():
    """Tạo các flights để test xung đột"""
    base_time = datetime.strptime("2025-01-19T08:00:00", "%Y-%m-%dT%H:%M:%S")
    
    flights = []
    
    # Test 1: Crossing conflict - 2 flights giao nhau tại waypoint B
    flight1 = Flight(
        callsign="TEST001",
        route=["A", "B", "C"],
        speed=450,
        flight_level=330,
        entry_time=base_time
    )
    
    flight2 = Flight(
        callsign="TEST002", 
        route=["D", "B", "E"],
        speed=460,
        flight_level=340,  # Gần cùng mực bay
        entry_time=base_time + timedelta(minutes=5)  # Cách 5 phút
    )
    
    # Test 2: Head-on conflict - 2 flights ngược chiều trên cùng route
    flight3 = Flight(
        callsign="TEST003",
        route=["A", "B"],
        speed=440,
        flight_level=350,
        entry_time=base_time + timedelta(minutes=10)
    )
    
    flight4 = Flight(
        callsign="TEST004",
        route=["B", "A"],  # Ngược chiều
        speed=450,
        flight_level=360,  # Gần cùng mực bay
        entry_time=base_time + timedelta(minutes=12)
    )
    
    # Test 3: Overtake conflict - 2 flights cùng chiều, cùng route
    flight5 = Flight(
        callsign="TEST005",
        route=["A", "B", "C"],
        speed=400,  # Chậm hơn
        flight_level=370,
        entry_time=base_time + timedelta(minutes=15)
    )
    
    flight6 = Flight(
        callsign="TEST006",
        route=["A", "B", "C"],  # Cùng route
        speed=500,  # Nhanh hơn
        flight_level=380,  # Gần cùng mực bay
        entry_time=base_time + timedelta(minutes=16)  # Cách 1 phút
    )
    
    # Test 4: Lateral conflict - 2 flights gần nhau cùng thời điểm
    flight7 = Flight(
        callsign="TEST007",
        route=["A", "D"],
        speed=430,
        flight_level=390,
        entry_time=base_time + timedelta(minutes=20)
    )
    
    flight8 = Flight(
        callsign="TEST008",
        route=["B", "E"],  # Route song song
        speed=440,
        flight_level=400,  # Gần cùng mực bay
        entry_time=base_time + timedelta(minutes=20)  # Cùng thời điểm
    )
    
    test_flights = [flight1, flight2, flight3, flight4, flight5, flight6, flight7, flight8]
    
    # Tính timeline cho tất cả flights
    for flight in test_flights:
        distances = {}
        for i in range(len(flight.route)-1):
            wp1, wp2 = flight.route[i], flight.route[i+1]
            # Tính distance đơn giản (có thể dùng haversine thực tế)
            distances[(wp1, wp2)] = 50  # Giả sử 50NM
        flight.calculate_estimated_times(distances)
    
    return test_flights

def test_conflicts():
    """Test tất cả các loại xung đột"""
    print("🚀 Bắt đầu test các trường hợp xung đột...")
    
    # Tạo airspace và flights test
    airspace = create_test_airspace()
    test_flights = create_conflict_test_flights()
    
    print(f"✅ Đã tạo {len(airspace.waypoints)} waypoints và {len(test_flights)} flights test")
    
    # Phát hiện xung đột
    conflicts = detect_conflicts(test_flights)
    
    print(f"\n🔍 Phát hiện được {len(conflicts)} xung đột:")
    
    for i, conflict in enumerate(conflicts, 1):
        print(f"\n{i}. {conflict['type'].upper()} CONFLICT:")
        print(f"   Flights: {conflict['flight1']} & {conflict['flight2']}")
        print(f"   Flight Levels: {conflict['flight_level1']} & {conflict['flight_level2']}")
        
        if conflict['type'] == 'crossing':
            print(f"   Waypoint: {conflict['waypoint']}")
            print(f"   Time: {conflict['start_time']} - {conflict['end_time']}")
        elif conflict['type'] in ['head-on', 'overtake']:
            print(f"   Segment: {' → '.join(conflict['segment'])}")
            print(f"   Time: {conflict['start_time']} - {conflict['end_time']}")
        elif conflict['type'] == 'lateral':
            print(f"   Waypoints: {conflict['wp1']} & {conflict['wp2']}")
            print(f"   Time: {conflict['time']}")
    
    return conflicts

if __name__ == "__main__":
    test_conflicts() 