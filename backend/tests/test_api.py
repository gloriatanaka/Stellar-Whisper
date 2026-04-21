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

# New tests for the monthly horoscope endpoint
def test_horoscope_monthly_endpoint_valid_sign(client):
    """Test that the monthly horoscope endpoint works with valid sign."""
    response = client.get('/horoscope/monthly/aries')
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