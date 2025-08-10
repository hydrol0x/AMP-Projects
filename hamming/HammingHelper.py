import math
from functools import reduce
from operator import ixor, iand, ior


class HammingHelper:
    def __init__(self, num_redundancy_bits: int):
        self.r = num_redundancy_bits
        self.n = (2 ** self.r) - 1  # Total bits in codeword
        self.k = self.n - self.r    # Data bits in codeword

    def update_redundancy_bits(self, new_num_redundancy_bits: int):
        self.r = new_num_redundancy_bits
        self.n = (2 ** self.r) - 1
        self.k = self.n - self.r

    def parity(self, data: str):
        """
        Calculate the parity bit for the given data.

        Args:
            data (str): A binary string representing the data.

        Returns:
            int: The parity bit (0 or 1).

        Examples:
            >>> HammingHelper(3).parity('1011')
            1
            >>> HammingHelper(3).parity('1001')
            0
        """

        """"
        for parity first AND the bit mask (which is determined by the parity bit binary representation)
        then bit shift and XOR to get the parity of the masked bit string (or just do .count(1))
        """

        return data.count("1") % 2

    def calculate_parity_bit(self, data: str, parity_bit_pos: int):
        """
        Args:
            parity_bit_pos (int): This is one indexed
        Examples:
            >>> HammingHelper(3).calculate_parity_bit("pp1p011", 1)
            0
            >>> HammingHelper(3).calculate_parity_bit("pp1p011", 2)
            1
            >>> HammingHelper(3).calculate_parity_bit("pp1p011", 4)
            0
        """
        count = 0
        for i, bit in enumerate(data):
            # AND the index of the data bit and the parity bit
            # index is i+1 since we are 1 indexes
            index = i+1
            # print(f"bit {bit} at index {index}")
            110
            if (parity_bit_pos & index) and (index is not parity_bit_pos):
                # print(f"parity bit covers; {
                #      bin(parity_bit_pos)} & {bin(index)}")
                if bit == "1":
                    count += 1
                # print(f"count is {count}")
        return count % 2

    def num_parity_bits(self, data_len: int) -> int:
        return 1+math.floor(math.log2(data_len))  # add one to account for 2**0

    def pad_data(self, data: str) -> str:
        """
        Pad data string with parity bit positions
        """
        num_parity_bits = self.r
        parity_bit_pos = [2**i for i in range(num_parity_bits)]

        padded_data = ""
        data_index = 0
        for i in range(num_parity_bits + len(data)):
            index = i+1
            if index in parity_bit_pos:
                padded_data += "p"
            else:
                padded_data += data[data_index]
                data_index += 1
        return padded_data

    def to_codeword(self, data: str) -> str:
        """
        Convert data to a Hamming codeword.

        Args:
            data (str): A binary string representing the data.

        Returns:
            str: The Hamming codeword.

        Raises:
            ValueError: If the codeword length does not match the expected length.

        Examples:
            >>> h = HammingHelper(3)
            >>> h.to_codeword('1010')
            '1011010'
            >>> h.to_codeword('1111')
            '1111111'
        """
        if len(data) != self.k:
            raise ValueError(
                "Codeword length doesn't match the expected length.")
        padded = self.pad_data(data)
        for p_pos in range(self.r):
            parity_bit_value = self.calculate_parity_bit(padded, 2**p_pos)
            padded = padded.replace("p", str(parity_bit_value), 1)
        return padded

    def is_valid(self, codeword: str) -> bool:
        """
        Check if a given codeword is valid.

        Args:
            codeword (str): A binary string representing the codeword.

        Returns:
            bool: True if the codeword is valid, False otherwise.

        Examples:
            >>> h = HammingHelper(3)
            >>> h.is_valid('1010101')
            True
            >>> h.is_valid('1010100')
            False
        """
        if len(codeword) != self.n:
            return False
        return self.to_codeword(self.extract_data(codeword)) == codeword

    def syndrome(self, codeword: str) -> str:
        """
        Calculate the syndrome for a given codeword.

        Args:
            codeword (str): A binary string representing the codeword.

        Returns:
            str: The syndrome as a binary string.

        Raises:
            ValueError: If the codeword length does not match the expected length.

        Examples:
            >>> h = HammingHelper(3)
            >>> h.syndrome('1011010')
            '000'
            >>> h.syndrome('1010100')
            '111'
        """
        # return 0 if no issues, return the position of the error otherwise
        if len(codeword) != self.n:
            raise ValueError(
                f"The codeword length {len(codeword)} does not match the expected length of {self.n} for codeword {codeword}.")
        positions = []
        syndrome = ""
        for i in range(self.r):
            p_bit_pos = 2**i
            p_bit = self.calculate_parity_bit(codeword, p_bit_pos)
            # print(f"p bit pos is {p_bit_pos}")

            # print(f"p_bit is {codeword[p_bit_pos - 1]}")
            # print(f"calc p_bit is {p_bit}")

            if p_bit != int(codeword[p_bit_pos - 1]):
                # print(f"The p bit is wrong")
                syndrome = "1" + syndrome
            else:

                syndrome = "0" + syndrome
            # print(list(map(bin, positions)))

        # return format(reduce(ixor, positions), f'0{self.r}b')
        return syndrome

    def correct(self, codeword: str) -> str:
        """
        Correct a single-bit error in the codeword, if present. If no error is present,
        returns the original codeword

        Args:
            codeword (str): A binary string representing the codeword.

        Returns:
            bool: True if the codeword was corrected, False otherwise.

        Raises:
            ValueError: If the codeword length does not match the expected length.

        Examples:
            >>> h = HammingHelper(3)
            >>> h.correct('1011011')
            '1011010'
            >>> h.correct('1010101')
            '1010101'
        """
        if len(codeword) != self.n:
            raise ValueError(
                "The codeword length does not match the expected length.")
        incorrect_pos = int(self.syndrome(codeword), 2)
        if incorrect_pos == 0:
            return codeword
        # print(f"incorrect pos {incorrect_pos}")
        index = incorrect_pos - 1
        new_codeword = list(codeword)
        # print(f"old {new_codeword}")
        if codeword[index] == "0":
            new_codeword[index] = "1"
            # print(f"new {new_codeword}")
        else:
            # print(f"new {new_codeword}")
            new_codeword[index] = "0"
        return ''.join(new_codeword)

    def extract_data(self, codeword: str) -> str:
        """
        Extract data from a Hamming codeword independent of whether an error exists.

        Args:
            codeword (str): A binary string representing the codeword.

        Returns:
            str: The extracted data.

        Raises:
            ValueError: If the codeword length does not match the expected length.

        Examples:
            >>> h = HammingHelper(3)
            >>> h.extract_data('1010101')
            '1101'
            >>> h.extract_data('1110111')
            '1111'
        """
        if len(codeword) != self.n:
            raise ValueError(
                "Codeword length does not match the expected length.")

        parity_bit_pos = [2**i for i in range(self.r)]
        # print(f"parity bit pos {parity_bit_pos}")
        data = ""
        for i in range(len(codeword)):
            index = i+1
            if index not in parity_bit_pos:
                data += codeword[i]
        return data

    def __str__(self) -> str:
        """
        Return a string representation of the HammingHelper instance.

        Returns:
            str: A string describing the HammingHelper instance.

        Examples:
            >>> h = HammingHelper(3)
            >>> str(h)
            'HammingHelper(r=3, n=7, k=4)'
        """
        return f"HammingHelper(r={self.r}, n={self.n}, k={self.k})"


