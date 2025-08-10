import unittest
import time
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
AnagramHelper= None
if not AnagramHelper:
    from AnagramHelper import AnagramHelper

from valid_anagame_words import get_valid_word_list
from valid_anagame_words_german import get_valid_word_list_german
from valid_anagame_words_spanish import get_valid_word_list_spanish

class Test_get_highest_possible_score(unittest.TestCase):
    def setUp(self):
        self.explorer = AnagramHelper(get_valid_word_list())
        self.explorer_german = AnagramHelper(get_valid_word_list_german())
        self.explorer_spanish = AnagramHelper(get_valid_word_list_spanish())


    def test_get_highest_possible_score_0(self):
        """get_highest_possible_score - Data Types"""
        letter_choices =[["p", "o", "t", "s", "r", "i", "a"],
                         ["p", "o", "t", "s"],
                         [],
                         ["x", "y", "z"]
                        ]
        for letters in letter_choices:
            with self.subTest(letters=letters):
                actual = self.explorer.get_highest_possible_score(letters)
                self.assertIsInstance(actual, tuple, "get_highest_possible_score should return a tuple.")
                self.assertIsInstance(actual[0], int, "get_highest_possible_score should return a tuple with an int in the first spot.")
                self.assertIsInstance(actual[1], list, "get_highest_possible_score should return a tuple with a list in the second spot.")
                self.assertEqual(actual[1], letters, "get_highest_possible_score should return the appropriate list of letters.")

    def test_get_highest_possible_score_1(self):
        """get_highest_possible_score - all consonants """
        letters = ['f', 'f','f','f','f','f','f']

        start_time = time.time()
        actual = self.explorer.get_highest_possible_score(letters)
        elapsed_time = time.time() - start_time
        self.assertLessEqual(elapsed_time, 1, "procedure should take <= 1 second")
        
        expected = 0
        self.assertEqual(actual[0], expected, f"The highest possible score from {letters} is {expected}.")
        self.assertEqual(actual[1], letters, f"{letters} should be returned.")

    def test_get_highest_possible_score_2(self):
        """get_highest_possible_score - ["p", "o", "t", "s", "r", "i", "a"] """
        letters = ["p", "o", "t", "s", "r", "i", "a"]
        
        start_time = time.time()
        actual = self.explorer.get_highest_possible_score(letters)
        elapsed_time = time.time() - start_time
        self.assertLessEqual(elapsed_time, 1, "procedure should take <= 1 second")
        
        expected = 151
        self.assertEqual(actual[0], expected, f"The highest possible score from {letters} is {expected}.")
        self.assertEqual(actual[1], letters, f"{letters} should be returned.")

    def test_get_highest_possible_score_3(self):
        """get_highest_possible_score - ["e", "o", "t", "s", "o", "i", "a"] """
        letters = ["e", "o", "t", "s", "o", "i", "a"]

        start_time = time.time()
        actual = self.explorer.get_highest_possible_score(letters)
        elapsed_time = time.time() - start_time
        self.assertLessEqual(elapsed_time, 1, "procedure should take <= 1 second")
        
        expected = 31
        self.assertEqual(actual[0], expected, f"The highest possible score from {letters} is {expected}.")
        self.assertEqual(actual[1], letters, f"{letters} should be returned.")

    def test_get_highest_possible_score_4(self):
        """get_highest_possible_score - [] """
        letters = []

        start_time = time.time()
        actual = self.explorer.get_highest_possible_score(letters)
        elapsed_time = time.time() - start_time
        self.assertLessEqual(elapsed_time, 1, "procedure should take <= 1 second")
        
        expected = 0
        self.assertEqual(actual[0], expected, f"The highest possible score from {letters} is {expected}.")
        self.assertEqual(actual[1], letters, f"{letters} should be returned.")
      
    def test_get_highest_possible_score_5(self):
        """get_highest_possible_score - German"""
        letters = ['l', 'i', 's', 't', 'e', 'n', 'g']

        start_time = time.time()
        actual = self.explorer_german.get_highest_possible_score(letters)
        elapsed_time = time.time() - start_time
        self.assertLessEqual(elapsed_time, 1, "procedure should take <= 1 second")
        
        expected = 438
        self.assertEqual(actual[0], expected, f"The highest possible score from {letters} is {expected}.")
        self.assertEqual(actual[1], letters, f"{letters} should be returned.")
    
    def test_get_highest_possible_score_5(self):
        """get_highest_possible_score - Spanish"""
        letters = ["a", "i", "s", "ñ", "e", "d", "á"]

        start_time = time.time()
        actual = self.explorer_spanish.get_highest_possible_score(letters)
        elapsed_time = time.time() - start_time
        self.assertLessEqual(elapsed_time, 1, "procedure should take <= 1 second")
        
        expected = 13
        self.assertEqual(actual[0], expected, f"The highest possible score from {letters} is {expected}.")
        self.assertEqual(actual[1], letters, f"{letters} should be returned.")
   

if __name__ == '__main__':
   	unittest.main()