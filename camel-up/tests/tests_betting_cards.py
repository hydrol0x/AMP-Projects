import unittest
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from BettingCards import BettingCards
from Camel import Color


class TestBettingCards(unittest.TestCase):
	bets_none_removed = [2, 2, 3, 5]
	bets_one_removed = [2, 2, 3]
	bets_two_removed = [2, 2]
	bets_three_removed = [2]
	bets_all_removed = []

	first_card = 5
	second_card = 3
	third_card = 2
	fourth_card = 2

	full_bets = {Color.RED: [2, 2, 3, 5], Color.YELLOW: [2, 2, 3, 5], Color.GREEN: [2, 2, 3, 5], Color.PURPLE: [2, 2, 3, 5], Color.BLUE: [2, 2, 3, 5]}
	empty_bets = {Color.RED: [], Color.YELLOW: [], Color.GREEN: [], Color.PURPLE: [], Color.BLUE: []}

	def test_remove_red(self):
		"""Tests that remove() removes the correct color card and value from the betting stack: a single card"""
		Bets = BettingCards()
		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.first_card))
		self.assertEqual(Bets.bets[Color.RED], self.bets_one_removed)

	def test_remove_two(self):
		"""Tests that remove() removes the correct color card and value from the betting stack: two cards of the same color"""
		Bets = BettingCards()
		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.first_card))
		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.second_card))
		self.assertEqual(Bets.bets[Color.RED], self.bets_two_removed)


	def test_remove_four(self):
		"""Tests that remove() removes the correct color card and value from the betting stack: four cards of the same color"""
		Bets = BettingCards()
		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.first_card))
		self.assertEqual(Bets.bets[Color.RED], self.bets_one_removed)

		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.second_card))
		self.assertEqual(Bets.bets[Color.RED], self.bets_two_removed)


		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.third_card))
		self.assertEqual(Bets.bets[Color.RED], self.bets_three_removed)

		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.fourth_card))
		self.assertEqual(Bets.bets[Color.RED], self.bets_all_removed)


	def test_remove_three(self):
		"""Tests that remove() removes the correct color card and value from the betting stack: three cards of the same color"""
		Bets = BettingCards()
		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.first_card))
		self.assertEqual(Bets.bets[Color.RED], self.bets_one_removed)


		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.second_card))
		self.assertEqual(Bets.bets[Color.RED], self.bets_two_removed)


		items = Bets.remove(Color.RED)
		self.assertEqual(items, (Color.RED, self.third_card))
		self.assertEqual(Bets.bets[Color.RED], self.bets_three_removed)


	def test_remove_everything(self):
		"""Tests that remove() removes the correct color card and value from the betting stack: every single card"""
		Bets = BettingCards()

		bet_lists = Bets.return_bets().keys()
		keys = [i for i in bet_lists]
		Bets = BettingCards()

		for color in keys:

			self.assertEqual(Bets.bets[color], self.bets_none_removed)

			items = Bets.remove(color)
			self.assertEqual(items, (color, self.first_card))
			self.assertEqual(Bets.bets[color], self.bets_one_removed)


			items = Bets.remove(color)
			self.assertEqual(items, (color, self.second_card))
			self.assertEqual(Bets.bets[color], self.bets_two_removed)


			items = Bets.remove(color)
			self.assertEqual(items, (color, self.third_card))
			self.assertEqual(Bets.bets[color], self.bets_three_removed)

			items = Bets.remove(color)
			self.assertEqual(items, (color, self.fourth_card))
			self.assertEqual(Bets.bets[color], self.bets_all_removed)

		self.assertEqual(self.empty_bets, Bets.return_bets())

if __name__ == '__main__':
	unittest.main()
