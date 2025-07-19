import heapq
from math import radians, sin, cos, sqrt, atan2
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in nautical miles using Haversine formula"""
    R = 3440.065  # Earth's radius in nautical miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def calculate_turn_angle(path, current, next_wp):
    """Calculate turn angle between segments"""
    if len(path) < 2:
        return 0
    
    # Get coordinates for the three points
    prev_wp = path[-2]
    current_wp = current
    next_wp = next_wp
    
    # Calculate bearings
    def bearing(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        y = sin(dlon) * cos(lat2)
        x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
        return atan2(y, x)
    
    # Calculate turn angle
    bearing1 = bearing(prev_wp.latitude, prev_wp.longitude, current_wp.latitude, current_wp.longitude)
    bearing2 = bearing(current_wp.latitude, current_wp.longitude, next_wp.latitude, next_wp.longitude)
    
    angle = abs(bearing2 - bearing1)
    if angle > 3.14159:  # pi
        angle = 2 * 3.14159 - angle
    
    return angle * 180 / 3.14159  # Convert to degrees

def a_star_search(airspace, start, goal, flight, other_flights, constraints=None):
    """
    Enhanced A* search with conflict avoidance and aviation constraints
    """
    if start not in airspace.waypoints or goal not in airspace.waypoints:
        return None
    
    open_set = []
    heapq.heappush(open_set, (0, 0, [start]))  # (f_score, g_score, path)
    closed = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: haversine(
        airspace.waypoints[start].latitude, airspace.waypoints[start].longitude,
        airspace.waypoints[goal].latitude, airspace.waypoints[goal].longitude
    )}
    
    while open_set:
        current_f, current_g, path = heapq.heappop(open_set)
        current = path[-1]
        
        if current == goal:
            return path
        
        if current in closed:
            continue
        
        closed.add(current)
        
        # Get current waypoint object
        current_wp = airspace.waypoints[current]
        
        # Check all possible routes from current waypoint
        for neighbor, distance, airway, direction in airspace.routes.get(current, []):
            if neighbor in closed:
                continue
            
            # Check route direction constraint
            if direction == "ONEWAY":
                # For one-way routes, check if we're going in the right direction
                # This is a simplified check - in real implementation you'd check airway direction
                pass
            
            # Check turn angle constraint - only if we have enough waypoints
            if len(path) >= 2:
                neighbor_wp = airspace.waypoints[neighbor]
                try:
                    turn_angle = calculate_turn_angle(path, current_wp, neighbor_wp)
                    if turn_angle > 90:  # Maximum turn angle of 90 degrees
                        continue
                except Exception as e:
                    # If turn angle calculation fails, continue anyway
                    print(f"Warning: Turn angle calculation failed: {e}")
                    pass
            
            # Check conflict avoidance
            if not is_safe_route(airspace, current, neighbor, flight, other_flights):
                continue
            
            tentative_g = g_score[current] + distance
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                
                # Calculate heuristic (distance to goal)
                neighbor_wp = airspace.waypoints[neighbor]
                goal_wp = airspace.waypoints[goal]
                h = haversine(
                    neighbor_wp.latitude, neighbor_wp.longitude,
                    goal_wp.latitude, goal_wp.longitude
                )
                
                f_score[neighbor] = tentative_g + h
                
                # Add to open set
                new_path = path + [neighbor]
                heapq.heappush(open_set, (f_score[neighbor], tentative_g, new_path))
    
    return None

def is_safe_route(airspace, from_wp, to_wp, flight, other_flights):
    """
    Check if a route segment is safe from conflicts
    """
    # Check if any other flight is using this route segment at the same time
    for other_flight in other_flights:
        # Check if other flight uses this route segment
        for i in range(len(other_flight.route) - 1):
            if (other_flight.route[i] == from_wp and other_flight.route[i+1] == to_wp) or \
               (other_flight.route[i] == to_wp and other_flight.route[i+1] == from_wp):
                
                # Check if flight levels are too close
                fl_diff = abs(flight.flight_level - other_flight.flight_level) * 100
                if fl_diff < 1000:  # Less than 1000ft separation
                    return False
    
    return True

def find_alternative_path(airspace, flight, start, goal, other_flights, max_attempts=5):
    """
    Find alternative path with multiple attempts and different strategies
    """
    # Strategy 1: Standard A* with conflict avoidance
    path = a_star_search(airspace, start, goal, flight, other_flights)
    if path:
        return path
    
    # Strategy 2: Relaxed constraints (allow higher flight levels)
    original_fl = flight.flight_level
    for attempt in range(max_attempts):
        # Try different flight levels
        flight.flight_level = original_fl + (attempt + 1) * 1000  # Increase by 1000ft each attempt
        path = a_star_search(airspace, start, goal, flight, other_flights)
        if path:
            flight.flight_level = original_fl  # Restore original
            return path
    
    flight.flight_level = original_fl  # Restore original
    
    # Strategy 3: Find path with minimal conflicts
    return find_minimal_conflict_path(airspace, start, goal, flight, other_flights)

def find_minimal_conflict_path(airspace, start, goal, flight, other_flights):
    """
    Find path with minimal conflicts when no conflict-free path exists
    """
    # This is a simplified implementation
    # In a real system, you'd implement more sophisticated conflict resolution
    
    # Try to find a path that minimizes the number of conflicts
    open_set = []
    heapq.heappush(open_set, (0, 0, [start]))  # (conflicts, distance, path)
    closed = set()
    
    while open_set:
        conflicts, distance, path = heapq.heappop(open_set)
        current = path[-1]
        
        if current == goal:
            return path
        
        if current in closed:
            continue
        
        closed.add(current)
        
        for neighbor, dist, airway, direction in airspace.routes.get(current, []):
            if neighbor in closed:
                continue
            
            # Count conflicts on this segment
            segment_conflicts = count_segment_conflicts(current, neighbor, flight, other_flights)
            
            new_path = path + [neighbor]
            new_conflicts = conflicts + segment_conflicts
            new_distance = distance + dist
            
            heapq.heappush(open_set, (new_conflicts, new_distance, new_path))
    
    return None

def count_segment_conflicts(from_wp, to_wp, flight, other_flights):
    """
    Count number of conflicts on a route segment
    """
    conflicts = 0
    for other_flight in other_flights:
        for i in range(len(other_flight.route) - 1):
            if (other_flight.route[i] == from_wp and other_flight.route[i+1] == to_wp) or \
               (other_flight.route[i] == to_wp and other_flight.route[i+1] == from_wp):
                fl_diff = abs(flight.flight_level - other_flight.flight_level) * 100
                if fl_diff < 1000:
                    conflicts += 1
    return conflicts
