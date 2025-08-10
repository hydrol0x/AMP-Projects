import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
HammingHelper= None
if not HammingHelper:
    import HammingHelper as HammingHelper

class Test_correct(unittest.TestCase):
    def test_correct_7_bit_codeword(self):
        """Test correct for a valid 7-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(3)
        valid_codewords=['0000000', '1101001', '0101010', '1000011', '1001100', '0100101']
        corrected_codewords = ['0000000', '1101001', '0101010', '1000011', '1001100', '0100101']
        for codeword, corrected in zip(valid_codewords, corrected_codewords):
            actual = helper.correct(codeword)
            expected = corrected
            self.assertEqual(actual, expected, f"{codeword} expected to have correct: {expected}, got {actual}.")
    
    def test_correct_15_bit_codeword(self):
        """Test correct for a valid 15-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(4)
        valid_codewords=['110000000111010', '000100010111011', '000000000111100', '110100010111101', '010100010111110']
        corrected_codewords = ['110000000111010', '000100010111011', '000000000111100', '110100010111101', '010100010111110']
        for codeword, corrected in zip(valid_codewords, corrected_codewords):
            actual = helper.correct(codeword)
            expected = corrected
            self.assertEqual(actual, expected, f"{codeword} expected to have correct: {expected}, got {actual}.")
    
    def test_correct_7_bit_codeword_invalid(self):
        """Test correct for an invalid 7-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(3)
        correct_codewords=['1110110', '1011011', "0110101", "1011011", "1010000"]
        correct_values=['1100110', '1011010', '0100101', '1011010', '1110000']
        for codeword, synd in zip(correct_codewords, correct_values):
            actual = helper.correct(codeword)
            expected = synd
            self.assertEqual(actual, expected, f"{codeword} expected to have correct: {expected}, got {actual}.")
    
    def test_correct_15_bit_codeword_invalid(self):
        helper = HammingHelper.HammingHelper(4)
        correct_codewords=['101101001010010','110000011000100', '110101011010100', '100001011000000', '000000001011001']
        correct_values=['101101001011010', '110000011000101', '110100011010100', '100000011000000', '100000001011001']

        for codeword, synd in zip(correct_codewords, correct_values):
            actual = helper.correct(codeword)
            expected = synd
            self.assertEqual(actual, expected, f"{codeword} expected to have correct: {expected}, got {actual}.")
    
    def test_correct_invalid_length(self):
        """Test correct with invalid input length"""
        helper = HammingHelper.HammingHelper(3)
        codeword = '101001'
        with self.assertRaises(ValueError, msg=f"Expected ValueError for {codeword}"):
            actual = helper.correct(codeword)

    def test_correct_invalid_length2(self):
        """Test correct with invalid input length"""
        helper = HammingHelper.HammingHelper(4)
        codeword = '1011010001'
        with self.assertRaises(ValueError, msg=f"Expected ValueError for {codeword}"):
            actual = helper.correct(codeword)

   
if __name__ == '__main__':
    unittest.main()