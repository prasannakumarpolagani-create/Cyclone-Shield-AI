import math


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate approximate distance between two geographic points.
    Returns distance in kilometers.
    """

    earth_radius = 6371

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


def calculate_risk(asset, cyclone):
    """
    Calculate prototype infrastructure vulnerability score.
    """

    # Distance between infrastructure and cyclone
    distance = calculate_distance(
        asset["latitude"],
        asset["longitude"],
        cyclone["latitude"],
        cyclone["longitude"]
    )

    # Wind risk
    wind_risk = min(
        cyclone["wind_speed"] / 2,
        100
    )

    # Distance risk
    if cyclone["radius"] > 0:
        distance_risk = max(
            0,
            100 - (
                distance /
                cyclone["radius"]
            ) * 100
        )
    else:
        distance_risk = 0

    # Elevation risk
    elevation_risk = max(
        0,
        100 - asset["elevation"] * 5
    )

    # Infrastructure criticality
    criticality_risk = (
        asset["criticality"] * 20
    )

    # Final risk score
    score = (
        0.35 * wind_risk
        + 0.30 * distance_risk
        + 0.20 * elevation_risk
        + 0.15 * criticality_risk
    )

    score = round(
        min(score, 100),
        2
    )

    # Risk classification
    if score >= 80:
        level = "CRITICAL"

    elif score >= 60:
        level = "HIGH"

    elif score >= 30:
        level = "MEDIUM"

    else:
        level = "LOW"

    return distance, score, level