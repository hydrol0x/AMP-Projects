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

class Test_get_words_with_no_anagrams(unittest.TestCase):
    def setUp(self):
        """
        Set up a sample corpus for testing.
        """
        self.corpus = [
            "listen", "silent", "enlist", "inlets", "stone", "tones", "unique", "apple", "banana",
            "carrot", "rat", "tar", "art", "stop", "pots", "tops", "top", "pot", "tax"
        ]
        self.explorer = AnagramHelper(self.corpus)

    def test_get_words_with_no_anagrams_0(self):
        """
         get_words_with_no_anagrams- Test that words with no anagrams in the entire corpus are correctly identified.
        """
        actual = self.explorer.get_words_with_no_anagrams()
        expected = {"unique", "apple", "banana", "carrot", "tax"}
        self.assertEqual(actual, expected)

    def test_get_words_with_no_anagrams_1(self):
        """
         get_words_with_no_anagrams- Test that words with no anagrams for a specific set of letters are correctly identified.
        """
        letters = ["u", "n", "i", "q", "u", "e"]
        actual = self.explorer.get_words_with_no_anagrams(letters)
        expected = set(self.corpus)
        self.assertEqual(actual, expected)

    def test_get_words_with_no_anagrams_2(self):
        """
         get_words_with_no_anagrams- Test that an empty set is returned when all words in the corpus have anagrams.
        """
        corpus = ["rat", "tar", "art", "stop", "pots", "tops"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_words_with_no_anagrams()
        expected = set()
        self.assertEqual(actual, expected)

    def test_get_words_with_no_anagrams_3(self):
        """
         get_words_with_no_anagrams- Test that the method returns all words with no anagrams when letters is an empty list.
        """
        actual = self.explorer.get_words_with_no_anagrams([])
        expected = {"unique", "apple", "banana", "carrot", "tax"}
        self.assertEqual(actual, expected)

    def test_get_words_with_no_anagrams_4(self):
        """
         get_words_with_no_anagrams- Test that words with no anagrams letters that match one word
        """
        letters = ["a", "p", "p", "l", "e", "s"]
        actual = self.explorer.get_words_with_no_anagrams(letters)
        expected = set(self.corpus)
        self.assertEqual(actual, expected)

    def test_get_words_with_no_anagrams_5(self):
        """
        get_words_with_no_anagrams- 5 letter anagrams only in a list of 7 letters
        """
        letters = ["l", "i", "s", "t", "e", "n", "a"]
        actual = self.explorer.get_words_with_no_anagrams(letters)
        expected = {
            "tones", "tax", "rat", "apple", "unique", "tops", "banana", "carrot", 
            "pots", "tar", "pot", "top", "art", "stop", "stone"
        }
        self.assertEqual(actual, expected)
    
    def test_get_words_with_no_anagrams_6(self):
        """
         get_words_with_no_anagrams- Anagrams made from 3 and 4 letter combinstions from letters
        """
        letters = ["p", "o", "t", "s", "r", "t", "a"]
        actual = self.explorer.get_words_with_no_anagrams(letters)
        expected = {
              "listen", "silent", "enlist", "inlets", "stone", "tones", "unique", 
              "apple", "banana", "carrot", "tax"
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
