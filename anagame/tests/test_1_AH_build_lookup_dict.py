import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
AnagramHelper= None
if not AnagramHelper:
    from AnagramHelper import AnagramHelper


class Test_AnagramHelper_build_lookup_dict(unittest.TestCase):

    def test_build_lookup_dict_build_lookup_dict_0(self):
        """build_lookup_dict - Data Types"""
        corpus = ["abcd", "efg", "hijk", "lmnop", "qrs", "tuv", "wxyz", "dcba", "gfe", "kjih", "ponml", "srq", "vut", "zyxw"]
        explorer = AnagramHelper(corpus)
        actual = explorer.build_lookup_dict()
        self.assertIsInstance(actual, dict)
        self.assertEqual(len(actual), 7, "There should be 7 unique anagram families")
        self.assertTrue(all(isinstance(key, tuple) for key in actual), "All keys should be tuples")
        self.assertTrue(all(key == tuple(sorted(key)) for key in actual), "All keys should be sorted tuples")
        self.assertTrue(all(isinstance(family, set) for family in actual.values()), "All values should be set")
        self.assertTrue(all(len(family) == 2 for family in actual.values()), "All anagram families should have two corpus")  
 
    def test_build_lookup_dict_build_lookup_dict_1(self):
        """build_lookup_dict -  Short list (2 sets of anagrams)"""
        corpus = ["abed", "abled", "bade", "baled", "bead", "blade"]
        explorer = AnagramHelper(corpus)
        actual = explorer.build_lookup_dict()
        expected = {
            ("a", "b", "d", "e"): {"abed", "bade", "bead"},
            ("a", "b", "d", "e", "l"): {"abled", "baled", "blade"},
        }
        self.assertEqual(actual, expected)

    def test_build_lookup_dict_2(self):
        """build_lookup_dict -  Long list (20 sets of anagrams); given in the starter code"""
        corpus = ['abed', 'bade', 'bead', 'acme', 'came', 'mace', 'abet', 'beat', 'beta', 'acre', 'care', 'race', 'apt', 'pat', 'tap', 'abut', 'tabu', 'tuba', 'amen', 'mane', 'mean', 'name', 'ales', 'leas', 'sale', 'seal', 'anew', 'wane', 'wean', 'abets', 'baste', 'beast', 'beats', 'betas', 'acres', 'cares', 'races', 'scare', 'angel', 'angle', 'glean', 'alert', 'alter', 'later', 'airmen', 'marine', 'remain', 'aligned', 'dealing', 'leading', 'actors', 'castor', 'costar', 'antler', 'learnt', 'rental', 'alerted', 'altered', 'related', 'treadle', 'actress', 'casters', 'recasts', 'allergy', 'gallery', 'largely', 'regally']
        explorer = AnagramHelper(corpus)
        actual = explorer.build_lookup_dict()
        expected = {
            ("a", "b", "d", "e"): {"abed", "bade", "bead"},
            ("a", "b", "e", "t"): {"abet", "beat", "beta"},
            ("a", "b", "e", "s", "t"): {"abets", "baste", "beast", "beats", "betas"},
            ("a", "b", "t", "u"): {"abut", "tabu", "tuba"},
            ("a", "c", "e", "m"): {"acme", "came", "mace"},
            ("a", "c", "e", "r"): {"acre", "care", "race"},
            ("a", "c", "e", "r", "s"): {"acres", "cares", "races", "scare"},
            ("a", "c", "o", "r", "s", "t"): {"actors", "castor", "costar"},
            ("a", "c", "e", "r", "s", "s", "t"): {"actress", "casters", "recasts"},
            ("a", "e", "i", "m", "n", "r"): {"airmen", "marine", "remain"},
            ("a", "e", "l", "r", "t"): {"alert", "alter", "later"},
            ("a", "d", "e", "e", "l", "r", "t"): {"alerted", "altered", "related", "treadle"},
            ("a", "e", "l", "s"): {"ales", "leas", "sale", "seal"},
            ("a", "d", "e", "g", "i", "l", "n"): {"aligned", "dealing", "leading"},
            ("a", "e", "g", "l", "l", "r", "y"): {"allergy", "gallery", "largely", "regally"},
            ("a", "e", "m", "n"): {"amen", "mane", "mean", "name"},
            ("a", "e", "n", "w"): {"anew", "wane", "wean"},
            ("a", "e", "g", "l", "n"): {"angel", "angle", "glean"},
            ("a", "e", "l", "n", "r", "t"): {"antler", "learnt", "rental"},
            ("a", "p", "t"): {"apt", "pat", "tap"},
        }
        self.assertEqual(actual, expected)

    def test_build_lookup_dict_3(self):
        """build_lookup_dict -  Empty corpus list"""
        corpus = []
        explorer = AnagramHelper(corpus)       
        actual = explorer.build_lookup_dict()
        self.assertEqual(actual, {})

    def test_build_lookup_dict_4(self):
        """build_lookup_dict -  No anagrams (each list has length 1)"""
        corpus = ["abed", "allergy", "amen", "anew", "angel", "tap", "treadle"]
        explorer = AnagramHelper(corpus)        
        actual = explorer.build_lookup_dict()
        expected = {
            ("a", "b", "d", "e"): {"abed"},
            ("a", "e", "g", "l", "l", "r", "y"): {"allergy"},
            ("a", "e", "m", "n"): {"amen"},
            ("a", "e", "n", "w"): {"anew"},
            ("a", "e", "g", "l", "n"): {"angel"},
            ("a", "p", "t"): {"tap"},
            ("a", "d", "e", "e", "l", "r", "t"): {"treadle"},
        }
        self.assertEqual(actual, expected)

    def test_build_lookup_dict_5(self):
        """build_lookup_dict -  Mix of many anagrams and no anagrams"""
        corpus = ["abc","abcd","abce","abdc","acb","acbd","acdb","acc","bac","bacd","badc","bca","bcad","bcda","cab","cabd","cadb","cac","cba","cbad","cbda","cca"]
        explorer = AnagramHelper(corpus)
        actual = explorer.build_lookup_dict()
        expected = {
            ("a", "b", "c"): {"abc", "acb", "bac", "bca", "cab", "cba"},
            ("a", "b", "c", "d"): {"abcd", "abdc", "acbd", "acdb", "bacd", "badc", "bcad", "bcda", "cabd", "cadb", "cbad", "cbda"},
            ("a", "b", "c", "e"): {"abce"},
            ("a", "c", "c"): {"acc", "cac", "cca"},
        }
        self.assertEqual(actual, expected)

    def test_build_lookup_dict_6(self):
        """build_lookup_dict -  corpus with 1 word"""
        corpus = ["rat"]
        explorer = AnagramHelper(corpus)        
        actual = explorer.build_lookup_dict()
        self.assertEqual(actual, {("a", "r", "t"): {"rat"}})

if __name__ == '__main__':
    unittest.main() 