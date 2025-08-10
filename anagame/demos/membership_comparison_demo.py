import time
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from valid_anagame_words import get_valid_word_list # only words with 2 - 7 letters

def membership_comparison():
    all_words_list = get_valid_word_list()
    print(f"word_list is a {type(all_words_list)} with {len(all_words_list)} words in it.")

    all_words_set = set()
    for word in all_words_list:
        all_words_set.add(word)
    print(f"all_words_set is a {type(all_words_set)} with {len(all_words_set)} words in it.")

    input=["abacus", "begin", "middle", "night", "yellow", "zoom", "gjdhddsjg"]
    word_collections=[all_words_list, all_words_set]

    for word in input:
        print(f"{word}:")
        for collection in word_collections:
            start = time.perf_counter()
            if word in collection:
                stop = time.perf_counter()
                elapsed_time = (stop-start)*1000

                print(f'\tIt took {round(elapsed_time,5)}ms to find "{word}" in a {type(collection)}')
            else:
                stop = time.perf_counter()
                elapsed_time = (stop-start)*1000

                print(f'\tIt took {round(elapsed_time,5)}ms to find out that "{word}" is not present in a {type(collection)}')


def elements_in_common():

    set1 = set(range(0,10000))        # create a set with a bunch of numbers in it
    set2 = set(range(5000,20000))     # create another set with a bunch of numbers in it
    
    start = time.perf_counter()
    intersection_set = set1.intersection(set2)
    set_time = (time.perf_counter() - start)

    list1 = list(range(0,10000))      # create a list with a bunch of numbers in it
    list2 = list(range(5000,20000))   # create another list with a bunch of numbers in it
    start = time.perf_counter()
    intersection_list = []
    for e1 in list1:
        for e2 in list2:
            if e1==e2:
                intersection_list.append(e1)
    list_time = (time.perf_counter() - start)

    assert(list(intersection_set) == intersection_list), "The two intersection methods should yield the same result."
    print(f"Finding the intersection of two sets took {round(set_time, 6):.6}s")
    print(f"Finding the intersection of two lists took {round(list_time, 6):.6}s")
    print(f"Sets are {round(list_time//set_time)}x faster than lists for finding intersecting elements.")

if __name__ == "__main__":
    membership_comparison()
    print()
    elements_in_common()