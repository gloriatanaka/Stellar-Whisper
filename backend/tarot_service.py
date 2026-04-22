"""
Tarot card service for Stellar Whisper.
Defines the tarot deck and functions for drawing cards.
"""

import random
from typing import List, Dict, Optional

# Tarot card data structure
# We'll define the 78 cards: 22 Major Arcana and 56 Minor Arcana (4 suits of 14 cards each)
# Each card has: id, name, arcana (major/minor), suit (for minor), number, meaning_upright, meaning_reversed
# For simplicity, we'll use generic meanings. In a real app, these would be more detailed.

MAJOR_ARCANA = [
    {"id": 0, "name": "The Fool", "arcana": "major", "number": 0, 
     "meaning_upright": "New beginnings, adventure, innocence, spontaneity, free spirit",
     "meaning_reversed": "Holding back, recklessness, risk taking"},
    {"id": 1, "name": "The Magician", "arcana": "major", "number": 1,
     "meaning_upright": "Manifestation, resourcefulness, power, inspired action",
     "meaning_reversed": "Manipulation, poor planning, untapped talents"},
    {"id": 2, "name": "The High Priestess", "arcana": "major", "number": 2,
     "meaning_upright": "Intuition, sacred knowledge, divine feminine, mystery",
     "meaning_reversed": "Secrets, withdrawal, lack of balance"},
    {"id": 3, "name": "The Empress", "arcana": "major", "number": 3,
     "meaning_upright": "Femininity, beauty, nature, nurturing, abundance",
     "meaning_reversed": "Creative block, dependence on others"},
    {"id": 4, "name": "The Emperor", "arcana": "major", "number": 4,
     "meaning_upright": "Authority, establishment, structure, father figure",
     "meaning_reversed": "Domination, excessive control, rigidity"},
    {"id": 5, "name": "The Hierophant", "arcana": "major", "number": 5,
     "meaning_upright": "Spiritual wisdom, religious beliefs, conformity, traditions",
     "meaning_reversed": "Personal beliefs, freedom, challenging the status quo"},
    {"id": 6, "name": "The Lovers", "arcana": "major", "number": 6,
     "meaning_upright": "Love, harmony, relationships, values alignment, choices",
     "meaning_reversed": "Self-love, imbalance, disagreements, misaligned values"},
    {"id": 7, "name": "The Chariot", "arcana": "major", "number": 7,
     "meaning_upright": "Control, victory, willpower, determination, action",
     "meaning_reversed": "Lack of control, aggression, impulsive"},
    {"id": 8, "name": "Strength", "arcana": "major", "number": 8,
     "meaning_upright": "Strength, courage, compassion, influence, persuasion",
     "meaning_reversed": "Inner strength, self-doubt, low energy, raw emotions"},
    {"id": 9, "name": "The Hermit", "arcana": "major", "number": 9,
     "meaning_upright": "Introspection, inner guidance, soul-searching, wisdom",
     "meaning_reversed": "Isolation, loneliness, withdrawal"},
    {"id": 10, "name": "Wheel of Fortune", "arcana": "major", "number": 10,
     "meaning_upright": "Good fortune, karma, life cycles, destiny, turning point",
     "meaning_reversed": "Bad luck, resisting change, breaking cycles"},
    {"id": 11, "name": "Justice", "arcana": "major", "number": 11,
     "meaning_upright": "Justice, fairness, truth, cause and effect, law",
     "meaning_reversed": "Unfairness, lack of accountability, dishonesty"},
    {"id": 12, "name": "The Hanged Man", "arcana": "major", "number": 12,
     "meaning_upright": "Pause, surrender, letting go, new perspective",
     "meaning_reversed": "Stalling, selfishness, delay, resistance"},
    {"id": 13, "name": "Death", "arcana": "major", "number": 13,
     "meaning_upright": "Endings, change, transformation, transition",
     "meaning_reversed": "Resistance to change, personal transformation"},
    {"id": 14, "name": "Temperance", "arcana": "major", "number": 14,
     "meaning_upright": "Balance, moderation, patience, purpose, healing",
     "meaning_reversed": "Imbalance, excess, self-healing, re-alignment"},
    {"id": 15, "name": "The Devil", "arcana": "major", "number": 15,
     "meaning_upright": "Shadow self, attachment, addiction, restriction, sexuality",
     "meaning_reversed": "Breaking free, detachment, rediscovering desires"},
    {"id": 16, "name": "The Tower", "arcana": "major", "number": 16,
     "meaning_upright": "Sudden change, upheaval, chaos, revelation, awakening",
     "meaning_reversed": "Fear of change, personal transformation, avoiding disaster"},
    {"id": 17, "name": "The Star", "arcana": "major", "number": 17,
     "meaning_upright": "Hope, faith, purpose, renewal, spirituality",
     "meaning_reversed": "Despair, lack of faith, disconnection"},
    {"id": 18, "name": "The Moon", "arcana": "major", "number": 18,
     "meaning_upright": "Illusion, fear, anxiety, subconscious, intuition",
     "meaning_reversed": "Release of fear, confusion, misunderstanding"},
    {"id": 19, "name": "The Sun", "arcana": "major", "number": 19,
     "meaning_upright": "Positivity, fun, warmth, success, vitality",
     "meaning_reversed": "Inner child, feeling joyless, overly optimistic"},
    {"id": 20, "name": "Judgement", "arcana": "major", "number": 20,
     "meaning_upright": "Judgement, rebirth, inner calling, absolution",
     "meaning_reversed": "Self-doubt, inner critic, ignoring the call"},
    {"id": 21, "name": "The World", "arcana": "major", "number": 21,
     "meaning_upright": "Completion, accomplishment, travel, integration",
     "meaning_reversed": "Shortcuts, delays, incomplete"}
]

