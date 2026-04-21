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