if __name__ == "__main__":
    words = ['abed', 'abet', 'abets', 'abut', 'acme', 'acre', 'acres', 'actors', 'actress', 'airmen', 'alert', 'alerted', 'ales', 'aligned', 'allergy', 'alter', 'altered', 'amen', 'anew', 'angel', 'angle', 'antler', 'apt', 'bade', 'baste', 'bead', 'beast', 'beat', 'beats', 'beta', 'betas', 'came', 'care', 'cares', 'casters', 'castor', 'costar', 'dealing',
    'gallery', 'glean', 'largely', 'later', 'leading', 'learnt', 'leas','mace', 'mane', 'marine', 'mean', 'name', 'pat', 'race', 'races','recasts', 'regally', 'related', 'remain', 'rental', 'sale', 'scare','seal', 'tabu', 'tap', 'treadle', 'tuba', 'wane', 'wean']

    primeMap = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13,
        'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37,
        'm': 41, 'n': 43, 'o': 47, 'p': 53, 'q': 59, 'r': 61,
        's': 67, 't': 71, 'u': 73, 'v': 79, 'w': 83, 'x': 89,
        'y': 97, 'z': 101 }

    def primeHash(word):
        hashValue = 1
        for letter in word:
            hashValue *= primeMap[letter]
        return hashValue

    print (sorted(words , key=primeHash, reverse=False))

    #['abed', 'bade', 'bead', 'acme', 'came', 'mace', 'abet', 'beat', 'beta', 'acre', 'care', 'race', 'apt', 'pat', 'tap', 'abut', 'tabu', 'tuba', 'amen', 'mane', 'mean', 'name', 'ales', 'leas', 'sale', 'seal', 'anew', 'wane', 'wean', 'abets', 'baste', 'beast', 'beats', 'betas', 'acres', 'cares', 'races', 'scare', 'angel', 'angle', 'glean', 'alert', 'alter', 'later', 'airmen', 'marine', 'remain', 'aligned', 'dealing', 'leading', 'actors', 'castor', 'costar', 'antler', 'learnt', 'rental', 'alerted', 'altered', 'related', 'treadle', 'actress', 'casters', 'recasts', 'allergy', 'gallery', 'largely', 'regally']