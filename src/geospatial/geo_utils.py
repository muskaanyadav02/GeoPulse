import math

def is_valid_gps(lat, lon):
    if lat is None or lon is None:
        return False
    if -90 <= lat <= 90 and -180 <= lon <= 180:
        return True
    return False


def get_distance_meters(lat1, lon1, lat2, lon2):
    # Approximate conversion: 1 degree is ~111,000 meters
    lat_diff = (lat2 - lat1) * 111000
    lon_diff = (lon2 - lon1) * 111000 * math.cos(math.radians(lat1))
    
    distance = math.sqrt(lat_diff**2 + lon_diff**2)
    return round(distance, 2)


if __name__ == "__main__":
    store1 = (26.8467, 80.9462)  # Hazratganj Store
    store2 = (26.8500, 80.9500)  # Gomti Nagar Hub
    
    print("Is Store 1 GPS valid?:", is_valid_gps(store1[0], store1[1]))
    dist = get_distance_meters(store1[0], store1[1], store2[0], store2[1])
    print(f"Distance between stores: {dist} meters")
