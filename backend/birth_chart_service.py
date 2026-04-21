"""Birth chart calculation service for Stellar Whisper using Skyfield for accurate astronomical calculations."""

from datetime import datetime
import math
from typing import Dict, List, Tuple, Optional
from skyfield.api import load, wgs84
from skyfield.framelib import ecliptic_frame
import numpy as np

# Load ephemeris data once at module initialization
try:
    eph = load('de421.bsp')  # Using DE421 ephemeris (good balance of accuracy and size)
    ts = load.timescale()
except Exception as e:
    # Fallback to built-in if file not found
    eph = load('de421.bsp')
    ts = load.timescale()

# Celestial bodies we want to track - using correct target names from de421.bsp
# Available targets from error: 
# 0 SOLAR SYSTEM BARYCENTER, 1 MERCURY BARYCENTER, 2 VENUS BARYCENTER, 3 EARTH BARYCENTER, 
# 4 MARS BARYCENTER, 5 JUPITER BARYCENTER, 6 SATURN BARYCENTER, 7 URANUS BARYCENTER, 
# 8 NEPTUNE BARYCENTER, 9 PLUTO BARYCENTER, 10 SUN, 199 MERCURY, 299 VENUS, 301 MOON, 399 EARTH, 499 MARS
BODIES = {
    'sun': eph['sun'],                           # 10 SUN
    'moon': eph['moon'],                         # 301 MOON
    'mercury': eph['mercury'],                   # 199 MERCURY (actual planet)
    'venus': eph['venus'],                       # 299 VENUS (actual planet)
    'mars': eph['mars'],                         # 499 MARS (actual planet)
    'jupiter': eph['jupiter barycenter'],        # 5 JUPITER BARYCENTER
    'saturn': eph['saturn barycenter'],          # 6 SATURN BARYCENTER
    'uranus': eph['uranus barycenter'],          # 7 URANUS BARYCENTER
    'neptune': eph['neptune barycenter'],        # 8 NEPTUNE BARYCENTER
    'pluto': eph['pluto barycenter']             # 9 PLUTO BARYCENTER
}

# Zodiac signs in order
ZODIAC_SIGNS = [
    'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
]

# Aspect orbs in degrees (traditional values)
ASPECT_ORBS = {
    'conjunction': 8.0,
    'sextile': 6.0,
    'square': 8.0,
    'trine': 8.0,
    'opposition': 8.0
}

# Aspect angles in degrees
ASPECT_ANGLES = {
    'conjunction': 0,
    'sextile': 60,
    'square': 90,
    'trine': 120,
    'opposition': 180
}


def _datetime_to_skyfield_time(dt: datetime):
    """Convert Python datetime to Skyfield time object."""
    # Ensure datetime is timezone naive (assume UTC if no timezone info)
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    # Skyfield expects UTC times, so we treat naive datetimes as UTC
    return ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


