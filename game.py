from classes import *
from enum import Enum
from player import *

class Move(Enum):
    FOLD = 0
    CHECK = 1
    CALL = 2
    RAISE = 3
    ALL_IN = 4

class Action:
    def __init__(self, player: Player, move: Move, amount: int = 0):
        self.player = player
        self.move = move
        self.amount = amount

class Game:
    def __init__(self, players: list[Player], small_blind: int = 10, total_rounds: int = 20):
        self.players: list[Player] = players
        self.num_players: int = len(players)
        self.curr_player_index: int = 0
        self.starting_player_index: int = 0

        self.small_blind: int = small_blind
        self.big_blind: int = self.small_blind * 2
        self.pot: int = 0
        self.curr_bet: int = 0

        self.deck: Deck = Deck().shuffle()
        self.community_cards: list[Card] = []
        self.action_history: list[Action] = []

        self.total_rounds: int = total_rounds
        self.curr_round: int = 0

    def clear_pot(self):
        self.pot = 0
    
    def deal_pocket_cards(self):
        for player in self.players:
            player.add_cards(self.deck.draw_cards(2))
    
    def start_new_round(self):
        self.clear_pot()
        self.deck = Deck().shuffle()
        self.curr_player_index = self.starting_player_index
        self.action_history.clear()

        for player in self.players:
            player.clear_hand()
            player.is_active = True

    def get_blinds(self):
        players_with_not_enough_chips: list[Player] = []

        small_blind_player = self.players[self.starting_player_index]
        try:
            small_blind_player.remove_amount(self.small_blind)
            self.pot += self.small_blind
        except ValueError:
            self.pot += small_blind_player.stack
            small_blind_player.remove_amount(small_blind_player.stack)
            players_with_not_enough_chips.append(small_blind_player)
        
        big_blind_player = self.players[(self.starting_player_index + 1) % self.num_players]
        try:
            big_blind_player.remove_amount(self.big_blind)
            self.pot += self.big_blind
        except ValueError:
            self.pot += big_blind_player.stack
            big_blind_player.remove_amount(big_blind_player.stack)
            players_with_not_enough_chips.append(big_blind_player)
        
        return players_with_not_enough_chips
    
    def get_moves(self):
        betting_started = False
        self.curr_bet = 0

        for player_index in range(self.curr_player_index, self.num_players):
            player = self.players[player_index]

            if not player.is_active:
                continue

            move, amount = player.play_turn(Game_State(self.pot, self.curr_bet, self.community_cards, self.action_history))
            self.parse_move(betting_started, player, move, amount)
            self.curr_player_index = (self.curr_player_index + 1) % self.num_players

        for player_index in range(0, self.curr_player_index):
            player = self.players[player_index]

            if not player.is_active:
                continue

            move, amount = player.play_turn(Game_State(self.pot, self.curr_bet, self.community_cards, self.action_history))
            self.parse_move(betting_started, player, move, amount)
            self.curr_player_index = (self.curr_player_index + 1) % self.num_players
    
    def parse_move(self, betting_started: bool, player: Player, move: Move, amount: int = 0):
        if player.is_all_in:
                if move != Move.FOLD or move != Move.CALL:
                    raise Exception("Player is all in but did not fold or call")

        if move == Move.FOLD:
            player.is_active = False
            self.action_history.append(Action(player, move))
        elif move == Move.CHECK:
            if betting_started:
                raise Exception("Cannot check when betting has started")
            self.action_history.append(Action(player, move))
        elif move == Move.CALL:
            if betting_started:
                try:
                    player.remove_amount(self.curr_bet)
                    self.pot += self.curr_bet
                    self.action_history.append(Action(player, move, self.curr_bet))
                except ValueError:
                    player.remove_amount(player.stack)
                    self.pot += player.stack
                    player.is_all_in = True
                    self.action_history.append(Action(player, Move.ALL_IN, player.stack))
            else:
                self.action_history.append(Action(player, Move.CHECK))
        elif move == Move.RAISE:
            if amount <= self.curr_bet:
                raise Exception("Cannot raise less than the current bet")
            
            if not betting_started:
                betting_started = True
            try:
                player.remove_amount(amount)
                self.pot += amount
                self.curr_bet = amount
                self.action_history.append(Action(player, move, amount))
            except ValueError:
                self.pot += player.stack
                player.remove_amount(player.stack)
                player.is_all_in = True
                self.action_history.append(Action(player, Move.ALL_IN, player.stack))
        elif move == Move.ALL_IN:
            if player.is_all_in:
                raise Exception("Player is already all in")
            player.is_all_in = True
            self.pot += player.stack
            player.remove_amount(player.stack)
            self.action_history.append(Action(player, move, player.stack))
        else:
            raise Exception("Invalid move")
        
    def check_win(self):
        active_players = [player for player in self.players if player.is_active]
        if len(active_players) == 1:
            return active_players[0]
        return None
    
    def showdown(self):
        best_hand_player = [player for player in self.players if player.is_active][0]
        best_hand = Hand(best_hand_player.hand, self.community_cards)
        for player in self.players:
            if not player.is_active:
                continue
            player_hand = Hand(player.hand, self.community_cards)
            if player_hand.rank > best_hand.rank:
                best_hand_player = player
                best_hand = player_hand
        
        return best_hand_player

    def play(self):
        if (self.num_players < 2):
            raise Exception('Not enough players to start game')
        
        while (True):
            self.curr_round += 1

            if self.curr_round > self.total_rounds:
                print("All rounds completed")
                break
        
            # Start game
            self.start_new_round()
            self.deal_pocket_cards()

            # Blinds
            compulsory_all_in_players = self.get_blinds()
            for player in compulsory_all_in_players:
                player.is_all_in = True
                self.pot += player.stack
                player.remove_amount(player.stack)
                self.action_history.append(Action(player, Move.ALL_IN, player.stack))

            # Betting round
            self.get_moves()

            # Deal flop
            self.community_cards = self.deck.draw_cards(3)

            # Betting round
            self.get_moves()
            self.check_win()

            # Deal turn
            self.community_cards.append(self.deck.draw_cards(1)[0])

            # Betting round
            self.get_moves()
            self.check_win()

            # Deal river
            self.community_cards.append(self.deck.draw_cards(1)[0])

            # Betting round
            self.get_moves()
            self.check_win()

            self.showdown()

            # Game ends
            self.starting_player_index = (self.starting_player_index + 1) % self.num_players

class Game_State:
    def __init__(self, pot: int, curr_bet: int, community_cards: list[Card], action_history: list[Action]):
        self.pot: int = pot
        self.curr_bet: int = curr_bet
        self.community_cards: list[Card] = community_cards
        self.action_history: list[Action] = action_history
