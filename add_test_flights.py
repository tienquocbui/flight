#!/usr/bin/env python3
"""
Script để thêm test flights vào hệ thống
Sử dụng: python add_test_flights.py [test_case_name]
"""

import json
import sys
import os
from datetime import datetime, timedelta

def load_test_cases():
    """Load test cases từ file"""
    try:
        with open('test_conflict_cases.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ File test_conflict_cases.json không tìm thấy!")
        return []

def load_existing_flights():
    """Load flights hiện tại"""
    try:
        with open('data/flight_plans.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ File data/flight_plans.json không tìm thấy!")
        return []

def save_flights(flights):
    """Lưu flights vào file"""
    try:
        with open('data/flight_plans.json', 'w', encoding='utf-8') as f:
            json.dump(flights, f, indent=4, ensure_ascii=False)
        print("✅ Đã lưu flights thành công!")
    except Exception as e:
        print(f"❌ Lỗi khi lưu file: {e}")

def add_test_case(test_case_name):
    """Thêm test case vào hệ thống"""
    test_cases = load_test_cases()
    existing_flights = load_existing_flights()
    
    if not test_cases:
        return
    
    # Tìm test case
    test_case = None
    for tc in test_cases:
        if tc['test_case'] == test_case_name:
            test_case = tc
            break
    
    if not test_case:
        print(f"❌ Không tìm thấy test case: {test_case_name}")
        print("📋 Các test cases có sẵn:")
        for tc in test_cases:
            print(f"  - {tc['test_case']}: {tc['description']}")
        return
    
    print(f"🚀 Thêm test case: {test_case['test_case']}")
    print(f"📝 Mô tả: {test_case['description']}")
    print(f"🎯 Xung đột mong đợi: {test_case['expected_conflicts']}")
    print(f"📍 Vị trí xung đột: {test_case['conflict_location']}")
    print(f"⏰ Thời gian xung đột: {test_case['conflict_time']}")
    
    # Thêm flights vào danh sách hiện tại
    new_flights = existing_flights + test_case['flights']
    
    # Cập nhật STT
    for i, flight in enumerate(new_flights):
        flight['STT'] = i + 1
    
    # Lưu file
    save_flights(new_flights)
    
    print(f"✅ Đã thêm {len(test_case['flights'])} flights mới!")
    print(f"📊 Tổng số flights: {len(new_flights)}")

def list_test_cases():
    """Liệt kê tất cả test cases"""
    test_cases = load_test_cases()
    
    if not test_cases:
        print("❌ Không có test cases nào!")
        return
    
    print("📋 Danh sách test cases:")
    print("=" * 80)
    
    for i, tc in enumerate(test_cases, 1):
        print(f"{i}. {tc['test_case']}")
        print(f"   📝 {tc['description']}")
        print(f"   🎯 Xung đột: {tc['expected_conflicts']}")
        print(f"   📍 Vị trí: {tc['conflict_location']}")
        print(f"   ⏰ Thời gian: {tc['conflict_time']}")
        if 'notes' in tc:
            print(f"   📌 Ghi chú: {tc['notes']}")
        print()

def add_all_test_cases():
    """Thêm tất cả test cases"""
    test_cases = load_test_cases()
    existing_flights = load_existing_flights()
    
    if not test_cases:
        print("❌ Không có test cases nào!")
        return
    
    print("🚀 Thêm tất cả test cases...")
    
    # Thêm tất cả flights từ test cases
    all_new_flights = []
    for tc in test_cases:
        all_new_flights.extend(tc['flights'])
    
    new_flights = existing_flights + all_new_flights
    
    # Cập nhật STT
    for i, flight in enumerate(new_flights):
        flight['STT'] = i + 1
    
    # Lưu file
    save_flights(new_flights)
    
    print(f"✅ Đã thêm {len(all_new_flights)} flights từ {len(test_cases)} test cases!")
    print(f"📊 Tổng số flights: {len(new_flights)}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🚀 Air Traffic Control - Test Cases Manager")
        print("=" * 50)
        print("Sử dụng:")
        print("  python add_test_flights.py list                    - Liệt kê test cases")
        print("  python add_test_flights.py all                     - Thêm tất cả test cases")
        print("  python add_test_flights.py <test_case_name>        - Thêm test case cụ thể")
        print()
        print("Ví dụ:")
        print("  python add_test_flights.py CROSSING_CONFLICT_1")
        print("  python add_test_flights.py HEAD_ON_CONFLICT_1")
        print("  python add_test_flights.py OVERTAKE_CONFLICT_1")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_test_cases()
    elif command == 'all':
        add_all_test_cases()
    else:
        add_test_case(sys.argv[1])

if __name__ == "__main__":
    main() 