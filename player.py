from classes import *
import game

class Player:
    def __init__(self, name: str, stack: int = 200):
        self.name: str = name
        self.stack: int = stack

        # Round variables
        self.hand: list[Card] = []
        self.is_active: bool = True
        self.is_all_in: bool = False

    def __repr__(self):
        return f'{self.name} with stack {self.stack}'

    def __eq__(self, other: "Player"):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def add_cards(self, cards: list[Card]):
        self.hand.extend(cards)
    
    def retrieve_cards(self):
        return self.hand

    def get_hand_count(self):
        return len(self.hand)
    
    def clear_hand(self):
        self.hand.clear()

    def remove_amount(self, amount: int):
        if amount > self.stack:
            raise ValueError("Not enough chips")
        self.stack -= amount
        
    def add_amount(self, amount: int):
        self.stack += amount

    def play_turn(self, game_state: game.Game_State) -> tuple[game.Move, int]:
        raise NotImplementedError("Player must implement play_turn method")