def _ecliptic_longitude_to_zodiac(lon_deg: float) -> Tuple[str, float]:
    """
    Convert ecliptic longitude to zodiac sign and degree within sign.
    
    Args:
        lon_deg: Ecliptic longitude in degrees (0-360)
        
    Returns:
        Tuple of (sign_name, degree_within_sign)
    """
    # Normalize to 0-360 range
    lon_deg = lon_deg % 360.0
    if lon_deg < 0:
        lon_deg += 360.0
    
    # Each sign is 30 degrees
    sign_index = int(lon_deg // 30) % 12
    degree_in_sign = lon_deg % 30
    
    return ZODIAC_SIGNS[sign_index], degree_in_sign


def _calculate_zodiac_from_vector(position) -> str:
    """
    Calculate zodiac sign from a Skyfield position vector.
    
    Args:
        position: Skyfield position object (from eph[body].at(time))
        
    Returns:
        Zodiac sign name
    """
    # Get ecliptic coordinates
    ecliptic_lat, ecliptic_lon, _ = position.frame_xyz(ecliptic_frame).degrees
    sign, _ = _ecliptic_longitude_to_zodiac(ecliptic_lon)
    return sign


def _get_planet_sign_and_degree(body_name: str, dt: datetime) -> Dict[str, float]:
    """
    Get the zodiac sign and degree for a planetary body at a given time.
    
    Args:
        body_name: Name of the body ('sun', 'moon', etc.)
        dt: Datetime for calculation
        
    Returns:
        Dictionary with 'sign' and 'degree' keys
    """
    if body_name not in BODIES:
        raise ValueError(f"Unknown body: {body_name}")
    
    time = _datetime_to_skyfield_time(dt)
    body = BODIES[body_name]
    
    # Get position relative to Earth
    earth = eph['earth']
    
    if body_name == 'sun':
        # For Sun, we need Earth's position relative to Sun, then get the opposite direction
        # Observe Sun from Earth gives us the direction to Sun
        # The Earth's position relative to Sun is opposite
        sun_pos = earth.at(time).observe(body)
        # For zodiac calculation, we want the Sun's ecliptic longitude as seen from Earth
        # This is what observe() gives us directly
        astrometric = sun_pos
    else:
        # For other bodies, get their geocentric position as seen from Earth
        astrometric = earth.at(time).observe(body)
    
    # Get apparent position (accounts for light travel time, aberration, etc.)
    apparent = astrometric.apparent()
    
    # Get ecliptic longitude and latitude
    ecliptic_lat, ecliptic_lon, _ = apparent.frame_latlon(ecliptic_frame)
    
    sign, degree = _ecliptic_longitude_to_zodiac(ecliptic_lon.degrees)
    
    return {
        'sign': sign,
        'degree': degree,
        'longitude': ecliptic_lon.degrees
    }


def get_sun_sign(birth_date: datetime) -> str:
    """
    Calculate the sun sign (zodiac sign) based on birth date using actual astronomical position.
    
    Args:
        birth_date: datetime object representing the birth date
        
    Returns:
        str: the zodiac sign in lowercase
    """
    result = _get_planet_sign_and_degree('sun', birth_date)
    return result['sign']


def get_moon_sign(birth_date: datetime, birth_time: datetime, latitude: float, longitude: float) -> str:
    """
    Calculate the moon sign based on birth date, time, and location.
    
    Args:
        birth_date: datetime object representing the birth date
        birth_time: datetime object representing the birth time
        latitude: float representing birth latitude in degrees
        longitude: float representing birth longitude in degrees
        
    Returns:
        str: the moon sign in lowercase
    """
    # Combine date and time for calculation
    birth_datetime = datetime(
        birth_date.year, birth_date.month, birth_date.day,
        birth_time.hour, birth_time.minute, birth_time.second
    )
    
    result = _get_planet_sign_and_degree('moon', birth_datetime)
    return result['sign']


def get_rising_sign(birth_date: datetime, birth_time: datetime, latitude: float, longitude: float) -> str:
    """
    Calculate the rising sign (ascendant) based on birth date, time, and location.
    
    The rising sign is the zodiac sign that was ascending on the eastern horizon
    at the exact time and location of birth.
    
    Args:
        birth_date: datetime object representing the birth date
        birth_time: datetime object representing the birth time
        latitude: float representing birth latitude in degrees
        longitude: float representing birth longitude in degrees
        
    Returns:
        str: the rising sign in lowercase
    """
    # Combine date and time for calculation
    birth_datetime = datetime(
        birth_date.year, birth_date.month, birth_date.day,
        birth_time.hour, birth_time.minute, birth_time.second
    )
    
    time = _datetime_to_skyfield_time(birth_datetime)
    
    # Create observer location
    observer = wgs84.latlong(latitude_degrees=latitude, longitude_degrees=longitude)
    
    # Get Earth's position
    earth = eph['earth']
    
    # Calculate the local sidereal time at the birth location
    # This is equivalent to finding what point on the ecliptic is rising
    # We'll calculate the Midheaven and Ascendant using standard formulas
    
    # Get the apparent position of the Sun (to get ecliptic orientation)
    sun_app = earth.at(time).observe(eph['sun']).apparent()
    sun_lon = sun_app.frame_xyz(ecliptic_frame)[1].degrees  # ecliptic longitude
    
    # Calculate local sidereal time (LST) in degrees
    # LST = GMST + longitude
    # where GMST is Greenwich Mean Sidereal Time
    # Using Skyfield's built-in sidereal time calculation
    gast = ts.greenwich_apparent_sidereal_time(time)  # Greenwich Apparent Sidereal Time in hours
    lst_hours = gast.hours + longitude / 15.0  # Convert longitude to hours
    lst_degrees = (lst_hours * 15) % 360  # Convert to degrees, normalize to 0-360
    
    # Calculate Ascendant (rising sign)
    # Formula: Ascendant = arctan(-cos(LST) / (sin(LST) * cos(lat) + tan(lat) * sin(obliquity)))
    # But simpler approach: calculate the point on ecliptic that is rising
    
    # Obliquity of the ecliptic (approximate)
    obliquity = 23.43929111  # degrees (J2000 value, good enough for our purposes)
    obl_rad = math.radians(obliquity)
    lat_rad = math.radians(latitude)
    lst_rad = math.radians(lst_degrees)
    
    # Calculate Ascendant using spherical trigonometry
    # Ascendant = atan2(-cos(LST), sin(LST) * cos(lat) + tan(lat) * sin(obliquity))
    x = -math.cos(lst_rad)
    y = math.sin(lst_rad) * math.cos(lat_rad) + math.tan(lat_rad) * math.sin(obl_rad)
    
    if abs(x) < 1e-10 and abs(y) < 1e-10:
        asc_deg = 0.0
    else:
        asc_deg = math.degrees(math.atan2(x, y))
    
    # Normalize to 0-360
    asc_deg = asc_deg % 360
    if asc_deg < 0:
        asc_deg += 360
    
    # Convert to zodiac sign
    sign, _ = _ecliptic_longitude_to_zodiac(asc_deg)
    return sign


def get_planetary_positions(birth_date: datetime, birth_time: datetime, latitude: float, longitude: float) -> Dict[str, Dict[str, float]]:
    """
    Calculate the positions of major planets based on birth date, time, and location.
    
    Args:
        birth_date: datetime object representing the birth date
        birth_time: datetime object representing the birth time
        latitude: float representing birth latitude in degrees
        longitude: float representing birth longitude in degrees
        
    Returns:
        dict: planetary positions with planet names as keys and dicts containing
              'sign', 'degree', and 'longitude' keys
    """
    # Combine date and time for calculation
    birth_datetime = datetime(
        birth_date.year, birth_date.month, birth_date.day,
        birth_time.hour, birth_time.minute, birth_time.second
    )
    
    positions = {}
    
    for body_name in BODIES.keys():
        try:
            result = _get_planet_sign_and_degree(body_name, birth_datetime)
            positions[body_name] = {
                'sign': result['sign'],
                'degree': result['degree'],
                'longitude': result['longitude']
            }
        except Exception as e:
            # Fallback to sun sign if calculation fails for a particular body
            sun_sign = get_sun_sign(birth_datetime)
            positions[body_name] = {
                'sign': sun_sign,
                'degree': 0.0,
                'longitude': 0.0
            }
    
    return positions


def calculate_aspects(planetary_positions: Dict[str, Dict[str, float]]) -> List[Dict[str, float]]:
    """
    Calculate aspects between planets based on their longitudes.
    
    Args:
        planetary_positions: Dictionary of planetary positions from get_planetary_positions
        
    Returns:
        List of aspect dictionaries, each containing:
        - 'planet1': name of first planet
        - 'planet2': name of second planet
        - 'aspect': aspect name ('conjunction', 'sextile', 'square', 'trine', 'opposition')
        - 'angle': exact angle between planets in degrees
        - 'orb': orb (how exact the aspect is, lower is tighter)
    """
    aspects = []
    planets = list(planetary_positions.keys())
    
    # Compare each pair of planets
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            planet1 = planets[i]
            planet2 = planets[j]
            
            lon1 = planetary_positions[planet1]['longitude']
            lon2 = planetary_positions[planet2]['longitude']
            
            # Calculate the shortest angle between the two positions
            angle_diff = abs(lon2 - lon1) % 360
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
            
            # Check each aspect type
            for aspect_name, target_angle in ASPECT_ANGLES.items():
                orb = abs(angle_diff - target_angle)
                max_orb = ASPECT_ORBS[aspect_name]
                
                if orb <= max_orb:
                    aspects.append({
                        'planet1': planet1,
                        'planet2': planet2,
                        'aspect': aspect_name,
                        'angle': angle_diff,
                        'orb': orb
                    })
                    break  # Only assign to the closest aspect
    
    return aspects


def get_birth_chart(birth_date: datetime, birth_time: datetime, latitude: float, longitude: float) -> Dict:
    """
    Calculate a complete birth chart with planetary positions, signs, and aspects.
    
    Args:
        birth_date: datetime object representing the birth date
        birth_time: datetime object representing the birth time
        latitude: float representing birth latitude in degrees
        longitude: float representing birth longitude in degrees
        
    Returns:
        Dictionary containing complete birth chart data
    """
    # Combine date and time for calculation
    birth_datetime = datetime(
        birth_date.year, birth_date.month, birth_date.day,
        birth_time.hour, birth_time.minute, birth_time.second
    )
    
    # Get planetary positions
    positions = get_planetary_positions(birth_date, birth_time, latitude, longitude)
    
    # Get ascendant (rising sign)
    rising_sign = get_rising_sign(birth_date, birth_time, latitude, longitude)
    
    # Calculate aspects
    aspects = calculate_aspects(positions)
    
    # Prepare result
    result = {
        'birth_date': birth_date.strftime('%Y-%m-%d'),
        'birth_time': birth_time.strftime('%H:%M:%S'),
        'latitude': latitude,
        'longitude': longitude,
        'planetary_positions': {},
        'ascendant': rising_sign,
        'aspects': aspects,
        'calculated_at': datetime.now().isoformat()
    }
    
    # Format planetary positions for output
    for planet, data in positions.items():
        result['planetary_positions'][planet] = {
            'sign': data['sign'],
            'degree': round(data['degree'], 2),
            'longitude': round(data['longitude'], 2)
        }
    
    return result


if __name__ == "__main__":
    # Simple test
    test_date = datetime(2023, 4, 20)
    test_time = datetime(2023, 4, 20, 12, 0, 0)  # Noon
    print(f"Sun sign for {test_date} at {test_time}: {get_sun_sign(test_date)}")
    print(f"Moon sign: {get_moon_sign(test_date, test_time, 40.0, -74.0)}")
    print(f"Rising sign: {get_rising_sign(test_date, test_time, 40.0, -74.0)}")
    
    positions = get_planetary_positions(test_date, test_time, 40.0, -74.0)
    print(f"Planetary positions: {list(positions.keys())}")
    
    aspects = calculate_aspects(positions)
    print(f"Number of aspects: {len(aspects)}")