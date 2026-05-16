def detect_anomaly(speed, latitude, longitude):
    reasons = []

    if speed > 80:
        reasons.append("Overspeed detected")

    if latitude < 17.20 or latitude > 17.60:
        reasons.append("Latitude outside normal city route")

    if longitude < 78.20 or longitude > 78.80:
        reasons.append("Longitude outside normal city route")

    if speed < 0:
        reasons.append("Invalid speed value")

    if reasons:
        return True, ", ".join(reasons)

    return False, "Normal"