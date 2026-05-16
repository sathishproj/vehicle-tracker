from math import radians, sin, cos, sqrt, atan2

def distance_meters(lat1, lon1, lat2, lon2):
    r = 6371000
    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return r * 2 * atan2(sqrt(a), sqrt(1-a))
