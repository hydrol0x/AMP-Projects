import itertools

if __name__ == "__main__":
  letters = list("Academy")
  print("\nPermutation: Arrangements of the elements in a list word grows at a factorial rate:")
  for i in range(1, len(letters)+1):
    word = letters[0:i]
    perms = list(itertools.permutations(word))
    print(f"{word} has {len(word)} elements and {len(perms)} permutations.")

  n = 3
  print(f"\nCombinations: All arrangements of {n} objects selected from {letters}")
  combos = list(itertools.combinations(letters, n))
  print(f"There are {len(combos)} ways to choose {n} letters from {letters} without replacement:")
  print(combos)

  print(f"\nCombination with replacement: All arrangements of {n} objects selected from {letters}")
  combos = list(itertools.combinations_with_replacement(letters, n))
  print(f"There are {len(combos)} ways to choose {n} letters from {letters} with replacement:")
  print(combos)