SUITS = ["wands", "cups", "swords", "pentacles"]
# Minor Arcana: Ace to 10, then Page, Knight, Queen, King
MINOR_RANKS = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "page", "knight", "queen", "king"]

def get_suit_meaning(suit: str) -> str:
    """Get the general meaning of a suit."""
    meanings = {
        "wands": "creativity, action, and passion",
        "cups": "emotions, relationships, and intuition",
        "swords": "thoughts, communication, and conflict",
        "pentacles": "material aspects, work, and finances"
    }
    return meanings.get(suit, "unknown")

def get_rank_meaning(rank: str) -> str:
    """Get the general meaning of a rank."""
    meanings = {
        "ace": "new beginnings and potential",
        "2": "balance and partnership",
        "3": "growth and collaboration",
        "4": "stability and foundation",
        "5": "change and challenge",
        "6": "harmony and adjustment",
        "7": "reflection and assessment",
        "8": "movement and transition",
        "9": "attainment and completion",
        "10": "fulfillment and burden",
        "page": "exploration and message",
        "knight": "action and journey",
        "queen": "nurturing and maturity",
        "king": "mastery and authority"
    }
    return meanings.get(rank, "unknown")

MINOR_ARCANA = []
card_id = 22  # Start after Major Arcana
for suit in SUITS:
    for rank in MINOR_RANKS:
        name = f"{rank} of {suit}"
        # For simplicity, we'll generate meanings based on suit and rank
        # In a real app, these would be more nuanced
        meaning_upright = f"The {rank} of {suit} represents {get_suit_meaning(suit)} in the context of {get_rank_meaning(rank)}"
        meaning_reversed = f"The reversed {rank} of {suit} indicates a blockage or internalization of {get_suit_meaning(suit)}"
        MINOR_ARCANA.append({
            "id": card_id,
            "name": name,
            "arcana": "minor",
            "suit": suit,
            "rank": rank,
            "meaning_upright": meaning_upright,
            "meaning_reversed": meaning_reversed
        })
        card_id += 1

# Combine all cards
TAROT_DECK = MAJOR_ARCANA + MINOR_ARCANA

def shuffle_deck() -> List[Dict]:
    """
    Returns a shuffled copy of the tarot deck.
    """
    deck_copy = TAROT_DECK.copy()
    random.shuffle(deck_copy)
    return deck_copy

def draw_cards(num_cards: int = 1, deck: Optional[List[Dict]] = None) -> List[Dict]:
    """
    Draw a specified number of cards from the deck.
    
    Args:
        num_cards: Number of cards to draw (default 1)
        deck: Optional pre-shuffled deck. If not provided, a new shuffled deck is used.
    
    Returns:
        List of drawn card dictionaries (with an additional 'reversed' boolean indicating orientation)
    """
    if deck is None:
        deck = shuffle_deck()
    
    if num_cards > len(deck):
        raise ValueError(f"Cannot draw {num_cards} cards from a deck of {len(deck)}")
    
    drawn = []
    for i in range(num_cards):
        card = deck[i].copy()
        # Randomly determine if the card is reversed (for simplicity, 50% chance)
        card['reversed'] = random.choice([True, False])
        drawn.append(card)
    
    return drawn

def get_card_meaning(card: Dict) -> str:
    """
    Get the meaning of a card based on its orientation.
    
    Args:
        card: A card dictionary (must have 'meaning_upright', 'meaning_reversed', and 'reversed' keys)
    
    Returns:
        The meaning string (upright or reversed)
    """
    if card.get('reversed', False):
        return card.get('meaning_reversed', 'No reversed meaning available')
    else:
        return card.get('meaning_upright', 'No upright meaning available')

if __name__ == "__main__":
    # Simple test
    deck = shuffle_deck()
    print(f"Deck size: {len(deck)}")
    drawn = draw_cards(3, deck)
    print("Drawn cards:")
    for card in drawn:
        orientation = "reversed" if card['reversed'] else "upright"
        print(f"- {card['name']} ({orientation}): {get_card_meaning(card)}")
