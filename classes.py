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

class Hand_Rank(Enum):
    High_Card = 1
    Pair = 2
    Two_Pair = 3
    Three_of_a_Kind = 4
    Straight = 5
    Flush = 6
    Full_House = 7
    Four_of_a_Kind = 8
    Straight_Flush = 9
    Royal_Flush = 10

class Hand:
    def __init__(self, pocket_cards: list[Card], community_cards: list[Card]):
        self.pocket_cards: list[Card] = pocket_cards
        self.community_cards: list[Card] = community_cards
        self.rank: Hand_Rank = self.get_rank()

    def __repr__(self):
        return self.rank.name

    def __eq__(self, other: "Hand"):
        return self.rank == other.rank
    
    def __hash__(self) -> int:
        return hash(self.rank)
    
    def __lt__(self, other: "Hand"):
        return self.rank.value < other.rank.value
    
    def get_rank(self):
        all_cards = self.pocket_cards + self.community_cards
        all_cards.sort(reverse=True)  # Sort the cards in descending order by rank
        
        # Check for a royal flush
        if all_cards[0].rank == 14 and all_cards[1].rank == 13 and all_cards[2].rank == 12 and all_cards[3].rank == 11 and all_cards[4].rank == 10 and all_cards[0].suit == all_cards[1].suit == all_cards[2].suit == all_cards[3].suit == all_cards[4].suit:
            return Hand_Rank.Royal_Flush
        
        # Check for a straight flush
        for i in range(len(all_cards) - 4):
            if all_cards[i].rank == all_cards[i+1].rank + 1 and all_cards[i].rank == all_cards[i+2].rank + 2 and all_cards[i].rank == all_cards[i+3].rank + 3 and all_cards[i].rank == all_cards[i+4].rank + 4 and all_cards[i].suit == all_cards[i+1].suit == all_cards[i+2].suit == all_cards[i+3].suit == all_cards[i+4].suit:
                return Hand_Rank.Straight_Flush
        
        # Check for four of a kind
        for i in range(len(all_cards) - 3):
            if all_cards[i].rank == all_cards[i+1].rank == all_cards[i+2].rank == all_cards[i+3].rank:
                return Hand_Rank.Four_of_a_Kind
        
        # Check for a full house
        for i in range(len(all_cards) - 2):
            if all_cards[i].rank == all_cards[i+1].rank == all_cards[i+2].rank:
                for j in range(len(all_cards) - 1):
                    if j != i and j != i+1 and j != i+2 and all_cards[j].rank == all_cards[j+1].rank:
                        return Hand_Rank.Full_House
        
        # Check for a flush
        for i in range(len(all_cards) - 4):
            if all_cards[i].suit == all_cards[i+1].suit == all_cards[i+2].suit == all_cards[i+3].suit == all_cards[i+4].suit:
                return Hand_Rank.Flush
        
        # Check for a straight
        for i in range(len(all_cards) - 4):
            if all_cards[i].rank == all_cards[i+1].rank + 1 and all_cards[i].rank == all_cards[i+2].rank + 2 and all_cards[i].rank == all_cards[i+3].rank + 3 and all_cards[i].rank == all_cards[i+4].rank + 4:
                return Hand_Rank.Straight
        
        # Check for three of a kind
        for i in range(len(all_cards) - 2):
            if all_cards[i].rank == all_cards[i+1].rank == all_cards[i+2].rank:
                return Hand_Rank.Three_of_a_Kind
        
        # Check for two pair
        for i in range(len(all_cards) - 3):
            if all_cards[i].rank == all_cards[i+1].rank and all_cards[i+2].rank == all_cards[i+3].rank:
                return Hand_Rank.Two_Pair
        
        # Check for a pair
        for i in range(len(all_cards) - 1):
            if all_cards[i].rank == all_cards[i+1].rank:
                return Hand_Rank.Pair
        
        # If no other hand rank is found, return high card
        return Hand_Rank.High_Card
    