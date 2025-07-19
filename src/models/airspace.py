from typing import Dict, List, Set, Tuple
from .waypoint import Waypoint
import math

class Airspace:
    def __init__(self):
        self.waypoints = {}  # name -> Waypoint
        self.routes = {}     # name -> list of (neighbor_name, distance, airway_name, direction)
        
    def add_waypoint(self, waypoint):
        self.waypoints[waypoint.name] = waypoint
        if waypoint.name not in self.routes:
            self.routes[waypoint.name] = []

    def add_route(self, from_wp, to_wp, distance, airway_name, direction="BIDIRECTIONAL"):
        # direction: "BIDIRECTIONAL", "ONEWAY"
        self.routes[from_wp].append((to_wp, distance, airway_name, direction))
        if direction == "BIDIRECTIONAL":
            self.routes[to_wp].append((from_wp, distance, airway_name, direction))
