import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
from Pyramid import Pyramid
from Camel import Color

class Pyramid_Test(unittest.TestCase):
    all_dices = [Color.BLUE, Color.RED, Color.GREEN, Color.PURPLE, Color.YELLOW]

    def test_random_roll_1(self):
        """Tests that roll_dice() randomly generates numbers 1-3"""
        helper = Pyramid()
        count_dict = {'1': 0, '2': 0, '3': 0}
        for i in range(0,30000):
            if not helper.dice:
                helper.reset_dice()
            color, number = helper.roll_dice()
            count_dict[str(number)]+=1
        actual = True
        expected = True
        for item in count_dict.values():
            if not 8500 < item < 11500:
                actual = False
        self.assertEqual(actual, expected, "roll_dice() expected to generate approximately the same number of 1s, 2s, and 3s.")

    def test_reset_dice(self):
        helper = Pyramid()
        for i in range(6):
            for j in range(i):
                helper.roll_dice()
                helper.reset_dice()
            self.assertEqual(helper.get_dice(), self.all_dices)

if __name__ == '__main__':
    unittest.main()