from enum import Enum, auto
from typing import Self


class Hand:
    def __init__(self):
        self.alive: bool = True
        self.value: int = 1

class Player:
    def __init__(self):
        self.left:Hand = Hand()
        self.right: Hand = Hand()

    def tap(self, frum: Hand, amount: int, to: Hand) -> None:
        frum.value -= amount
        to.value += amount

        if frum.value <= 0:
            frum.value = 0
            frum.alive = False
        if to.value <= 0:
            to.value = 0
            to.alive = False

        if frum.value > 0 and not frum.alive:
            frum.alive = True
        if to.value > 0 and not to.alive:
            to.alive = True

    def split(self, left_to_right: bool, amount: int) -> None:
        if left_to_right:
            self.tap(self.left, amount, self.right)
        else:
            self.tap(self.right, amount, self.left)
