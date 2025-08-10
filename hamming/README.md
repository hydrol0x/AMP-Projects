---
layout: spec
latex: true
---

# Deep Emoji

### Due: Start of class on Monday, July 7

## Starter Files

Please clone this repository onto your local computer. You will write code in [HammingHelper.py](HammingHelper.py) and [DeepEmoji.py](DeepEmoji.py).

To clone, you can go to the Command Prompt, get to the directory you want to put the repo in, and then type:
```bash
git clone <HTTPS_URL>
```
The URL can be found by clicking the green Code button on the GitHub browser page.
> **Note:** If you're more used to using the macOS terminal, some of the commands are different in Windows.
> For example, the equivalant of `ls` is `dir` and `control-l` is now `cls`.

After that, you can just open Atom, add the project folder, and now you can push and pull within the IDE.

Feel free to clone via GitHub Desktop if that is easier for you.

## Background
Hamming codes are sequences of bits that may or may not contain single-bit errors. The accumulation of these errors can reveal hidden messages. These messages are padded with carefully positioned parity bits to allow for identification of the exact bit in error.

**Parity** refers to using a bit to track whether the number of `1`'s in a set of bits is even or odd.

> [This site contains an interactive visual of 16-bit Hamming codes](https://harryli0088.github.io/hamming-code/) that you may find helpful!

## Overview

You will implement at least 7 functions in Part 1 and at least 1 function in Part 2.

* [Part 1: Hamming Helper](#part-1-hamming-helper)
* [Part 2: Deep Emoji](#part-2-deep-emoji)

<a name="part-1-hamming-helper"></a>
## Part 1: Hamming Helper

In the spirit of decomposition, we will implement a class called `HammingHelper` to help us eventually write a program that can interpret Hamming codes.

In [HammingHelper.py](HammingHelper.py) there are 7 functions you must implement. Notice the constructor code has been included:
```
def __init__(self, num_redundancy_bits:int):
        self.r = num_redundancy_bits
        self.n = (2 ** self.r) - 1  # Total bits in codeword
        self.k = self.n - self.r    # Data bits in codeword 
```

Feel free to add more functions and data attributes in your implementations.

#### `def parity(self, data:str):`
* Returns parity bit for a data input, represented as a binary number in string form

#### `def to_codeword(self, data: str) -> str:`
* Returns the Hamming codeword for a data input
* In other words, you are adding in the parity bits to the data input

#### `def valid_codewords(self) -> list[str]:`
* Generate all valid Hamming codewords of the length that was set in the constructor
* Hint: you may want to call another function in this class

#### `def is_valid(self, codeword: str) -> bool:`
* Checks if a given Hamming codeword is valid

#### `def syndrome(self, codeword: str) -> str:`
* Calculate the syndrome for a given codeword.

#### `def correct(self, codeword: str) -> str:`
* Given a Hamming codeword, if there is an error, it returns the corrected version.
* If there are no errors, it returns the original codeword

#### `def extract_data(self, codeword: str) -> str:`
* Extract data from a Hamming codeword independent of whether an error exists.
* In other words, given a Hamming codeword string, return the data string.

### Testing
* We are making some test cases for this assignment visible. To run them in the Command Prompt, type:

```bash
python tests\<file_name>.py
```

<a name="part-2-deep-emoji"></a>
## Part 2: Deep Emoji

Now that you have a `HammingHelper` class, you are to implement the `decode()` function in [DeepEmoji.py](DeepEmoji.py). This function will carry out the task of decoding a file with an emoji-encoded message.

Each line in the file has 2 distinct emojis.

It is **strongly encouraged** that you write helper functions and add member variables.


<a name="Submitting"></a>
## Submitting

If you are able to see this README, that means you have successfully accepted the GitHub classroom assignment!

To submit your code, just push your changes. The test cases will run every time you submit. Although you have access to the test cases for this assignment, your assignment isn't considered complete until you have pushed your code. Your "score" is the number of tests that pass when you push.
