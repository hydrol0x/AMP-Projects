import unittest
import sys 
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from Camel import Camel, Color
import random

class TestCamel(unittest.TestCase):
	# actual, expted
	all_colors = [Color.BLUE, Color.RED, Color.GREEN, Color.PURPLE, Color.YELLOW]

	def test_initalize_camel(self):
		""" Test creating only one camel object"""
		camel = Camel(Color.RED)
		self.assertEqual(camel.get_color(), Color.RED)
		self.assertEqual(camel.get_position(), 0)
		self.assertEqual(camel.get_stacked_on_me(), None)

	def test_initalize_camels(self):
		""" Test initalized all camels"""
		for color in self.all_colors:
			camel = Camel(color)
			self.assertEqual(camel.get_color(), color)
			self.assertEqual(camel.get_position(), 0)
			self.assertEqual(camel.get_stacked_on_me(), None)

	def test_move_camel_once(self):
		camel = Camel(Color.RED)
		move_forward = random.randint(1, 3)
		camel.add_position(move_forward)
		self.assertEqual(move_forward, camel.get_position())	

	def test_move_camel_twice(self):
		camel = Camel(Color.RED)
		move_forward = random.randint(1, 3)
		camel.add_position(move_forward)
		self.assertEqual(move_forward, camel.get_position())	

if __name__ == '__main__':
	unittest.main()
