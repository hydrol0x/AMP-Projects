from typing import override
# from BettingCards import BettingCards
# from Pyramid import Pyramid
from Camel import Color

bets = dict[Color, list[int]]

class Player:
    def __init__(self, name: str):
        # OLD
#         self.money: int = 2
#         self.name: str = name
#         self.spectator_card_played: bool = False
#         self.spectator_card_position: int | None = None
#         self.spectator_card_value: int | None = None
        # ======
        self.money: int = 3
        self.current_bets: bets = {color: [] for color in Color} # keeps track of for which color which value the betting card has for 1st place, which determines the other values
        self.name = name
        self.spectator_card_played: bool= False
        self.spectator_card_position: int | None= None
        self.spectator_card_value: bool | None = None
        self.finish_cards: list[Color] = [Color.BLUE, Color.RED, Color.GREEN, Color.PURPLE, Color.YELLOW]
        self.overall_winner = list()
        self.overall_loser = list()

    def set_overall_winner(self, winner_color: Color):
        self.finish_cards.remove(winner_color)
        self.overall_winner.append(winner_color)

    def set_overall_loser(self, loser_color: Color):
        self.finish_cards.remove(loser_color)
        self.overall_loser.append(loser_color)

    def get_availible_finish_cards(self):
        return self.finish_cards

    def get_name(self):
        return self.name

    def add_bets(self, color: Color, value: int):
        self.current_bets[color].append(value)

    def get_current_bets(self) -> bets:
        return self.current_bets

    def add_money(self, amount: int) -> None:
        self.money += amount

    def get_money(self) -> int:
        return self.money

    def add_spectator_card(self, position: int, value: int) -> None:
        self.spectator_card_position = position
        self.spectator_card_value = value

    def get_spectator_card_position(self) -> int | None:
        return self.spectator_card_position

    def get_spectator_card_value(self) -> int | None:
        return self.spectator_card_value

    @override
    def __repr__(self) -> str:
        return f"{self.name}"
