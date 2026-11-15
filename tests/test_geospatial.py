import sys
import os

# Add the root directory to Python path so we can import our geospatial utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.geospatial.geo_utils import is_valid_gps, get_distance_meters

def run_geospatial_tests():
    # Test 1: Check valid Lucknow store coordinates
    assert is_valid_gps(26.8467, 80.9462) is True, "Valid coordinates failed!"
    
    # Test 2: Check invalid GPS coordinates (out of range)
    assert is_valid_gps(120.0, 200.0) is False, "Invalid coordinates should return False!"
    assert is_valid_gps(None, 80.9462) is False, "Null latitude should return False!"
    
    # Test 3: Verify distance calculation between Hazratganj and Gomti Nagar Hub
    dist = get_distance_meters(26.8467, 80.9462, 26.8500, 80.9500)
    assert 500 <= dist <= 550, f"Unexpected distance calculated: {dist}"
    
    print("All Geospatial Unit Tests Passed Successfully!")

if __name__ == "__main__":
    run_geospatial_tests()
