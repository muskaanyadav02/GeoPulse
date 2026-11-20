import sys
import os
import json

# Add the root directory to Python path
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
    
    # Test 4: Verify geospatial_config.json file loads properly
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'utils', 'geospatial_config.json'))
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    assert config_data["city"] == "Lucknow", "Config city mismatch!"
    assert len(config_data["stores"]) == 3, "Expected 3 stores in config!"
    
    print("All 4 Geospatial & Config Unit Tests Passed Successfully!")

if __name__ == "__main__":
    run_geospatial_tests()

from src.geospatial.geo_utils import is_within_catchment
assert is_within_catchment(26.8470, 80.9465, 26.8467, 80.9462) is True, "Customer inside 500m should return True!"
assert is_within_catchment(26.8500, 80.9500, 26.8467, 80.9462) is False, "Customer outside 500m should return False!"
print("Catchment boundary check passed!")
