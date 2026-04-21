import pytest
import json
from datetime import datetime
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_horoscope_endpoint(client):
    """Test that the horoscope endpoint works."""
    response = client.get('/horoscope/aries')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'sign' in data
    assert data['sign'] == 'aries'
    assert 'horoscope' in data
    assert 'date' in data

def test_today_horoscope_endpoint(client):
    """Test that today's horoscope endpoint works."""
    response = client.get('/horoscope/today')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'date' in data
    assert 'horoscopes' in data
    assert len(data['horoscopes']) == 12

def test_birth_chart_endpoint_missing_fields(client):
    """Test that the birth chart endpoint validates required fields."""
    # Missing birth_date
    response = client.post('/api/birth-chart', 
                          json={'birth_time': '12:00:00', 'latitude': 40.0, 'longitude': -74.0})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'birth_date' in data['error']
    
    # Missing birth_time
    response = client.post('/api/birth-chart', 
                          json={'birth_date': '2023-04-20', 'latitude': 40.0, 'longitude': -74.0})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'birth_time' in data['error']
    
    # Missing latitude
    response = client.post('/api/birth-chart', 
                          json={'birth_date': '2023-04-20', 'birth_time': '12:00:00', 'longitude': -74.0})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'latitude' in data['error']
    
    # Missing longitude
    response = client.post('/api/birth-chart', 
                          json={'birth_date': '2023-04-20', 'birth_time': '12:00:00', 'latitude': 40.0})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'longitude' in data['error']

def test_birth_chart_endpoint_invalid_format(client):
    """Test that the birth chart endpoint validates input format."""
    # Invalid date format
    response = client.post('/api/birth-chart', 
                          json={'birth_date': '2023/04/20', 'birth_time': '12:00:00', 'latitude': 40.0, 'longitude': -74.0})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid input format' in data['error']
    
    # Invalid time format
    response = client.post('/api/birth-chart', 
                          json={'birth_date': '2023-04-20', 'birth_time': '12:00', 'latitude': 40.0, 'longitude': -74.0})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid input format' in data['error']
    
    # Invalid latitude (not a number)
    response = client.post('/api/birth-chart', 
                          json={'birth_date': '2023-04-20', 'birth_time': '12:00:00', 'latitude': 'invalid', 'longitude': -74.0})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid input format' in data['error']

def test_birth_chart_endpoint_valid_request(client):
    """Test that the birth chart endpoint works with valid input."""
    response = client.post('/api/birth-chart', 
                          json={
                              'birth_date': '2023-04-20',
                              'birth_time': '12:00:00',
                              'latitude': 40.0,
                              'longitude': -74.0
                          })
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Check that all expected fields are present
    expected_fields = ['birth_date', 'birth_time', 'latitude', 'longitude', 
                      'sun_sign', 'moon_sign', 'rising_sign', 'planetary_positions', 'calculated_at']
    for field in expected_fields:
        assert field in data, f"Missing field: {field}"
    
    # Check that the values are of correct type
    assert isinstance(data['sun_sign'], str)
    assert isinstance(data['moon_sign'], str)
    assert isinstance(data['rising_sign'], str)
    assert isinstance(data['planetary_positions'], dict)
    assert isinstance(data['calculated_at'], str)
    
    # Check that the sun sign is correct for April 20, 2023 (should be taurus)
    assert data['sun_sign'] == 'taurus'
    
    # Check that planetary positions contains expected planets
    expected_planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
    for planet in expected_planets:
        assert planet in data['planetary_positions']
        assert isinstance(data['planetary_positions'][planet], str)

if __name__ == '__main__':
    pytest.main([__file__])
def test_weekly_horoscope_endpoint(client):
    """Test that the weekly horoscope endpoint works."""
    response = client.get('/horoscope/weekly/aries')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'sign' in data
    assert data['sign'] == 'aries'
    assert 'horoscope' in data
    assert 'date' in data

def test_weekly_horoscope_endpoint_invalid_sign(client):
    """Test that the weekly horoscope endpoint returns 400 for invalid sign."""
    response = client.get('/horoscope/weekly/invalid')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

# New tests for the monthly horoscope endpoint
def test_horoscope_monthly_endpoint_valid_sign(client):
    """Test that the monthly horoscope endpoint works with valid sign."""
    response = client.get('/horoscope/monthly/aries')
# New tests for the specific date endpoint
def test_horoscope_specific_date_endpoint_valid(client):
    """Test that the horoscope for a specific date endpoint works with valid input."""
    response = client.get('/horoscope/aries/2026-04-21')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'sign' in data
    assert data['sign'] == 'aries'
    assert 'horoscope' in data
    assert 'date' in data

def test_horoscope_monthly_endpoint_invalid_sign(client):
    """Test that the monthly horoscope endpoint returns 400 for invalid sign."""
    response = client.get('/horoscope/monthly/invalid')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['date'] == '2026-04-21'

def test_horoscope_specific_date_endpoint_invalid_sign(client):
    """Test that the horoscope for a specific date endpoint returns 400 for invalid sign."""
    response = client.get('/horoscope/invalid/2026-04-21')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_horoscope_specific_date_endpoint_invalid_date_format(client):
    """Test that the horoscope for a specific date endpoint returns 400 for invalid date format."""
    response = client.get('/horoscope/aries/2026-13-01')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_horoscope_specific_date_endpoint_invalid_date(client):
    """Test that the horoscope for a specific date endpoint returns 400 for non-existent date."""
    response = client.get('/horoscope/aries/2026-02-30')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
