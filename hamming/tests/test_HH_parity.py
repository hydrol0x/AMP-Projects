import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
HammingHelper= None
if not HammingHelper:
    import HammingHelper as HammingHelper

class Test_parity(unittest.TestCase):
    def test_parity_all_zeros_with_4(self):
        """Test parity for all zeros with constructor parameter 4"""
        helper = HammingHelper.HammingHelper(4)
        data = '0000'
        expected = 0
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_all_ones_with_4(self):
        """Test parity for all ones with constructor parameter 4"""
        helper = HammingHelper.HammingHelper(4)
        data = '1111'
        expected = 0
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_mixed_bits_even_with_4(self):
        """Test parity for mixed bits with even number of 1s and constructor parameter 4"""
        helper = HammingHelper.HammingHelper(4)
        data = '1100'
        expected = 0
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_mixed_bits_odd_with_4(self):
        """Test parity for mixed bits with odd number of 1s and constructor parameter 4"""
        helper = HammingHelper.HammingHelper(4)
        data = '1101'
        expected = 1
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")
    def test_parity_all_zeros(self):
        """Test parity for all zeros"""
        helper = HammingHelper.HammingHelper(3)
        data = '0000'
        expected = 0
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_all_ones(self):
        """Test parity for all ones"""
        helper = HammingHelper.HammingHelper(3)
        data = '1111'
        expected = 0
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_mixed_bits_even(self):
        """Test parity for mixed bits with even number of 1s"""
        helper = HammingHelper.HammingHelper(3)
        data = '1010'
        expected = 0
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_mixed_bits_odd(self):
        """Test parity for mixed bits with odd number of 1s"""
        helper = HammingHelper.HammingHelper(3)
        data = '1011'
        expected = 1
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_single_bit_0(self):
        """Test parity for a single bit 0"""
        helper = HammingHelper.HammingHelper(3)
        data = '0'
        expected = 0
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_single_bit_1(self):
        """Test parity for a single bit 1"""
        helper = HammingHelper.HammingHelper(3)
        data = '1'
        expected = 1
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_large_input(self):
        """Test parity for a large binary string"""
        helper = HammingHelper.HammingHelper(3)
        data = '1101010101010101'
        expected = 1
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_larger_input_even_parity(self):
        """Test parity for a larger binary string with even parity"""
        helper = HammingHelper.HammingHelper(3)
        data = '110101010101010110'
        expected = 0
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

    def test_parity_empty_string(self):
        """Test parity for an empty string"""
        helper = HammingHelper.HammingHelper(3)
        data = ''
        expected = 0
        actual = helper.parity(data)
        self.assertEqual(actual, expected, f"Expected parity of {data} to be {expected}, got {actual}.")

if __name__ == '__main__':
    unittest.main()