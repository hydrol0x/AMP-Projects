import unittest
import sys
import os
import random
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
from Player import Player

class Test_Player(unittest.TestCase):

	def test_no_money(self):
		player = Player('A')
		self.assertEqual(player.get_money(), 2)

	def test_add_money(self):
		player = Player('A')
		current_money = player.get_money()
		money_to_be_added = 3
		current_money += money_to_be_added
		player.add_money(money_to_be_added)
		self.assertEqual(player.get_money(), current_money,)
		
if __name__ == '__main__':
    unittest.main()	