if __name__ == '__main__':
    hamming = HammingHelper(3)
    data = "1101"
    num_p = hamming.num_parity_bits(len(data))

    # print(hamming.num_parity_bits(len(data)))
    # print(f"parity bits are {[2**i for i in range(num_p)]}")
    # padded = hamming.pad_data(data)
    # print(f"padded data: {padded}")
    # codeword = hamming.to_codeword(data)
    # print(f"original data is {data}")
    # print(f"codeword is {codeword}")
    # extracted_data = hamming.extract_data(codeword)
    # print(f"extracted data is {extracted_data}")
    # print("===============\n\n")
    # print(f"data is 1011010")
    # syndrome = hamming.syndrome("1011010")
    # print(f"syndrome is {syndrome}")

# pr# int("===============\n\n")
    # print(f"data is 1110110 ")
    # syndrome = hamming.syndrome("1110110")
    # print(f"syndrome is {syndrome}")

    # print("\n\n")
    # print(hamming.syndrome('1010100'))

    # r = 3
    # data = "1011"
    # data2 = "1001"
    # valid_codeword = "1011010"
    # invalid_codeword = "1011011"
    # hamming = HammingHelper(3)
    # print(hamming)

    # codeword_data = hamming.to_codeword(data)
    # codeword_data2 = hamming.to_codeword(data2)
    # print(f"Hamming Codeword for {data}: ", codeword_data)
    # print(f"Bit Parity of {repr(data)}: ", hamming.parity(data))

    # print("Expected: '1011010'")
    print("Expected 1010101")
    print(hamming.correct('1010101'))
    # print(hamming.correct('1011011'))

    # print(f"Is {repr(valid_codeword)} a valid codeword? ",
    #       hamming.is_valid(valid_codeword))
    # print(f"Syndrome of {repr(valid_codeword)}: ",
    #       hamming.syndrome(valid_codeword))
    # print(f"Is {repr(invalid_codeword)} a valid codeword? ",
    #       hamming.is_valid(invalid_codeword))
    # print(f"Syndrome of {repr(invalid_codeword)}: ",
    #       hamming.syndrome(invalid_codeword))

    # corrected = hamming.correct(invalid_codeword)
    # print(f"Corrected {repr(invalid_codeword)}: ", corrected)

    # print(f"Extracted data from {repr(codeword_data)
    #                              }: ", hamming.extract_data(codeword_data))
    # print(f"Extracted data from {repr(codeword_data2)
    #                              }: ", hamming.extract_data(codeword_data2))
