import valid_anagame_words
from valid_anagame_words_spanish import get_valid_word_list_spanish
from valid_anagame_words_german import get_valid_word_list_german
from valid_anagame_words import get_valid_word_list

from itertools import combinations, combinations_with_replacement
from collections import Counter
import math
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

class AnagramHelper:
    def __init__(self, valid_words: list[str]):
        self.__corpus = valid_words
        # only calculated once, when the object is created
        self.__lookup_dict = self.build_lookup_dict()

    @property
    def corpus(self):
        return self.__corpus

    @property
    def lookup_dict(self):
        return self.__lookup_dict

    def generate_hash(self, word: str) -> tuple[str, ...]:
        """
        Generates a hash for the given word by sorting its letters and returning a tuple.

        Args:
            word (str): The word to generate a hash for.

        Returns:
            tuple[str]: A tuple representing the sorted letters of the word.

        Examples:
        >>> explorer = AnagramHelper(["listen", "silent"])
        >>> explorer.generate_hash("listen")
        ('e', 'i', 'l', 'n', 's', 't')
        """
        
        return tuple(sorted(word))

    def build_lookup_dict(self) -> dict[tuple[str, ...], set[str]]:
        """
        Builds a lookup dictionary where keys are sorted tuples of lowercase letters, 
        and values are sets of lowercase words from self.__corpus with the same letters.
        Facilitates quick retrieval of anagram families based on their sorted letter representation.

        Returns:
            dict: A dictionary mapping sorted letter tuples to sets of words.

        Examples:
        >>> explorer = AnagramHelper(["listen", "silent", "enlist", "inlets", "apple"])
        >>> lookup = explorer.build_lookup_dict()
        >>> lookup[('e', 'i', 'l', 'n', 's', 't')] ==  {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> ('s', 't', 'o', 'n', 'e') in lookup
        False
        >>> lookup[('a', 'e', 'l', 'p', 'p')] == {"apple"}
        True
        """

        lookup: dict[tuple[str, ...], set[str]]= {}
        for word in self.corpus:
            key = self.generate_hash(word)
            if key not in lookup:
                lookup[key] = {word}
            else:
                lookup[key].add(word)

        return lookup

    def is_valid_anagram_pair(self, pair: tuple[str, str], letters: list[str] = None) -> bool:
        """
        Valid anagram pairs must exist in the corpus. 
        If letters are provided, both words must match the letters in the list (without replacement).
        Words must be at least 3 characters long and not identical.

        Args:
            pair (tuple[str, str]): A tuple containing two words to check.
            letters (list[str]): A list of letters available for forming anagrams.

        Returns:
            bool: True if the pair forms a valid anagram, False otherwise.

        Examples:
        >>> explorer = AnagramHelper(["listen", "silent", "enlist", "inlets"])
        >>> explorer.is_valid_anagram_pair(("listen", "silent"), ["l", "i", "s", "t", "e", "n"])
        True
        >>> explorer.is_valid_anagram_pair(("stone", "tones"), ["s", "t", "o", "n", "e"])
        False
        >>> explorer.is_valid_anagram_pair(("apple", "pale"), ["a", "p", "p", "l", "e"])
        False
        """

        word1, word2 = pair
        if not len(word1) == len(word2):
            return False
        word1 = word1.lower()
        word2 = word2.lower()
        if word1 == word2:
            return False
        if not (word1 in self.corpus and word2 in self.corpus):
            return False
        if letters:
            in_letters = True 
            for letter in word1:
                if letter not in letters:
                    in_letters = False
                    break
            return sorted(word1) == sorted(word2) and in_letters
        else:
            return sorted(pair[0]) == sorted(pair[1])

    def get_all_anagrams(self, letters: list[str] | None = None) -> set[str]:
        """
        Finds all anagrams that can be formed using the given letters. If no letters are provided
        or if the letters list is empty, returns all words from the corpus that can form an anagram pair.

        Args:
            letters (list[str], optional): A list of letters to form anagrams. Defaults to None.

        Returns:
            set[str]: A set of all valid anagrams.

        Examples:
        >>> explorer = AnagramHelper(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> explorer.get_all_anagrams(["l", "i", "s", "t", "e", "n"]) == {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> explorer.get_all_anagrams() == {'listen', 'silent', 'enlist', 'inlets', 'stone', 'tones'}
        True
        >>> explorer.get_all_anagrams(["a", "p", "p", "l", "e"])
        set()
        """
        anagrams: set[str] = set({})
        if not letters: 
            for value in self.lookup_dict.values():
                if len(value) > 1:
                    anagrams.update(value)
            return anagrams
        for r in range(3,len(letters)+1):
            combos = combinations(letters, r)
            for combo in combos:
                query = self.generate_hash("".join(combo))
                if query not in self.lookup_dict:
                    continue
                result = self.lookup_dict[query]
                if len(result) > 1:
                    anagrams.update(result)

        return anagrams
        # YOUR CODE GOES HERE

    def get_words_with_most_anagrams(self, letters: list[str] = None) -> set[str]:
        """
        Generates a set of words which form the largest number of anagram combinations within self.__corpus 
        The returned set contains all words for each anagram group that produces the maximum number of anagrams.
        If a list of letters is provided, the search is restricted to anagrams that can be formed from those letters.

        Args:
            letters (list[str], optional): A list of letters to form anagrams. Defaults to None.

        Returns:
            set[str]: A set of words that form the most anagrams.

        Examples:
        >>> explorer = AnagramHelper(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> explorer.get_words_with_most_anagrams(["l", "i", "s", "t", "e", "n"]) == {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> explorer.get_words_with_most_anagrams() == {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> explorer.get_words_with_most_anagrams(["a", "p", "p", "l", "e"])
        set()
        """

        max_words: set[str] = set({})
        max_len = 0
        if letters:
            for r in range(3,len(letters)+1):
                combos = combinations(letters, r)
                for combo in combos:
                    query = self.generate_hash("".join(combo))
                    if query not in self.lookup_dict:
                        continue
                    result = self.lookup_dict[query].copy()
                    # `print(f"query {query}", end="   ")
                    # `# print(f"result {result}")
                    # `print(max_words, max_len)
                    if len(result) > 1 and len(result) > max_len:
                        # print(f"words {result} more than {max_len}")
                        max_words = result
                        max_len = len(result)
                    elif len(result) == max_len:
                        # print(f"words {result} equal to {max_len}")
                        max_words.update(result)
            return max_words

        for key, words_ref in self.lookup_dict.items():
            # TODO: make sure words is a value not reference
            words = words_ref.copy()
            if len(words) > 1 and len(words) > max_len:
                # print(f"words {words} more than {max_len}")
                max_words = words
                max_len = len(words)
            elif len(words) == len(max_words):
                # print(f"words {words} equal to {max_len}")
                max_words.update(words)

        return max_words

    def get_words_with_no_anagrams(self, letters: list[str] | None = None) -> set[str]:
        """
        Finds all words in the corpus that do not form any anagram pairs with any other word.

        Returns:
            set[str]: A set of words from the corpus that have no anagrams.

        Examples:
        >>> explorer = AnagramHelper(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> explorer.get_words_with_no_anagrams() == {'unique'}
        True
        >>> explorer = AnagramHelper(["rat", "tar", "art", "stop", "tops", "pots", "spot", "post"])
        >>> explorer.get_words_with_no_anagrams()
        set()
        >>> explorer = AnagramHelper(["apple", "banana", "carrot"])
        >>> explorer.get_words_with_no_anagrams() == {'apple', 'banana', 'carrot'}
        True
        """
        words: set[str] = set()
        anagrams = self.get_all_anagrams(letters)
        difference = set(self.corpus) - anagrams
        return difference

        # if not letters: 
        #     for value in self.lookup_dict.values():
        #         if len(value) > 1:
        #             words.update(value)
        #     return words 
        # for r in range(3,len(letters)+1):
        #     combos = combinations(letters, r)
        #     for combo in combos:
        #         query = self.generate_hash("".join(combo))
        #         if query not in self.lookup_dict:
        #             continue
        #         result = self.lookup_dict[query]
        #         if len(result) > 1:
        #             words.update(result)

        # return words 

    def get_anas(self, letters: list[str]):
        anagrams = {}
        for r in range(3, len(letters) + 1):
            combos = combinations(letters, r)
            for combo in combos:
                query = self.generate_hash(''.join(combo))
                if query in self.lookup_dict:
                    anagrams[query] = self.lookup_dict[query]
        return anagrams 

    def get_highest_possible_score(self, letters: list[str] | None = None) -> tuple[int, list[str]]:
        """
        Calculates the highest score possible for a given collection of letters.

        Args:
            letters (list[str]): A list of letters to form anagrams.

        Returns:
            tuple: (The highest score: int, letters which produce the highest score: list[str])

        Examples:
        >>> explorer = AnagramHelper(["listen", "silent", "enlist", "inlets", "stone", "tones"])
        >>> explorer.get_highest_possible_score(["l", "i", "s", "t", "e", "n"]) == (24, ['l', 'i', 's', 't', 'e', 'n'])
        True
        >>> explorer.get_highest_possible_score(["s", "t", "o", "n", "e"]) == (3, ["s", "t", "o", "n", "e"])
        True
        >>> explorer.get_highest_possible_score(["a", "p", "p", "l", "e"]) ==  (0, ["a", "p", "p", "l", "e"])
        True
        """
        if len(letters) < 3:
            return (0, letters)

        score = 0
        used = []
        anagrams = self.get_anas(letters)

        for query, anagram_ls in anagrams.items():
            if len(anagram_ls) > 1:
                current_letters = sorted(list(''.join(query)))
                if current_letters not in used:
                    score += (len(current_letters) - 2) * math.comb(len(anagram_ls), 2)
                    used.append(current_letters)

        return (score, letters)

