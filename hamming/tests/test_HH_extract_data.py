import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
HammingHelper= None
if not HammingHelper:
    import HammingHelper as HammingHelper

class Test_extract_data(unittest.TestCase):
    def test_extract_data_7_bit_codeword(self):
        """Test extract_data for a valid 7-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(3)
        codeword = '1110000'
        expected = '1000'
        actual = helper.extract_data(codeword)
        self.assertEqual(actual, expected, f"Expected extracted data of {codeword} to be {expected}, got {actual}.")
    
    def test_extract_data_7_bit_codeword2(self):
        """Test extract_data for a valid 7-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(3)
        codeword = '1010101'
        expected = '1101'
        actual = helper.extract_data(codeword)
        self.assertEqual(actual, expected, f"Expected extracted data of {codeword} to be {expected}, got {actual}.")

    def test_extract_data_15_bit_codeword(self):
        """Test extract_data for a valid 15-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(4)
        codeword = '011011101000111'  
        expected = '11111000111'
        actual = helper.extract_data(codeword)
        self.assertEqual(actual, expected, f"Expected extracted data of {codeword} to be {expected}, got {actual}.")

    def test_extract_data_15_bit_codeword2(self):
        """Test extract_data for a valid 15-bit Hamming codeword"""
        helper = HammingHelper.HammingHelper(4)
        codeword = '001100100110011'  
        expected = '10010110011'
        actual = helper.extract_data(codeword)
        self.assertEqual(actual, expected, f"Expected extracted data of {codeword} to be {expected}, got {actual}.")

    def test_extract_data_invalid_length(self):
        """Test extract_data with invalid input length"""
        helper = HammingHelper.HammingHelper(3)
        codeword = '10101001'
        with self.assertRaises(ValueError, msg=f"Expected ValueError for {codeword}"):
            helper.extract_data(codeword)

    def test_extract_data_invalid_length2(self):
        """Test extract_data with invalid input length"""
        helper = HammingHelper.HammingHelper(4)
        codeword = '101011010001'
        with self.assertRaises(ValueError, msg=f"Expected ValueError for {codeword}"):
            helper.extract_data(codeword)

    def test_extract_data_invalid_15_bit_length(self):
        """Test extract_data with invalid 15-bit input length"""
        helper = HammingHelper.HammingHelper(4)
        codeword = '101101001010010'
        expected = '10101010010'
        actual = helper.extract_data(codeword)
        self.assertEqual(actual, expected, f"Expected extracted data of {codeword} to be {expected}, got {actual}.")
 
    def test_extract_data_invalid_7_bit_length(self):
        """Test extract_data with invalid 7-bit input length"""
        helper = HammingHelper.HammingHelper(3)
        codeword = '1011011'
        expected = '1011'
        actual = helper.extract_data(codeword)
        self.assertEqual(actual, expected, f"Expected extracted data of {codeword} to be {expected}, got {actual}.")
 
if __name__ == '__main__':
    unittest.main()