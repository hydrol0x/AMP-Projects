from enum import Enum, auto
from typing import override, Self


class Color(Enum):
    RED = (auto(), "red")
    BLUE = (auto(), "blue")
    YELLOW = (auto(), "yellow")
    PURPLE = (auto(), "purple")
    GREEN = (auto(), "green")

    @override
    def __repr__(self) -> str:
        return self._name_[0]

    @override
    def __str__(self) -> str:
        return self._name_[0]


class IllegalNumberMoves(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class Camel:
    def __init__(self, color: Color):
        self.color_dictionary = {"R": "🔴", "Y": "🟡", "P": "🟣", "G": "🟢", "B": "🔵"}
        self.color: Color = color
        self.position: int = 0
        self.stacked_on_me: Camel | None = (
            None  # Keeps track of which camel, if any, is immediately above this camel
        )

    def move_camel(self, moves: int):
        if abs(moves) > 3 or moves == 0:
            raise IllegalNumberMoves(f"Illegal number of moves {moves}. The camel can only move 1-3 spaces forward or backward.")
        self.position += moves
        if self.stacked_on_me:
            self.stacked_on_me.move_camel(moves)

    def set_stacked_on_me(self, camel_top: Self | None):
        self.stacked_on_me = camel_top

    def add_position(self, number: int):
        self.position += number

    def get_position(self):
        return self.position

    def get_color(self):
        return self.color

    def get_stacked_on_me(self):
        return self.stacked_on_me

    @override
    def __str__(self):
        return (str((self.color, self.position)) + "->" + (str(self.stacked_on_me.color) if self.stacked_on_me else str(None)))

    @override
    def __repr__(self) -> str:
        return (str((self.color, self.position)) + "->" + (str(self.stacked_on_me.color) if self.stacked_on_me else str(None)))