if __name__ == "__main__":

    #print("Demonstrating AnagramHelper functionality")

    simple_corpus = [
        "listen", "silent", "enlist", "inlets", "stone", "tones", "note", "tone", "rat", "tar", "art",
        "stop", "pots", "tops", "opt", "spot", "post", "unique", "apple", "banana", "carrot"
    ]
    no_anagrams_corpus = [
            "listen", "silent", "enlist", "inlets", "stone", "tones", "unique", "apple", "banana",
            "carrot", "rat", "tar", "art", "stop", "pots", "tops", "top", "pot", "tax"
        ]
    # Create an instance of AnagramHelper based on the words in simple_corpus
    # explorer = AnagramHelper(get_valid_word_list())
    # explorer.build_lookup_dict()
    # print(explorer.lookup_dict)
    # print(explorer.is_valid_anagram_pair(("tap", "pat")))
    # letters = ["p", "o", "t", "s", "r", "i", "a"]
    # letters1 = letters1 = ["a","b","e","d","l"]
    # letter_choices = ["p", "o", "t", "s", "r", "i", "a"]
    # # letter_choices =[["p", "o", "t", "s", "r", "i", "a"],
    # #                      ["p", "o", "t", "s"],
    # #                      [],
    # #                      ["x", "y", "z"]
    # #                     ]
    explorer = AnagramHelper(get_valid_word_list())
    # score=explorer.get_highest_possible_score(letter_choices)
    # print(f"highest possible score is {score}")
    print(explorer.get_highest_possible_score(["l", "i", "s", "t", "e", "n"]))

    # corpus = ["abed", "abled", "bade", "baled", "bead", "blade"]
    # explorer = AnagramHelper(corpus)
    # actual = explorer.get_words_with_most_anagrams()
    # print(f"get the word with the most anagrams in {corpus}")
    # expected = {"abed", "bade", "bead", "abled", "baled", "blade"}
    # print(f"actual: {actual}")
    # print(f"expected: {expected}")

    # letters = ["p", "o", "l", "s", "r", "i", "o"] # double letter: o
    # explorer = AnagramHelper(get_valid_word_list()) 
    # actual = explorer.get_words_with_most_anagrams(letters)
    # print("in main:")
    # print(explorer.lookup_dict[('l', 'o', 'p')])
    # expected = {'loops', 'pools', 'sloop', 'spool'}
    # print(f"actual: {actual}")
    # print(f"expected: {expected}")

 
    # corpus = ["abed", "allergy", "amen", "anew", "angel", "tap", "treadle"]
    # explorer = AnagramHelper(corpus)        
    # actual = explorer.get_words_with_most_anagrams()
    # expected = set()
    # print(f"the words with most anagrams for the corpus {corpus} is")
    # print(f"actual: {actual}")
    # print(f"expected: {expected}")


    #pair =("pot", "pot")
    # print(explorer.is_valid_anagram_pair(pair, letters))
