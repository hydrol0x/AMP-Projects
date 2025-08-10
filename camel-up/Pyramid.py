import random
from Camel import Color

class Pyramid:
    def __init__(self):
        self.dice = [Color.BLUE, Color.RED, Color.GREEN, Color.PURPLE, Color.YELLOW]
        
    def roll_dice(self) -> tuple[Color, int] | None:
        # Return None when there are no dice left
        number = random.randint(1,3)
        random.shuffle(self.dice)
        if len(self.dice) > 0:
            die = self.dice.pop()
            return die, number
        return None

    def reset_dice(self):
        self.dice= [Color.BLUE, Color.RED, Color.GREEN, Color.PURPLE, Color.YELLOW]

    def get_dice(self):
        return self.dice
