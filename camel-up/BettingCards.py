from Camel import Color

class BettingCards:
    def __init__(self):
        self.bets = {Color.RED: [2, 2, 3, 5], Color.YELLOW: [2, 2, 3, 5], Color.GREEN: [2, 2, 3, 5], Color.PURPLE: [2, 2, 3, 5], Color.BLUE: [2, 2, 3, 5]}

    def remove(self, color: Color):
        if not self.is_empty(self.bets[color]):
            bet_value = self.bets[color].pop()
            # print(bet_value)
            return (color, bet_value)
        return None

    def is_empty(self, list):
        if not list:
            return True
        else:
            return False

    def reset_cards(self):
        self.bets = {Color.RED: [2, 2, 3, 5], Color.YELLOW: [2, 2, 3, 5], Color.GREEN: [2, 2, 3, 5], Color.PURPLE: [2, 2, 3, 5], Color.BLUE: [2, 2, 3, 5]}

    def return_bets(self):
        return self.bets
