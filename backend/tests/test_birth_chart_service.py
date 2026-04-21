import pytest
from datetime import datetime
# We will import the service once we create it
# For now, we expect it to be in backend.birth_chart_service
# We'll write tests for the sun sign calculation

def test_sun_sign_calculation():
    """Test that the sun sign is correctly calculated from a birth date."""
    from birth_chart_service import get_sun_sign
    
    # Test cases: (year, month, day, expected_sign)
    test_cases = [
        (2023, 3, 21, "aries"),   # Aries start
        (2023, 4, 19, "aries"),   # Aries end
        (2023, 4, 20, "taurus"),  # Taurus start
        (2023, 5, 20, "taurus"),  # Taurus end
        (2023, 5, 21, "gemini"),  # Gemini start
        (2023, 6, 20, "gemini"),  # Gemini end
        (2023, 6, 21, "cancer"),  # Cancer start
        (2023, 7, 22, "cancer"),  # Cancer end
        (2023, 7, 23, "leo"),     # Leo start
        (2023, 8, 22, "leo"),     # Leo end
        (2023, 8, 23, "virgo"),   # Virgo start
        (2023, 9, 22, "virgo"),   # Virgo end
        (2023, 9, 23, "libra"),   # Libra start
        (2023, 10, 22, "libra"),  # Libra end
        (2023, 10, 23, "scorpio"), # Scorpio start
        (2023, 11, 21, "scorpio"), # Scorpio end
        (2023, 11, 22, "sagittarius"), # Sagittarius start
        (2023, 12, 21, "sagittarius"), # Sagittarius end
        (2023, 12, 22, "capricorn"), # Capricorn start
        (2024, 1, 19, "capricorn"), # Capricorn end (note: 2024 is leap year)
        (2024, 1, 20, "aquarius"), # Aquarius start
        (2024, 2, 18, "aquarius"), # Aquarius end
        (2024, 2, 19, "pisces"),   # Pisces start
        (2024, 3, 20, "pisces"),   # Pisces end
    ]
    
    for year, month, day, expected in test_cases:
        date = datetime(year, month, day)
        assert get_sun_sign(date) == expected, f"Failed for {date}"


def test_moon_sign_calculation():
    """Test that the moon sign calculation function exists and returns a string."""
    from birth_chart_service import get_moon_sign
    
    # For now, we'll test that it returns a string (placeholder implementation)
    birth_date = datetime(2023, 4, 20)
    birth_time = datetime(2023, 4, 20, 12, 0)  # noon
    latitude = 40.0
    longitude = -74.0
    
    result = get_moon_sign(birth_date, birth_time, latitude, longitude)
    assert isinstance(result, str)
    assert len(result) > 0


def test_rising_sign_calculation():
    """Test that the rising sign calculation function exists and returns a string."""
    from birth_chart_service import get_rising_sign
    
    # For now, we'll test that it returns a string (placeholder implementation)
    birth_date = datetime(2023, 4, 20)
    birth_time = datetime(2023, 4, 20, 12, 0)  # noon
    latitude = 40.0
    longitude = -74.0
    
    result = get_rising_sign(birth_date, birth_time, latitude, longitude)
    assert isinstance(result, str)
    assert len(result) > 0


def test_planetary_positions_calculation():
    """Test that the planetary positions calculation function exists and returns a dict."""
    from birth_chart_service import get_planetary_positions
    
    # For now, we'll test that it returns a dict with expected keys
    birth_date = datetime(2023, 4, 20)
    birth_time = datetime(2023, 4, 20, 12, 0)  # noon
    latitude = 40.0
    longitude = -74.0
    
    result = get_planetary_positions(birth_date, birth_time, latitude, longitude)
    assert isinstance(result, dict)
    expected_planets = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
    for planet in expected_planets:
        assert planet in result
        assert isinstance(result[planet], str)
        assert len(result[planet]) > 0


if __name__ == "__main__":
    pytest.main([__file__])