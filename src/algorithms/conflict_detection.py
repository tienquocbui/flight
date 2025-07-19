from typing import List
from datetime import timedelta

def detect_conflicts(flights: List):
    conflicts = []
    for i in range(len(flights)):
        for j in range(i+1, len(flights)):
            f1, f2 = flights[i], flights[j]
            
            # 1. Trường hợp giao nhau (crossing) - cải thiện
            common_waypoints = set(f1.route) & set(f2.route)
            for wp in common_waypoints:
                t1 = f1.estimated_times.get(wp)
                t2 = f2.estimated_times.get(wp)
                if t1 and t2:
                    fl_diff = abs(f1.flight_level - f2.flight_level) * 100
                    # Giảm ngưỡng phát hiện xung đột
                    if fl_diff < 2000:  # 2000ft thay vì 1000ft
                        # Mở rộng window thời gian
                        time_diff = abs((t1 - t2).total_seconds()) / 60
                        if time_diff < 15:  # 15 phút thay vì 10 phút
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
            
            # 2. Cùng đường bay, ngược chiều (head-on) - cải thiện
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
                            if fl_diff < 2000:
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
            
            # 3. Cùng đường bay, cùng chiều (overtake) - cải thiện
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
                            if fl_diff < 2000:
                                # Kiểm tra thời gian cách nhau
                                time_diff = abs((t1_start - t2_start).total_seconds()) / 60
                                if time_diff < 20:  # 20 phút thay vì 10 phút
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
            
            # 4. Đường song song, không giao cắt (lateral) - cải thiện
            for wp1, t1 in f1.estimated_times.items():
                for wp2, t2 in f2.estimated_times.items():
                    if wp1 != wp2:  # Không phải cùng waypoint
                        time_diff = abs((t1 - t2).total_seconds()) / 60
                        if time_diff < 5:  # 5 phút thay vì 1 phút
                            fl_diff = abs(f1.flight_level - f2.flight_level) * 100
                            if fl_diff < 2000:
                                conflicts.append({
                                    'type': 'lateral',
                                    'flight1': f1.callsign,
                                    'flight2': f2.callsign,
                                    'wp1': wp1,
                                    'wp2': wp2,
                                    'time': t1,
                                    'flight_level1': f1.flight_level,
                                    'flight_level2': f2.flight_level,
                                    'time_diff_minutes': time_diff
                                })
    
    return conflicts 