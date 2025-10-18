from __future__ import annotations

import random
from collections import deque
from typing import List, Iterator, Optional, Deque
from abc import ABC, abstractmethod

# Import from your card classes
from card import Card, CardColor, CardLabel, CardFactory


class IDeck(ABC):
    """
    Abstract interface for deck operations following Interface Segregation Principle.
    """
    
    @abstractmethod
    def shuffle(self) -> None:
        """Shuffle the deck in place"""
        pass
    
    @abstractmethod
    def draw(self, count: int = 1) -> List[Card]:
        """Draw specified number of cards from the top of the deck"""
        pass
    
    @abstractmethod
    def add_card(self, card: Card) -> None:
        """Add a single card to the deck"""
        pass
    
    @abstractmethod
    def add_cards(self, cards: List[Card]) -> None:
        """Add multiple cards to the deck"""
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        """Check if deck is empty"""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Get current number of cards in deck"""
        pass
    
    @abstractmethod
    def peek(self, count: int = 1) -> List[Card]:
        """Peek at top cards without removing them"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Remove all cards from the deck"""
        pass


class Deck(IDeck):
    """
    UNO Deck implementation using collections.deque for efficient operations.
    Follows standard 108-card UNO configuration.
    """
    
    # Class constants for deck composition
    _NUMBERS = list(range(10))
    _ACTIONS = [CardLabel.SKIP, CardLabel.REVERSE, CardLabel.DRAW_TWO]
    _WILDS = [CardLabel.WILD, CardLabel.WILD_DRAW_FOUR]
    _COLORS = [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]
    
    def __init__(self, initialize: bool = True) -> None:
        """
        Initialize a new UNO deck using deque for efficient pop/append operations.
        
        Args:
            initialize: If True, creates a standard 108-card UNO deck. 
                       If False, creates an empty deck.
        """
        self._cards: Deque[Card] = deque()
        
        if initialize:
            self._initialize_standard_deck()
    
    def _initialize_standard_deck(self) -> None:
        """Initialize the deck with standard UNO card distribution"""
        self._cards.clear()
        cards_to_add: List[Card] = []
        
        # Add number cards (one 0, two of each 1-9 per color)
        for color in self._COLORS:
            # One zero card per color
            cards_to_add.append(CardFactory.create_number_card(color, 0))
            
            # Two of each number 1-9 per color
            for number in range(1, 10):
                cards_to_add.append(CardFactory.create_number_card(color, number))
                cards_to_add.append(CardFactory.create_number_card(color, number))
        
        # Add action cards (two of each per color)
        for color in self._COLORS:
            for action in self._ACTIONS:
                cards_to_add.append(CardFactory.create_action_card(color, action))
                cards_to_add.append(CardFactory.create_action_card(color, action))
        
        # Add wild cards (four of each type)
        for wild_type in self._WILDS:
            for _ in range(4):
                cards_to_add.append(CardFactory.create_wild_card(wild_type))
        
        # Use extend for bulk addition (more efficient than multiple appends)
        self._cards.extend(cards_to_add)

    @staticmethod
    def basic_deck_store(self) -> Deck:
        pass
    
    def shuffle(self) -> None:
        """
        Shuffle the deck using random.shuffle on a temporary list.
        More efficient than shuffling deque directly.
        """
        cards_list = list(self._cards)
        random.shuffle(cards_list)
        self._cards = deque(cards_list)
    
    def draw(self, count: int = 1) -> List[Card]:
        """
        Draw specified number of cards from the top of the deck.
        Uses deque.popleft() for O(1) time complexity.
        
        Args:
            count: Number of cards to draw
            
        Returns:
            List of drawn cards
            
        Raises:
            ValueError: If count is negative or exceeds deck size
        """
        if count < 0:
            raise ValueError(f"Cannot draw negative number of cards: {count}")
        
        if count > len(self._cards):
            raise ValueError(f"Cannot draw {count} cards from deck with {len(self._cards)} cards")
        
        return [self._cards.popleft() for _ in range(count)]
    
    def draw_one(self) -> Optional[Card]:
        """
        Draw a single card from the top of the deck.
        O(1) time complexity using deque.popleft().
        
        Returns:
            Card if deck is not empty, None otherwise
        """
        if self.is_empty():
            return None
        
        return self._cards.popleft()
    
    def add_card(self, card: Card) -> None:
        """
        Add a single card to the bottom of the deck.
        O(1) time complexity using deque.append().
        
        Args:
            card: Card to add
        """
        self._cards.append(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        """
        Add multiple cards to the bottom of the deck.
        O(k) time complexity where k is number of cards.
        
        Args:
            cards: List of cards to add
        """
        self._cards.extend(cards)
    
    def add_to_top(self, card: Card) -> None:
        """
        Add a card to the top of the deck (will be drawn next).
        O(1) time complexity using deque.appendleft().
        
        Args:
            card: Card to add to top
        """
        self._cards.appendleft(card)
    
    def add_cards_to_top(self, cards: List[Card]) -> None:
        """
        Add multiple cards to the top of the deck.
        Cards will be drawn in reverse order of the input list.
        
        Args:
            cards: List of cards to add to top
        """
        for card in reversed(cards):
            self._cards.appendleft(card)
    
    def is_empty(self) -> bool:
        """
        Check if deck is empty.
        O(1) time complexity.
        
        Returns:
            True if deck has no cards, False otherwise
        """
        return len(self._cards) == 0
    
    def size(self) -> int:
        """
        Get current number of cards in deck.
        O(1) time complexity.
        
        Returns:
            Number of cards in deck
        """
        return len(self._cards)
    
    def peek(self, count: int = 1) -> List[Card]:
        """
        Peek at top cards without removing them.
        Uses slicing on deque for O(k) time complexity.
        
        Args:
            count: Number of cards to peek at
            
        Returns:
            List of top cards
            
        Raises:
            ValueError: If count is negative or exceeds deck size
        """
        if count < 0:
            raise ValueError(f"Cannot peek negative number of cards: {count}")
        
        if count > len(self._cards):
            raise ValueError(f"Cannot peek at {count} cards from deck with {len(self._cards)} cards")
        
        # Convert to list slice for the first 'count' elements
        return list(self._cards)[:count]
    
    def clear(self) -> None:
        """Remove all cards from the deck. O(1) time complexity."""
        self._cards.clear()
    
    def rotate(self, positions: int) -> None:
        """
        Rotate the deck by specified number of positions.
        Positive values rotate right, negative values rotate left.
        O(k) time complexity where k is abs(positions).
        
        Args:
            positions: Number of positions to rotate
        """
        self._cards.rotate(positions)
    
    def __len__(self) -> int:
        """Support for len(deck). O(1) time complexity."""
        return len(self._cards)
    
    def __bool__(self) -> bool:
        """Support for truth value testing. O(1) time complexity."""
        return not self.is_empty()
    
    def __iter__(self) -> Iterator[Card]:
        """Support for iteration over the deck."""
        return iter(self._cards)
    
    def __contains__(self, card: Card) -> bool:
        """Support for 'in' operator. O(n) time complexity."""
        return card in self._cards
    
    def __str__(self) -> str:
        return f"UNO Deck with {self.size()} cards"
    
    def __repr__(self) -> str:
        return f"Deck(cards={self.size()})"
    
    def get_card_distribution(self) -> dict:
        """
        Get distribution of cards in the deck by type.
        
        Returns:
            Dictionary with card type counts
        """
        distribution = {
            'total': self.size(),
            'number_cards': 0,
            'action_cards': 0,
            'wild_cards': 0,
            'by_color': {color.name: 0 for color in CardColor},
            'by_label': {label.name: 0 for label in CardLabel}
        }
        
        for card in self._cards:
            distribution['by_color'][card.color.name] += 1
            distribution['by_label'][card.label.name] += 1
            
            if card.is_number_card:
                distribution['number_cards'] += 1
            elif card.is_action_card:
                distribution['action_cards'] += 1
            elif card.is_wild:
                distribution['wild_cards'] += 1
        
        return distribution


class DeckBuilder:
    """
    Builder pattern implementation for creating customized UNO decks.
    Provides fluent interface for deck configuration.
    """
    
    def __init__(self) -> None:
        self._include_standard_cards = True
        self._custom_cards: List[Card] = []
    
    def exclude_standard_cards(self) -> DeckBuilder:
        """Exclude standard UNO cards from the deck"""
        self._include_standard_cards = False
        return self
    
    def add_custom_card(self, card: Card) -> DeckBuilder:
        """Add a custom card to the deck"""
        self._custom_cards.append(card)
        return self
    
    def add_custom_cards(self, cards: List[Card]) -> DeckBuilder:
        """Add multiple custom cards to the deck"""
        self._custom_cards.extend(cards)
        return self
    
    def build(self) -> Deck:
        """Build the customized deck"""
        deck = Deck(initialize=self._include_standard_cards)
        
        if self._custom_cards:
            deck.add_cards(self._custom_cards)
        
        return deck


# Utility functions for deck operations
def create_standard_deck(shuffled: bool = True) -> Deck:
    """
    Factory function to create a standard shuffled UNO deck.
    
    Args:
        shuffled: Whether to shuffle the deck after creation
        
    Returns:
        New Deck instance
    """
    deck = Deck(initialize=True)
    if shuffled:
        deck.shuffle()
    return deck


def create_empty_deck() -> Deck:
    """
    Create an empty deck.
    
    Returns:
        Empty Deck instance
    """
    return Deck(initialize=False)


def merge_decks(deck1: Deck, deck2: Deck) -> Deck:
    """
    Merge two decks into a new deck.
    
    Args:
        deck1: First deck
        deck2: Second deck
        
    Returns:
        New deck containing all cards from both decks
    """
    new_deck = create_empty_deck()
    new_deck.add_cards(list(deck1))
    new_deck.add_cards(list(deck2))
    return new_deck


def create_discard_pile(initial_card: Optional[Card] = None) -> Deck:
    """
    Create a discard pile (specialized deck for discard operations).
    
    Args:
        initial_card: Optional starting card for the discard pile
        
    Returns:
        Deck configured as a discard pile
    """
    discard_pile = create_empty_deck()
    if initial_card:
        discard_pile.add_card(initial_card)
    return discard_pile