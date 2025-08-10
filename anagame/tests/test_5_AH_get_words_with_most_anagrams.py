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

class TestEx1(unittest.TestCase):
        
    def test_get_words_with_most_anagrams_0(self):
        """get_words_with_most_anagrams -  Basic Data Types"""
        corpus = ["abed", "abled", "bade", "baled", "bead", "blade"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_words_with_most_anagrams()
        self.assertIsInstance(actual, set)
        self.assertTrue(all(isinstance(s, str) for s in actual), "All set elements should be str")
        actual = explorer.get_words_with_most_anagrams(["a","b","e","d","l"])
        self.assertIsInstance(actual, set)
        self.assertTrue(all(isinstance(s, str) for s in actual), "All set elements should be str")
        
    def test_get_words_with_most_anagrams_1(self):
        """get_words_with_most_anagrams -  Short list (2 sets of anagrams)"""
        corpus = ["abed", "abled", "bade", "baled", "bead", "blade"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_words_with_most_anagrams()
        expected = {"abed", "bade", "bead", "abled", "baled", "blade"}
        self.assertEqual(actual, expected)

    def test_get_words_with_most_anagrams_2(self):
        """get_words_with_most_anagrams -  Long list given in the starter code"""
        corpus = ['abed', 'bade', 'bead', 'acme', 'came', 'mace', 'abet', 'beat', 'beta', 'acre', 
                  'care', 'race', 'apt', 'pat', 'tap', 'abut', 'tabu', 'tuba', 'amen', 'mane', 
                  'mean', 'name', 'ales', 'leas', 'sale', 'seal', 'anew', 'wane', 'wean', 'abets', 
                  'baste', 'beast', 'beats', 'betas', 'acres', 'cares', 'races', 'scare', 'angel', 
                  'angle', 'glean', 'alert', 'alter', 'later', 'airmen', 'marine', 'remain', 'aligned', 
                  'dealing', 'leading', 'actors', 'castor', 'costar', 'antler', 'learnt', 'rental', 
                  'alerted', 'altered', 'related', 'treadle', 'actress', 'casters', 'recasts', 
                  'allergy', 'gallery', 'largely', 'regally']
        explorer = AnagramHelper(corpus)
        actual = explorer.get_words_with_most_anagrams()
        expected = {'abets','baste', 'beast', 'beats', 'betas'}
        self.assertEqual(actual, expected)

    def test_get_words_with_most_anagrams_3(self):
        """get_words_with_most_anagrams -  Empty corpus"""
        corpus = []
        explorer = AnagramHelper(corpus)
        actual = explorer.get_words_with_most_anagrams()
        expected = set()
        self.assertEqual(actual, expected)

    def test_get_words_with_most_anagrams_4(self):
        """get_words_with_most_anagrams -  No anagrams in corpus"""
        corpus = ["abed", "allergy", "amen", "anew", "angel", "tap", "treadle"]
        explorer = AnagramHelper(corpus)        
        actual = explorer.get_words_with_most_anagrams()
        expected = set()
        self.assertEqual(actual, expected)

    def test_get_words_with_most_anagrams_5(self):
        """get_words_with_most_anagrams -  Tie for most anagrams and several no anagrams"""
        corpus = ["rat", "mouse", "tar", "art", "chicken", "stop", "pots", "tops" ]
        explorer = AnagramHelper(corpus)        
        actual = explorer.get_words_with_most_anagrams()
        expected = {'art',"rat","tar", "stop", "pots", "tops"}
        self.assertEqual(actual, expected)
    
    def test_get_words_with_most_anagrams_6(self):
        """explorer.get_words_with_most_anagrams -  One anagram family that is the longest"""
        wordList= ["abed", "mouse", "bead", "baled", "abled", "rat", "blade"]
        letters = ["a","b","e","d","l"]
        explorer = AnagramHelper(wordList)
        actual = explorer.get_words_with_most_anagrams(letters)
        expected = {"baled", "abled", "blade"}
        self.assertEqual(actual, expected)

    def test_get_words_with_most_anagrams_7(self):
        """explorer.get_words_with_most_anagrams -  Two anagram families that are the longest"""
        wordList= ["abed", "mouse", "bead", "baled", "rat", "blade"]
        letters = ["a","b","e","d","l"]
        expected = {"abed","bead","baled","blade"}
        explorer = AnagramHelper(wordList)
        actual = explorer.get_words_with_most_anagrams(letters)
        self.assertEqual(actual, expected)

    def test_get_words_with_most_anagrams_8(self):
        """explorer.get_words_with_most_anagrams - default letter choices in actual wordlist from valid_anagame_words()"""
        letters = ["p", "o", "t", "s", "r", "i", "a"]        
        explorer = AnagramHelper(get_valid_word_list())
        actual = explorer.get_words_with_most_anagrams(letters)
        expected = {'opts', 'post', 'pots', 'spot', 'stop', 'tops'}
        self.assertEqual(actual, expected)

    def test_get_words_with_most_anagrams_9(self):
        """explorer.get_words_with_most_anagrams - different letter choices in actual wordlist from valid_anagame_words()"""
        letters = ["t", "e", "l", "s", "r", "i", "a"]        
        explorer = AnagramHelper(get_valid_word_list())
        actual = explorer.get_words_with_most_anagrams(letters)
        expected = {'least', 'salet', 'slate', 'stale', 'steal', 'tales', 'teals'}
        self.assertEqual(actual, expected)

    def test_get_words_with_most_anagrams_10(self):
        """explorer.get_words_with_most_anagrams - different letter choices in actual wordlist from valid_anagame_words()"""
        letters = ["p", "o", "l", "s", "r", "i", "o"] # double letter: o
        explorer = AnagramHelper(get_valid_word_list()) 
        actual = explorer.get_words_with_most_anagrams(letters)
        expected = {'loops', 'pools', 'sloop', 'spool'}
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main() 
