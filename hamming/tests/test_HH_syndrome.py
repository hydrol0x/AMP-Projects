import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
HammingHelper= None
if not HammingHelper:
    import HammingHelper as HammingHelper

class Test_syndrome(unittest.TestCase):
    def test_syndrome_7_bit_codeword(self):
        """Test syndrome for a valid 7-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(3)
        valid_codewords=['0000000', '1101001', '0101010', '1000011', '1001100', '0100101',
                           '1100110', '0001111', '1110000', '0011001', '1011010', '0110011', 
                           '0111100', '1010101', '0010110', '1111111']
        for codeword in valid_codewords:
            actual = helper.syndrome(codeword)
            expected = '000'
            self.assertEqual(actual, expected, f"{codeword} expected to have syndrome: {expected}, got {actual}.")
        
    def test_syndrome_15_bit_codeword(self):
        """Test syndrome for a valid 15-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(4)
        valid_codewords=['110000000111010', '000100010111011', '000000000111100', '110100010111101', '010100010111110', 
                           '100000000111111', '100000011000000', '010100001000001', '110100001000010', '000000011000011', 
                           '000100001000100', '110000011000101', '010000011000110', '100100001000111', '100100001001000', 
                           '010000011001001', '110000011001010', '000100001001011', '000000011001100', '110100001001101', 
                           '010100001001110', '100000011001111', '010000001010000', '100100011010001', '000100011010010', 
                           '110000001010011', '110100011010100', '000000001010101', '100000001010110', '010100011010111', 
                           '010100011011000', '100000001011001']
        for codeword in valid_codewords:
            actual = helper.syndrome(codeword)
            expected = '0000'
            self.assertEqual(actual, expected, f"{codeword} expected to have syndrome: {expected}, got {actual}.")
        
    def test_syndrome_7_bit_codeword_invalid(self):
        """Test syndrome for an invalid 7-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(3)
        syndrome_codewords=['1110110', '1011011', "0110101", "1011011", "1010000"]
        syndrome_values=['011', '111', '011', '111', '010']
        for codeword, synd in zip(syndrome_codewords, syndrome_values):
            actual = helper.syndrome(codeword)
            expected = synd
            self.assertEqual(actual, expected, f"{codeword} expected to have syndrome: {expected}, got {actual}.")
    
    def test_syndrome_15_bit_codeword_invalid(self):
        helper = HammingHelper.HammingHelper(4)
        syndrome_codewords=['101101001010010','110000011000100', '110101011010100', '100001011000000', '000000001011001']
        syndrome_values=['1100', '1111', '0110', '0110', '0001']

        for codeword, synd in zip(syndrome_codewords, syndrome_values):
            actual = helper.syndrome(codeword)
            expected = synd
            self.assertEqual(actual, expected, f"{codeword} expected to have syndrome: {expected}, got {actual}.")
    
    def test_syndrome_invalid_length(self):
        """Test syndrome with invalid input length"""
        helper = HammingHelper.HammingHelper(3)
        codeword = '101001'
        with self.assertRaises(ValueError, msg=f"Expected ValueError for {codeword}"):
            actual = helper.syndrome(codeword)

    def test_syndrome_invalid_length2(self):
        """Test syndrome with invalid input length"""
        helper = HammingHelper.HammingHelper(4)
        codeword = '1011010001'
        with self.assertRaises(ValueError, msg=f"Expected ValueError for {codeword}"):
            actual = helper.syndrome(codeword)

   
if __name__ == '__main__':
    unittest.main()