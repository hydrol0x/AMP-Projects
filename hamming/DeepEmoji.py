try:
    from HammingHelper import HammingHelper
except ModuleNotFoundError:
    print("HammingHelper.py is not found.")
    pass


class DeepEmoji:
    def __init__(self, r):
        # 7 bit strings
        self.hamming = HammingHelper(r)

    def decode(self, file_name: str):
        """
        Decodes a secret message from an emoji-encoded file.

        Args:
            file_name (str): The path to the file containing the emoji-encoded message.

        Returns:
            str: The decoded secret message.
        """
        with open(file_name, "r") as file:
            binary = self.emoji_to_binary(file.readlines())
            binary = [line.strip("\n") for line in binary]
            # print(binary)

            alphabet = "abcdefghijklmnopqrstuvwxyz"

            bits = ""
            letters = []
            for binary_string in binary:
                num_r_bits = self.hamming.num_parity_bits(len(binary_string))
                self.hamming.update_redundancy_bits(num_r_bits)
                syndrome = int(self.hamming.syndrome(binary_string), 2)
                if syndrome == 0:
                    # print("syndrome is 0")
                    continue
                i = syndrome - 1
                # print(f"syndrome is {syndrome}, index {
                #      i}, the bit we need is binary_string[{i}]={binary_string[i]}")
                bits += str(binary_string[i])
                # print(f"bits are {bits}")
                if len(bits) == 5:
                    if int(bits, 2) == 31:
                        letters.append(" ")
                        bits = ""
                        continue
                    pos = int(bits, 2)
                    assert pos < 26, f"Message string indicates out of bound letter. Pos is {
                        pos}"
                    letters.append(alphabet[pos])
                    bits = ""

            return "".join(letters)

    def identify_emoji(self, emoji_line: str):
        emoji_1 = emoji_line[0]
        emoji_2 = ""
        for emoji in emoji_line:
            if emoji != emoji_1:
                emoji_2 = emoji
                break

        return (emoji_1, emoji_2)

    def emoji_to_binary(self, emoji_message: list[str]):
        """
        For even-numbered lines the first emoji in the line
        represents a 0, while the other emoji represents a 1. For
        odd-numbered lines in the file, the first-emoji represents a 1,
        while the second emoji represents a 0.
        """
        first_bit = 1
        second_bit = 0
        lines = []
        for line in emoji_message:
            emoji_1, emoji_2 = self.identify_emoji(line)

            # print(f"emoji 1 : {emoji_1} = {
            #       first_bit} ; emojo 2: {emoji_2} = {second_bit}")
            line = line.replace(emoji_1, str(first_bit))
            line = line.replace(emoji_2, str(second_bit))

            lines.append(line)
            first_bit = 1 if first_bit == 0 else 0
            second_bit = 1 if second_bit == 0 else 0

        return lines


if __name__ == '__main__':
    deep = DeepEmoji(4)
    encrypted_file_name = "mystery4.txt"

    decoded_message = deep.decode(encrypted_file_name)
    print(decoded_message)
