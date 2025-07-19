from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict, Set

class WaypointType(Enum):
    VOR = "VOR"  # VHF Omnidirectional Range
    NDB = "NDB"  # Non-Directional Beacon
    FIX = "FIX"  # Fixed point

@dataclass
class Waypoint:
    name: str
    latitude: float
    longitude: float
    type: WaypointType
    adjacent: Dict[str, float] = None  # Dictionary of adjacent waypoint names and their distances
    connected_by: Set[str] = None      # Set of airways that connect to this waypoint

    def __init__(self, name, latitude, longitude, wp_type):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.type = wp_type  # VOR, NDB, FIX, etc.

    def __repr__(self):
        return f"Waypoint({self.name}, {self.latitude}, {self.longitude}, {self.type})"

    def __post_init__(self):
        if self.adjacent is None:
            self.adjacent = {}
        if self.connected_by is None:
            self.connected_by = set()

    def add_adjacent(self, waypoint_name: str, distance: float, airway: str):
        """Add an adjacent waypoint with its distance and connecting airway"""
        self.adjacent[waypoint_name] = distance
        self.connected_by.add(airway)

    def get_coordinates(self) -> Tuple[float, float]:
        """Return waypoint coordinates as (latitude, longitude)"""
        return (self.latitude, self.longitude)

    def __eq__(self, other):
        if not isinstance(other, Waypoint):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
