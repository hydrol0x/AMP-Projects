import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
HammingHelper= None
if not HammingHelper:
    import HammingHelper as HammingHelper

class Test_to_codeword(unittest.TestCase):
    def test_to_codeword_7_bit_codeword(self):
        """Test to_codeword for a 7-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(3)
        data=['1110', '0110', '1111', '0011', "0000", "1001", "1010"]
        codewords = ['0010110', '1100110', '1111111', '1000011', '0000000', '0011001', '1011010']
        for d, c in zip(data, codewords):
            actual = helper.to_codeword(d)
            expected = c
            self.assertEqual(actual, expected, f"{d} expected to have correct: {expected}, got {actual}.")
    
    def test_to_codeword_15_bit_codeword(self):
        """Test to_codeword for a valid 15-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(4)
        data=['00000111010', '00010111011', '00000111100', '00010111101', '00101111101']
        codewords = ['110000000111010', '110000110111011', '000000000111100', '000000110111101', '000001001111101']
        for d, c in zip(data, codewords):
            actual = helper.to_codeword(d)
            expected = c
            self.assertEqual(actual, expected, f"{d} expected to have correct: {expected}, got {actual}.")
    
    def test_to_codeword_invalid_length(self):
        """Test to_codeword with invalid input length"""
        helper = HammingHelper.HammingHelper(3)
        codeword = '101001'
        with self.assertRaises(ValueError, msg=f"Expected ValueError for {codeword}"):
            actual = helper.to_codeword(codeword)

    def test_to_codeword_invalid_length2(self):
        """Test to_codeword with invalid input length"""
        helper = HammingHelper.HammingHelper(4)
        codeword = '1011010001'
        with self.assertRaises(ValueError, msg=f"Expected ValueError for {codeword}"):
            actual = helper.to_codeword(codeword)

   
if __name__ == '__main__':
    unittest.main()