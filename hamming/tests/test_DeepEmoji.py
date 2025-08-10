import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
DeepEmoji= None
HammingHelper=None
if not DeepEmoji:
    import DeepEmoji as DeepEmoji
if not HammingHelper:
    import HammingHelper as HammingHelper

class Test_DeepEmoji(unittest.TestCase):

    def test_eval_1(self):
        """Placeholder test"""
        actual = True
        self.assertTrue(actual, "This is a placeholder test.")

if __name__ == '__main__':
    unittest.main()