"""
Inputs: corpus (per round), letters (per turn), guesses (per turn updated)

Outputs : valid_guesses [] , invalid_guesses [], unique_guessed Set(), not_guessed Set(), score , max_score, accuracy, skill
"""
import time
import random
from collections import Counter

try:
    from AnagramHelper import AnagramHelper
except ModuleNotFoundError:
    print("AnagramHelper.py is not found.")
    pass

from valid_anagame_words import get_valid_word_list

guess = tuple[str, str]
game_time = float | None

class AnaGame:
    def __init__(self, valid_words: list[str]):
        self.helper=AnagramHelper(valid_words)
        self.guesses: list[guess]= []
        self.round_score: int = 0
        self.high_score: int = 0
        self.timer_start: game_time = None
        # self.ROUND_TIME_SEC = 60 * 5 
        self.ROUND_TIME_SEC: float = 30
        self.current_letters: list[str] = [] 
        self.available_anagrams: set[str] = set() 
        self.hint_cost = 0 # deducts for using a hint

    def parse_guess(self, guess_str: str) -> guess | str | None:
        guess_str = guess_str.strip().lower()
        if guess_str == 'hint':
            return 'hint'
        try:
            word1, word2 = guess_str.split()
            return (word1, word2)
        except ValueError:
            return None
        
    def get_user_guess(self) -> guess | str | None:
        raw_guess = input("What's youre guess (word1 word2) or type 'hint' to recieve a hint")
        guess = self.parse_guess(raw_guess)
        return self.parse_guess(raw_guess)

    def init_round(self) -> None:
        self.round_score = 0
        self.guesses = []
        self.timer_start = time.time()
        self.current_letters = self.generate_random_letters(7)
        print(f"letters for this round are: {' | '.join(self.current_letters)}")
        self.available_anagrams = self.helper.get_all_anagrams(self.current_letters)
        print(f"highest possible score for this round: {self.helper.get_highest_possible_score(self.current_letters)}")

    def generate_random_letters(self, num_letters: int) -> list[str]:
        all_corpus_letters = [char for word in self.helper.corpus for char in word]
        if len(all_corpus_letters) < num_letters:
            return list(set(all_corpus_letters)) 
        return random.sample(all_corpus_letters, num_letters)

    def is_time_up(self) -> bool:
        # time.time() is the time in seconds
        if self.timer_start:
            time_delta = time.time() - self.timer_start
            return time_delta > self.ROUND_TIME_SEC
        return False

    def handle_hint(self):
       if self.round_score < self.hint_cost:
           print(f"You don't have enough score to get a hint! You need at least {self.hint_cost} points.")
           return

       self.round_score -= self.hint_cost
       print(f"Hint cost {self.hint_cost} points. Your new score is {self.round_score}.")

       unguessed_anagram_words = set()
       all_possible_anagrams_for_letters = self.helper.get_all_anagrams(self.current_letters)

       for potential in all_possible_anagrams_for_letters:
           guessed = False
           for guessed_pair in self.guesses:
               if potential == guessed_pair[0] or potential == guessed_pair[1]: # already guessed,hint would be redundant
                   guessed = True
                   break
           if not guessed:
               unguessed_anagram_words.add(potential)
       
       if not unguessed_anagram_words:
           print("You found all the words!")
           return

       possible_hints = set()
       for word in unguessed_anagram_words:
           hash = self.helper.generate_hash(word)
           if hash in self.helper.lookup_dict:
               possibilities = self.helper.lookup_dict[hash]
               
               unguessed_in_group = possibilities.intersection(unguessed_anagram_words)
               if len(unguessed_in_group) > 1: # we have a hint to offer
                   possible_hints.add(word)
               elif len(unguessed_in_group) == 1 and len(possibilities) > 1:
                   possible_hints.add(word)
       
       if not possible_hints:
           print("No more hints for this set!")
           return

       word_to_hint = random.choice(list(possible_hints))

       print(f"Hint: An unguessed anagram starts with the letter '{word_to_hint[0]}'. and has length {len(word_to_hint)}")
       

    def get_word_score(self, word:str) -> int:
        if len(word) < 3:
            return 0
        return len(word) - 2 
        
    def play_turn(self) -> None:
        while not self.is_time_up():
            guess_input = self.get_user_guess()

            if guess_input == 'hint':
                self.handle_hint()
                continue  

            if not guess_input:
                print("please enter guess in a valid format (word1 word2).")
                continue

            if not isinstance(guess_input, tuple) or len(guess_input) != 2:
                print("Please enter two words separated by a space.")
                continue

            word1, word2 = guess_input
            lower_word1, lower_word2 = word1.lower(), word2.lower()
            current_guess_tuple = (lower_word1, lower_word2)

            if current_guess_tuple in self.guesses or (lower_word2, lower_word1) in self.guesses:
                print("You already guessed that! Don't get lazy.")
                continue

            letters_counter = Counter(self.current_letters)
            word1_counter = Counter(lower_word1)
            word2_counter = Counter(lower_word2)

            can_form_word1 = all(word1_counter[char] <= letters_counter[char] for char in word1_counter)
            can_form_word2 = all(word2_counter[char] <= letters_counter[char] for char in word2_counter)

            if not (can_form_word1 and can_form_word2):
                print("Your guess contains letters not available in this round or uses too many of a letter. Try again.")
                continue

            if self.helper.is_valid_anagram_pair(current_guess_tuple, self.current_letters):
                self.guesses.append(current_guess_tuple)
                self.round_score += self.get_word_score(lower_word1)
                print(f"Correct! Your score is {self.round_score}")
                
                self.available_anagrams.discard(lower_word1)
                self.available_anagrams.discard(lower_word2)

            else:
                print("invalid pair or not in dictionary! Try again.")
                continue
        return


if __name__ == "__main__":
    game = AnaGame(get_valid_word_list())
    game_over = False

    game.init_round()
    while not game_over:
        if game.is_time_up():
            print("The game has concluded! Time's up.")
            break
        game.play_turn()
    print("\n--- Game Over ---")
    
