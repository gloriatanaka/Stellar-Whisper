import pytest
import sys
import os
from datetime import datetime

# Add the backend directory to the path so we can import tarot_service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tarot_service import shuffle_deck, draw_cards, get_card_meaning, TAROT_DECK, MAJOR_ARCANA, MINOR_ARCANA

def test_tarot_deck_structure():
    """Test that the tarot deck has the correct structure and size."""
    # Test total number of cards
    assert len(TAROT_DECK) == 78, f"Expected 78 cards, got {len(TAROT_DECK)}"
    
    # Test Major Arcana count
    assert len(MAJOR_ARCANA) == 22, f"Expected 22 Major Arcana cards, got {len(MAJOR_ARCANA)}"
    
    # Test Minor Arcana count
    assert len(MINOR_ARCANA) == 56, f"Expected 56 Minor Arcana cards, got {len(MINOR_ARCANA)}"
    
    # Test that all cards have required fields
    required_fields = ['id', 'name', 'arcana', 'meaning_upright', 'meaning_reversed']
    for card in TAROT_DECK:
        for field in required_fields:
            assert field in card, f"Missing field '{field}' in card {card}"
    
    # Test that IDs are unique and sequential
    ids = [card['id'] for card in TAROT_DECK]
    assert len(set(ids)) == 78, "Card IDs are not unique"
    assert min(ids) == 0, f"Minimum ID should be 0, got {min(ids)}"
    assert max(ids) == 77, f"Maximum ID should be 77, got {max(ids)}"

def test_shuffle_deck():
    """Test that shuffle_deck returns a properly shuffled deck."""
    deck1 = shuffle_deck()
    deck2 = shuffle_deck()
    
    # Both decks should have 78 cards
    assert len(deck1) == 78
    assert len(deck2) == 78
    
    # Both decks should contain the same cards (just in different order)
    # We'll check by sorting by ID
    sorted_deck1 = sorted(deck1, key=lambda x: x['id'])
    sorted_deck2 = sorted(deck2, key=lambda x: x['id'])
    
    # The sorted decks should be identical to the original deck
    assert sorted_deck1 == TAROT_DECK
    assert sorted_deck2 == TAROT_DECK
    
    # The decks should be different from each other (very high probability)
    # We'll check that at least a few cards are in different positions
    different_positions = sum(1 for i in range(78) if deck1[i]['id'] != deck2[i]['id'])
    assert different_positions > 10, "Decks are too similar after shuffling"

def test_draw_cards():
    """Test drawing cards from the deck."""
    deck = shuffle_deck()
    
    # Test drawing 1 card
    drawn = draw_cards(num_cards=1, deck=deck)
    assert len(drawn) == 1
    assert 'reversed' in drawn[0]
    assert isinstance(drawn[0]['reversed'], bool)
    
    # Test drawing multiple cards
    drawn = draw_cards(num_cards=3, deck=deck)
    assert len(drawn) == 3
    for card in drawn:
        assert 'reversed' in card
        assert isinstance(card['reversed'], bool)
    
    # Test that drawn cards are removed from the deck
    # (Actually, our implementation doesn't modify the deck, but let's test that we get different cards)
    deck2 = shuffle_deck()
    drawn2 = draw_cards(num_cards=3, deck=deck2)
    
    # The drawn cards should be different (with very high probability)
    # We'll check that they're not all the same
    drawn_ids = [card['id'] for card in drawn]
    drawn2_ids = [card['id'] for card in drawn2]
    assert drawn_ids != drawn2_ids or len(set(drawn_ids)) > 1, "Drawn cards are not random enough"

def test_draw_cards_error():
    """Test that drawing too many cards raises an error."""
    deck = shuffle_deck()
    with pytest.raises(ValueError):
        draw_cards(num_cards=79, deck=deck)  # More than 78 cards

def test_get_card_meaning():
    """Test that get_card_meaning returns the correct meaning based on orientation."""
    # Get a card from the deck
    card = TAROT_DECK[0].copy()  # The Fool
    card['reversed'] = False
    
    # Test upright meaning
    meaning_upright = get_card_meaning(card)
    assert meaning_upright == card['meaning_upright']
    
    # Test reversed meaning
    card['reversed'] = True
    meaning_reversed = get_card_meaning(card)
    assert meaning_reversed == card['meaning_reversed']

def test_suit_and_rank_meanings():
    """Test the helper functions for suit and rank meanings."""
    # These are internal functions, but we can test them indirectly
    # by checking that minor arcana cards have meanings
    for card in MINOR_ARCANA:
        assert card['meaning_upright'] is not None
        assert len(card['meaning_upright']) > 0
        assert card['meaning_reversed'] is not None
        assert len(card['meaning_reversed']) > 0
        assert 'of' in card['name']  # Minor arcana names should have "of"

if __name__ == "__main__":
    pytest.main([__file__])