from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta

@dataclass
class Flight:
    callsign: str
    route: List[str]         # List of waypoint names in the flight plan
    speed: float            # Speed in knots
    flight_level: int       # Flight level in hundreds of feet (e.g., 330 = 33,000 feet)
    entry_time: datetime    # Time of entry into the sector
    
    # Runtime tracking
    current_position: tuple = None  # (latitude, longitude)
    current_waypoint_idx: int = 0   # Index of the current/next waypoint in route
    estimated_times: Dict[str, datetime] = None  # Estimated time at each waypoint
    
    def __post_init__(self):
        if self.estimated_times is None:
            self.estimated_times = {}
            
    def update_position(self, current_time: datetime) -> None:
        """
        Update the flight's position based on the current time.
        This is a simplified linear interpolation between waypoints.
        In a real system, this would be more sophisticated.
        """
        if not self.estimated_times or len(self.estimated_times) < 2:
            return
            
        # Find the current segment
        current_wp = self.route[self.current_waypoint_idx]
        if current_time >= self.estimated_times[current_wp]:
            self.current_waypoint_idx += 1
            
    def calculate_estimated_times(self, waypoint_distances: Dict[tuple, float]) -> None:
        """
        Calculate estimated time at each waypoint based on speed and distances.
        waypoint_distances: Dictionary with (wp1, wp2) tuple keys and distance values
        """
        current_time = self.entry_time
        self.estimated_times[self.route[0]] = current_time
        
        for i in range(len(self.route) - 1):
            wp1, wp2 = self.route[i], self.route[i + 1]
            distance = waypoint_distances.get((wp1, wp2)) or waypoint_distances.get((wp2, wp1))
            if distance is None:
                continue
                
            # Calculate time to next waypoint (distance/speed gives hours, multiply by 3600 for seconds)
            travel_time = timedelta(seconds=(distance / self.speed) * 3600)
            current_time += travel_time
            self.estimated_times[wp2] = current_time
