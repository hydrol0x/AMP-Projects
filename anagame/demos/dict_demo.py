if __name__ == "__main__":
   #Dictionaries use a key-value lookup pairing
   prime_lookup = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13,
      'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43, 
      'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79, 
      'w': 83, 'x': 89, 'y': 97, 'z': 101 }

   print("\n**************Accessing elements in a dictionary********************")
   print(f"prime_lookup['c']:{prime_lookup['c']}")
   print(f"All the keys in a dictionary: {list(prime_lookup.keys())}") 
   print(f"All the values in a dictionary: {list(prime_lookup.values())}") 
   print(f"All the (key, value) pairs in a dictionary: {list(prime_lookup.values())}") 
   print("Dictionary items by iterating over dictionary keys to find values:")
   for k in prime_lookup:
      print(k, prime_lookup[k], end=" ")
   print("Dictionary items by iterating over dictionary items:")
   for k, v in prime_lookup.items():
      print(k, v, end=" ")

   print("\n**************Updating a dictionary********************")
   print("Inserting a new element in a dictionary:")
   prime_lookup['alpha'] = 103
   print(f"{prime_lookup}")
   print("Removing an element from a dictionary:")
   removed_item = prime_lookup.pop('alpha') # Removing an entry from a dictionary
   print(f"{removed_item} was removed from the dictionary.")
   print(f"{prime_lookup}")
   print("Updating an existing key, value pair in a dictionary:")
   prime_lookup['a'] = 1 #Updating an existing value
   print(f"{prime_lookup}")
   print("Deleting a key, value pair in a dictionary:")
   del prime_lookup['a'] #Deleting an entry without returning what was deleted
   print(f"{prime_lookup}")