#    print("all anagrams")
#    print(explorer.get_all_anagrams(letters1))
#    print("expected:")
#    print("expected = {'bead', 'dab', 'bade', 'lade', 'lead', 'bad', 'ale', 'dal', 'bed', 'bale','deal', 'lad', 'deb', 'abel', 'able', 'dale', 'abed', 'elba', 'lea'}")
#
    # no_anagrams = AnagramHelper(no_anagrams_corpus)
    # letters = ["u", "n", "i", "q", "u", "e"]
    # print(f"All words with no anagrams given {letters}")
    # print(no_anagrams.get_words_with_no_anagrams(letters))
     # print(f"expected {set(no_anagrams_corpus)}")
    # print(explorer.get_highest_possible_score(['a','p','p','l','e']))
    # print(explorer.get_highest_possible_score(["l", "i", "s", "t", "e", "n"]))
    # print(explorer.get_highest_possible_score(["a", "p", "p", "l", "e"]))
   # new_explorer = AnagramHelper(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
   # print("most anagrams:")
   # print(new_explorer.lookup_dict)
   # print(new_explorer.get_words_with_most_anagrams(["a", "p", "p", "l", "e"]))
   # 

    #letters = ["l", "i", "s", "t", "e", "n"]
    #print("\nGet all anagrams for the letters:", letters)
    #print("Anagrams:", explorer.get_all_anagrams(letters))

    #print("\nGet all words from the corpus that can form an anagram pair:")
    #print("Anagrams:", explorer.get_all_anagrams())

    # letters = ["s", "t", "o", "n", "e"]
    # print("\nFind the set of letters that forms the most anagrams:", letters)
    # print("Most anagrams:", explorer.get_words_with_most_anagrams(letters))

    #word_pair = ("listen", "silent")
    #print("\nCheck if two words form a valid anagram pair:", word_pair)
    #print("Is valid anagram pair:", explorer.is_valid_anagram_pair(
    #    word_pair, ["l", "i", "s", "t", "e", "n"]))

    #print("\nWords with no anagrams in the corpus:")
    #print(explorer.get_words_with_no_anagrams())

    #explorer_german = AnagramHelper(get_valid_word_list_german())
    #explorer_spanish = AnagramHelper(get_valid_word_list_spanish())

    #letters = ["l", "i", "s", "t", "e", "n", "g"]
    #print(f"Get highest possible score for {
    #      letters} in English corpus:", explorer.get_highest_possible_score(letters))
    #print(f"Get highest possible score for {
    #      letters} in German corpus:", explorer_german.get_highest_possible_score(letters))
    #print(f"Get highest possible score for {
    #      letters} in spanish corpus:", explorer_spanish.get_highest_possible_score(letters))

    #letters = ["a", "i", "s", "ñ", "e", "d", "á"]
    #print(f"Get highest possible score for {
    #      letters} in English corpus:", explorer.get_highest_possible_score(letters))
    #print(f"Get highest possible score for {
    #      letters} in German corpus:", explorer_german.get_highest_possible_score(letters))
    #print(f"Get highest possible score for {
    #      letters} in spanish corpus:", explorer_spanish.get_highest_possible_score(letters))

