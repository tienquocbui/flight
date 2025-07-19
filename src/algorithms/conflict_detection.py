from typing import List
from datetime import timedelta
import sys
import os

# Add src directory to path to import airspace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def detect_conflicts(flights: List):
    conflicts = []
    for i in range(len(flights)):
        for j in range(i+1, len(flights)):
            f1, f2 = flights[i], flights[j]
            
            # 1. Trường hợp giao nhau (crossing)
            common_waypoints = set(f1.route) & set(f2.route)
            for wp in common_waypoints:
                t1 = f1.estimated_times.get(wp)
                t2 = f2.estimated_times.get(wp)
                if t1 and t2:
                    fl_diff = abs(f1.flight_level - f2.flight_level) * 100
                    if fl_diff < 1000:  # 1000ft
                        time_diff = abs((t1 - t2).total_seconds()) / 60
                        if time_diff < 10:  # 10 phút
                            conflicts.append({
                                'type': 'crossing',
                                'flight1': f1.callsign,
                                'flight2': f2.callsign,
                                'waypoint': wp,
                                'start_time': min(t1, t2),
                                'end_time': max(t1, t2),
                                'flight_level1': f1.flight_level,
                                'flight_level2': f2.flight_level,
                                'time_diff_minutes': time_diff
                            })
            
            # 2. Cùng đường bay, ngược chiều (head-on)
            for idx1 in range(len(f1.route)-1):
                seg1 = (f1.route[idx1], f1.route[idx1+1])
                for idx2 in range(len(f2.route)-1):
                    seg2 = (f2.route[idx2+1], f2.route[idx2])  # đảo ngược để kiểm tra ngược chiều
                    if seg1 == seg2:
                        t1_start = f1.estimated_times.get(seg1[0])
                        t1_end = f1.estimated_times.get(seg1[1])
                        t2_start = f2.estimated_times.get(seg2[0])
                        t2_end = f2.estimated_times.get(seg2[1])
                        
                        if t1_start and t1_end and t2_start and t2_end:
                            fl_diff = abs(f1.flight_level - f2.flight_level) * 100
                            if fl_diff < 1000:
                                # Kiểm tra overlap thời gian
                                if t1_start < t2_end and t2_start < t1_end:
                                    conflicts.append({
                                        'type': 'head-on',
                                        'flight1': f1.callsign,
                                        'flight2': f2.callsign,
                                        'segment': seg1,
                                        'start_time': max(t1_start, t2_start),
                                        'end_time': min(t1_end, t2_end),
                                        'flight_level1': f1.flight_level,
                                        'flight_level2': f2.flight_level
                                    })
            
            # 3. Cùng đường bay, cùng chiều (overtake)
            for idx1 in range(len(f1.route)-1):
                seg1 = (f1.route[idx1], f1.route[idx1+1])
                for idx2 in range(len(f2.route)-1):
                    seg2 = (f2.route[idx2], f2.route[idx2+1])
                    if seg1 == seg2:
                        t1_start = f1.estimated_times.get(seg1[0])
                        t1_end = f1.estimated_times.get(seg1[1])
                        t2_start = f2.estimated_times.get(seg2[0])
                        t2_end = f2.estimated_times.get(seg2[1])
                        
                        if t1_start and t1_end and t2_start and t2_end:
                            fl_diff = abs(f1.flight_level - f2.flight_level) * 100
                            if fl_diff < 1000:
                                # Kiểm tra thời gian cách nhau
                                time_diff = abs((t1_start - t2_start).total_seconds()) / 60
                                if time_diff < 10:  # 10 phút
                                    conflicts.append({
                                        'type': 'overtake',
                                        'flight1': f1.callsign,
                                        'flight2': f2.callsign,
                                        'segment': seg1,
                                        'start_time': min(t1_start, t2_start),
                                        'end_time': max(t1_end, t2_end),
                                        'flight_level1': f1.flight_level,
                                        'flight_level2': f2.flight_level,
                                        'time_diff_minutes': time_diff
                                    })
            
            # 4. Đường song song, không giao cắt (lateral)
            for wp1, t1 in f1.estimated_times.items():
                for wp2, t2 in f2.estimated_times.items():
                    if wp1 != wp2:  # Không phải cùng waypoint
                        time_diff = abs((t1 - t2).total_seconds()) / 60
                        if time_diff < 5:  # 5 phút
                            fl_diff = abs(f1.flight_level - f2.flight_level) * 100
                            if fl_diff < 1000:  # 1000ft
                                # Kiểm tra khoảng cách thực tế giữa 2 waypoint
                                try:
                                    # Import airspace safely
                                    from api import airspace
                                    if wp1 in airspace.waypoints and wp2 in airspace.waypoints:
                                        wp1_data = airspace.waypoints[wp1]
                                        wp2_data = airspace.waypoints[wp2]
                                        
                                        # Tính khoảng cách bằng Haversine
                                        from math import radians, sin, cos, sqrt, atan2
                                        R = 3440.065  # Earth's radius in nautical miles
                                        lat1, lon1, lat2, lon2 = map(radians, [
                                            wp1_data.latitude, wp1_data.longitude,
                                            wp2_data.latitude, wp2_data.longitude
                                        ])
                                        dlat = lat2 - lat1
                                        dlon = lon2 - lon1
                                        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
                                        c = 2 * atan2(sqrt(a), sqrt(1-a))
                                        distance = R * c
                                        
                                        if distance < 10:  # Khoảng cách < 10 Nm
                                            conflicts.append({
                                                'type': 'lateral',
                                                'flight1': f1.callsign,
                                                'flight2': f2.callsign,
                                                'wp1': wp1,
                                                'wp2': wp2,
                                                'time': t1,
                                                'flight_level1': f1.flight_level,
                                                'flight_level2': f2.flight_level,
                                                'time_diff_minutes': time_diff,
                                                'distance_nm': round(distance, 2)
                                            })
                                except Exception as e:
                                    # Nếu không thể tính khoảng cách, bỏ qua
                                    pass
    
    return conflicts 