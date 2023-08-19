from enum import Enum
import random

class Suit(Enum):
    Clubs = 1
    Diamonds = 2
    Hearts = 3
    Spades = 4

suit_symbols = {
        Suit.Clubs: '♣',
        Suit.Diamonds: '♦',
        Suit.Hearts: '♥',
        Suit.Spades: '♠'
    }


class Rank(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 1

class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank: Rank = rank
        self.suit: Suit = suit

    def __setattr__(self, attr, value) :
        if hasattr(self, attr):
            raise AttributeError("Cannot change card attributes.")
        self.__dict__[attr] = value

    def __repr__(self):
        return f'{self.rank.value}{suit_symbols[self.suit]} {self.rank.name} of {self.suit.name}'

    def __eq__(self, other: "Card"):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other: "Card"):
        return self.rank.value < other.rank.value

    def __hash__(self):
        return hash((self.rank, self.suit))

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Suit for rank in Rank]
    
    def draw_cards(self, n: int):
        return [self.cards.pop() for _ in range(n)]
    
    def add_cards(self, cards: list[Card]):
        for card in cards:
            if card in self.cards:
                raise ValueError("Cannot add duplicate cards.")
        self.cards.extend(cards)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def get_num(self):
        return len(self.cards)
