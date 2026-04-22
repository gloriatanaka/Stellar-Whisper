import pytest
import json
from datetime import datetime
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_tarot_deck_endpoint(client):
    """Test that the tarot deck endpoint works."""
    response = client.get('/tarot/deck')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'deck' in data
    assert 'count' in data
    assert data['count'] == 78
    # Check that the deck has 78 cards
    assert len(data['deck']) == 78
    # Check that cards have the expected fields (without 'reversed' in the base deck)
    for card in data['deck']:
        assert 'id' in card
        assert 'name' in card
        assert 'arcana' in card
        assert 'meaning_upright' in card
        assert 'meaning_reversed' in card
        # The base deck should not have 'reversed' key
        assert 'reversed' not in card

def test_tarot_draw_single_endpoint(client):
    """Test that the single card draw endpoint works."""
    response = client.post('/tarot/draw/single')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'card' in data
    assert 'meaning' in data
    # Check that the card has the expected fields
    card = data['card']
    assert 'id' in card
    assert 'name' in card
    assert 'arcana' in card
    assert 'meaning_upright' in card
    assert 'meaning_reversed' in card
    assert 'reversed' in card
    assert isinstance(card['reversed'], bool)
    # Check that meaning is a string
    assert isinstance(data['meaning'], str)
    assert len(data['meaning']) > 0

def test_tarot_draw_three_card_endpoint(client):
    """Test that the three-card spread endpoint works."""
    response = client.post('/tarot/draw/three-card')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'spread' in data
    assert isinstance(data['spread'], list)
    assert len(data['spread']) == 3
    # Check each position
    positions = ['past', 'present', 'future']
    for i, position_data in enumerate(data['spread']):
        assert 'position' in position_data
        assert position_data['position'] == positions[i]
        assert 'card' in position_data
        assert 'meaning' in position_data
        card = position_data['card']
        assert 'id' in card
        assert 'name' in card
        assert 'arcana' in card
        assert 'meaning_upright' in card
        assert 'meaning_reversed' in card
        assert 'reversed' in card
        assert isinstance(card['reversed'], bool)
        assert isinstance(position_data['meaning'], str)
        assert len(position_data['meaning']) > 0

def test_tarot_draw_single_endpoint_method_not_allowed(client):
    """Test that the single card draw endpoint only accepts POST."""
    response = client.get('/tarot/draw/single')
    assert response.status_code == 405  # Method Not Allowed

def test_tarot_draw_three_card_endpoint_method_not_allowed(client):
    """Test that the three-card spread endpoint only accepts POST."""
    response = client.get('/tarot/draw/three-card')
    assert response.status_code == 405  # Method Not Allowed

if __name__ == '__main__':
    pytest.main([__file__])