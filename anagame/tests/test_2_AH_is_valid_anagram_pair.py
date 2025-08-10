import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
AnagramHelper= None
if not AnagramHelper:
    from AnagramHelper import AnagramHelper

from valid_anagame_words import get_valid_word_list

class Test_AnagramHelper_is_valid_anagram_pair(unittest.TestCase):
  @classmethod
  def setUpClass(self):
      '''Runs once, before any tests are run'''
      self.letters = ["p", "o", "t", "s", "r", "i", "a"]
      self.double_letters = ["p", "o", "l", "s", "r", "i", "o"]
      self.short_letters = ["p", "a", "t", "s"]
    
  def setUp(self):
      '''Runs before every test'''
      self.explorer = AnagramHelper(get_valid_word_list())

  def test_is_valid_anagram_pair_0(self):
      """explorer.is_valid_anagram_pair -  Data Type"""
      pair =("pot", "top")
      actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
      self.assertIsInstance(actual, bool)
  
  def test_is_valid_anagram_pair_1(self):
      """explorer.is_valid_anagram_pair -  Basic True"""
      pair =("pot", "top")
      actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
      self.assertEqual(actual, True)

  def test_is_valid_anagram_pair_2(self):
      """explorer.is_valid_anagram_pair -  Basic True with mixed Capitalization"""
      pair =("pot", "Top")
      actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
      self.assertEqual(actual, True)

  def test_is_valid_anagram_pair_3(self):
      """explorer.is_valid_anagram_pair -  Basic False"""
      pair =("pot", "rat")
      actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
      self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_4(self):
      """explorer.is_valid_anagram_pair -  Identical Words"""
      pair =("pot", "pot")
      actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
      self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_5(self):
     """explorer.is_valid_anagram_pair -  Identical Words with Mixed Capitalization"""
     pair =("pot", "POT")
     actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
     self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_6(self):
        """explorer.is_valid_anagram_pair -  Nearly Identical Words"""
        pair =("pot", "pit")
        actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
        self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_7(self):
      """explorer.is_valid_anagram_pair -  Valid anagrams, but not in letters"""
      pair =("baste", "beast")
      actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
      self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_8(self):
        """explorer.is_valid_anagram_pair -  1 letter words"""
        pair =("t", "t")
        actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
        self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_9(self):
        """explorer.is_valid_anagram_pair -  Almost Anagrams: Plural, all letters present in letters"""
        pair =("pot", "pots")
        actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
        self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_10(self):
        """explorer.is_valid_anagram_pair -  Two Empty Strings"""
        pair =("", "")
        actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
        self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_11(self):
        """explorer.is_valid_anagram_pair - Double letter in word but not letters list"""
        pair =("loop", "pool")
        actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
        self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_12(self):
        """explorer.is_valid_anagram_pair - Double letter in word and also letters list"""
        pair =("loop", "pool")
        actual = self.explorer.is_valid_anagram_pair(pair, self.double_letters)
        self.assertEqual(actual, True)

  def test_is_valid_anagram_pair_13(self):
        """explorer.is_valid_anagram_pair -  2 letter words"""
        pair =("on", "no")
        actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
        self.assertEqual(actual, False)
  
  def test_is_valid_anagram_pair_14(self):
        """explorer.is_valid_anagram_pair - Anagrams, but not in valid_word_list()"""
        pair =("sria", "airs")
        actual = self.explorer.is_valid_anagram_pair(pair, self.letters)
        self.assertEqual(actual, False)
  
  def test_is_valid_anagram_pair_15(self):
        """explorer.is_valid_anagram_pair - Anagrams in valid_word_list(), not in four letters """
        pair =("stop", "pots")
        actual = self.explorer.is_valid_anagram_pair(pair, self.short_letters)
        self.assertEqual(actual, False)
  
  def test_is_valid_anagram_pair_16(self):
        """explorer.is_valid_anagram_pair - Anagrams in valid_word_list(), in four letters """
        pair =("pats", "taps")
        actual = self.explorer.is_valid_anagram_pair(pair, self.short_letters)
        self.assertEqual(actual, True)

  def test_is_valid_anagram_pair_17(self):
        """explorer.is_valid_anagram_pair - Not anagrams, in four letters """
        pair =("taps", "sat")
        actual = self.explorer.is_valid_anagram_pair(pair, self.short_letters)
        self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_18(self):
        """explorer.is_valid_anagram_pair - Not anagrams, three of four letters """
        pair =("tap", "pat")
        actual = self.explorer.is_valid_anagram_pair(pair, self.short_letters)
        self.assertEqual(actual, True)

  def test_is_valid_anagram_pair_19(self):
        """explorer.is_valid_anagram_pair - anagrams, no letters """
        pair =("tap", "pat")
        actual = self.explorer.is_valid_anagram_pair(pair)
        self.assertEqual(actual, True)

  def test_is_valid_anagram_pair_20(self):
        """explorer.is_valid_anagram_pair - anagrams, no letters """
        pair =("baste", "beast")
        actual = self.explorer.is_valid_anagram_pair(pair)
        self.assertEqual(actual, True)

  def test_is_valid_anagram_pair_21(self):
        """explorer.is_valid_anagram_pair - not anagrams, no letters """
        pair =("baste", "best")
        actual = self.explorer.is_valid_anagram_pair(pair)
        self.assertEqual(actual, False)

  def test_is_valid_anagram_pair_22(self):
        """explorer.is_valid_anagram_pair -  anagrams w/ double letters, no letters """
        pair =("loop", "pool")
        actual = self.explorer.is_valid_anagram_pair(pair)
        self.assertEqual(actual, True)

if __name__ == '__main__':
    unittest.main() 