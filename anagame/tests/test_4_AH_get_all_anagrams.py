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

class Test_AnagramHelper_get_all_anagrams(unittest.TestCase):
    def setUp(self):
        #Runs before every test
        self.letters1 = ["a","b","e","d","l"]
        self.letters2 = ["p", "o", "t", "s", "r", "i", "a"]
        self.letters3 = ["p", "o", "l", "s", "r", "i", "o"]

    def test_get_all_anagrams_0(self):
        """get_all_anagrams -  Basic Data Types"""
        corpus =  ["abed", "abled", "bade", "baled", "bead", "blade"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams()
        self.assertIsInstance(actual, set)
        self.assertTrue(all(isinstance(s, str) for s in actual), "All set elements should be str")

    def test_get_all_anagrams_1(self):
        """get_all_anagrams -  Short list (2 sets of anagrams)"""
        corpus =  ["abed", "abled", "bade", "baled", "bead", "blade"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams()
        expected = {"abed", "bade", "bead","abled", "baled", "blade"}
        self.assertEqual(actual, expected)

    def test_get_all_anagrams_2(self):
        """get_all_anagrams -  Long list (20 sets of anagrams); given in the starter code"""
        corpus = [
            "abed", "abet", "abets", "abut", "acme", "acre", "acres", "actors", "actress", "airmen", "alert", "alerted",
            "ales", "aligned", "allergy", "alter", "altered", "amen", "anew", "angel", "angle", "antler", "apt", "bade",
            "baste", "bead", "beast", "beat", "beats", "beta", "betas", "came", "care", "cares", "casters", "castor",
            "costar", "dealing", "gallery", "glean", "largely", "later", "leading", "learnt", "leas", "mace", "mane",
            "marine", "mean", "name", "pat", "race", "races", "recasts", "regally", "related", "remain", "rental",
            "sale", "scare", "seal", "tabu", "tap", "treadle", "tuba", "wane", "wean",
        ]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams()
        expected = {
            "abed", "bade", "bead", "abet", "beat", "beta", "abets", "baste", "beast", "beats", "betas", "abut", "tabu", 
            "tuba", "acme", "came", "mace", "acre", "care", "race", "acres", "cares", "races", "scare", "actors", 
            "castor", "costar", "actress", "casters", "recasts", "airmen", "marine", "remain", "alert", "alter", 
            "later", "alerted", "altered", "related", "treadle", "ales", "leas", "sale", "seal", "aligned", "dealing", 
            "leading", "allergy", "gallery", "largely", "regally", "amen", "mane", "mean", "name", "anew", "wane", 
            "wean", "angel", "angle", "glean", "antler", "learnt", "rental", "apt", "pat", "tap",
        }
        self.assertEqual(actual, expected)

    def test_get_all_anagrams_3(self):
        """get_all_anagrams -  Empty words list"""
        corpus =  []
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams()
        expected=set()
        self.assertEqual(actual, expected)

    def test_get_all_anagrams_4(self):
        """get_all_anagrams -  No anagrams (each list has length 1)"""
        corpus =  ["abed", "allergy", "amen", "anew", "angel", "tap", "treadle"]
        explorer = AnagramHelper(corpus)  
        actual = explorer.get_all_anagrams()
        expected=set()
        self.assertEqual(actual, expected)

    def test_get_all_anagrams_5(self):
        """get_all_anagrams -  Mix of many anagrams and no anagrams"""
        corpus =  ["abc", "abcd", "abce", "abdc", "acb", "acbd", "acdb", "acc", 
                   "bac", "bacd", "badc", "bca", "bcad", "bcda", "cab",
                   "cabd", "cadb", "cac", "cba", "cbad", "cbda", "cca"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams()
        expected = {
            "abc", "acb", "bac", "bca", "cab", "cba", "abcd",
            "abdc", "acbd", "acdb", "bacd", "badc", "bcad", "bcda",
            "cabd", "cadb", "cbad", "cbda", "acc", "cac", "cca"
        }
        self.assertEqual(actual, expected)

    def test_get_all_anagrams_6(self):
        """get_all_anagrams -  corpus with 1 word"""
        corpus =  ["rat"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams()
        expected=set()

        self.assertEqual(actual, expected)

    def test_get_all_anagrams_7(self):
        """explorer.get_all_anagrams -  Data Types"""
        corpus= ["abed", "mouse", "bead", "baled", "abled", "rat", "blade"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams(self.letters1)
        self.assertIsInstance(actual, set)
        self.assertTrue(all(isinstance(s, str) for s in actual), "All set elements should be str")

    def test_get_all_anagrams_8(self):
        """explorer.get_all_anagrams -  Basic Example in function comments"""
        corpus= ["abed", "mouse", "bead", "baled", "abled", "rat", "blade"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams(self.letters1)
        expected= {"abed",  "abled", "baled", "bead", "blade"}
        self.assertEqual(actual, expected, f"Words that were in your set but not the expected set {actual.difference(expected)}\n Words that were in the expected set but not your set {expected.difference(actual)}")

    def test_get_all_anagrams_9(self):
        """explorer.get_all_anagrams - No anagrams in corpus"""
        corpus= ["abed", "mouse", "rat", "cat", "tiger", "elephant", "stork"]
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams(self.letters1)
        expected= set()
        self.assertEqual(actual, expected, f"Words that were in your set but not the expected set {actual.difference(expected)}\n Words that were in the expected set but not your set {expected.difference(actual)}")

    def test_get_all_anagrams_10(self):
        """explorer.get_all_anagrams - Corpus with 6 anagrams from 2 anagram families"""
        corpus = ["abed", "bead", "baled", "bade", "blade", "abled"]        
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams(self.letters1)
        expected = {"abed", "abled", "bade", "baled", "bead", "blade"}        
        self.assertEqual(actual, expected, f"Words that were in your set but not the expected set {actual.difference(expected)}\n Words that were in the expected set but not your set {expected.difference(actual)}")

    def test_get_all_anagrams_11(self):
        """explorer.get_all_anagrams - Variety of word lengths, some anagrams not in letters"""
        corpus= ["bad", "abed", "mouse", "bead", "baled", "abled", "rat", "art", "blade", "dab"]        
        explorer = AnagramHelper(corpus)
        actual = explorer.get_all_anagrams(self.letters1)
        expected ={"abed",  "abled", "bad", "baled", "bead", "blade", "dab"}       
        self.assertEqual(actual, expected, f"Words that were in your set but not the expected set {actual.difference(expected)}\n Words that were in the expected set but not your set {expected.difference(actual)}")

    def test_get_all_anagrams_12(self):
        """explorer.get_all_anagrams - Actual wordlist from valid_word_list, letter combo #1"""
        explorer = AnagramHelper(get_valid_word_list())
        actual = explorer.get_all_anagrams(self.letters1)
        expected = {'bead', 'dab', 'bade', 'lade', 'lead', 'bad', 'ale', 'dal', 'bed', 'bale', 
                    'deal', 'lad', 'deb', 'abel', 'able', 'dale', 'abed', 'elba', 'lea'}        
        self.assertEqual(actual, expected, f"Words that were in your set but not the expected set {actual.difference(expected)}\n Words that were in the expected set but not your set {expected.difference(actual)}")

    def test_get_all_anagrams_13(self):
        """explorer.get_all_anagrams - Actual wordlist from valid_word_list, letter combo #2"""
        explorer = AnagramHelper(get_valid_word_list())
        actual = explorer.get_all_anagrams(self.letters2)
        expected = {'part', 'pat', 'rats', 'riot', 'rapt', 'astir', 'pot', 'rasp', 'opts', 'tars', 'taro', 
                    'sprat', 'patios', 'star', 'spot', 'rots', 'trio', 'opt', 'rota', 'trips', 'ports', 'tar', 
                    'parts', 'ira', 'stop', 'pris', 'past', 'taos', 'pairs', 'riots', 'trios', 'stair', 'tip', 
                    'rap', 'tips', 'apt', 'asp', 'pit', 'taps', 'strop', 'strap', 'pots', 'oars', 'traps', 
                    'sari', 'pits', 'trap', 'strip', 'air', 'spat', 'spa', 'sort', 'prat', 'patois', 'raps', 
                    'pats', 'sap', 'tap', 'rips', 'spit', 'soar', 'spar', 'its', 'rat', 'post', 'arts', 
                    'paris', 'oats', 'art', 'sport', 'tops', 'top', 'airs', 'par', 'sit'}
        self.assertEqual(actual, expected, f"Words that were in your set but not the expected set {actual.difference(expected)}\n Words that were in the expected set but not your set {expected.difference(actual)}")

    def test_get_all_anagrams_14(self):
        """explorer.get_all_anagrams - Actual wordlist from valid_word_list, letter combo #3 (double letter)"""
        explorer = AnagramHelper(get_valid_word_list())
        actual = explorer.get_all_anagrams(self.letters3)
        expected = {'slip', 'spool', 'slop', 'sloop', 'lisp', 'ilo', 'lops', 'lips', 'oil', 'oslo', 'oils', 
                    'pool', 'solo', 'pools', 'silo', 'loop', 'soil', 'pris', 'rips', 'polo', 'loops'}       
        self.assertEqual(actual, expected, f"Words that were in your set but not the expected set {actual.difference(expected)}\n Words that were in the expected set but not your set {expected.difference(actual)}")


if __name__ == '__main__':
    unittest.main() 