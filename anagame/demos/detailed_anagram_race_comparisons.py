import tracemalloc, time
import matplotlib.pyplot as plt
import itertools

def exhaustive(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False

    permutations = list(itertools.permutations(w1))
    w2Tuple = tuple(w2)
    return w2Tuple in permutations

def checkoff(word1:str, word2:str)->bool:
    if len(word1) != len(word2):
        return False
    checkoff = list(word2)
    i = 0
    while i < len(word1):
        if word1[i] in checkoff:
            w2_index = checkoff.index(word2[i])
            checkoff[w2_index] = None
        else:
            return False
        i+=1
            
    return True

def lettercount_dict(s1: str, s2: str) -> bool:
    if len(s1) != len(s2): return False
    count = {}
    i=len(s1)-1
    while i>=0:
        if s1[i] in count: 
            count[s1[i]] = count[s1[i]]+1
            if count[s1[i]] == 0:
                del count[s1[i]]
        else:
            count[s1[i]] = 1

        if s2[i] in count: 
            count[s2[i]]=count[s2[i]]-1
            if count[s2[i]] == 0:
                del count[s2[i]]
        else:
            count[s2[i]] = -1        

        i=i-1
            
    return len(count)==0

def lettercount_xor(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    xor_result = 0
    for char in s1 + s2:
        xor_result ^= ord(char)
    return xor_result == 0

def lettercount_list(word1:str, word2:str)->bool:
    if len(word1) != len(word2):
        return False

    letterCount_w1 = [0]*26
    letterCount_w2 = [0]*26

    i=len(word1)-1
    while i>=0:
        letterCount_w1[ord(word1[i]) - 97] += 1
        letterCount_w2[ord(word2[i]) - 97] += 1
        i=i-1

    return letterCount_w1 == letterCount_w2

def sort(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False

    return sorted(word1)==sorted(word2)

def prime_hash_dict(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False
    primes = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13,
    'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43,
    'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79,
    'w': 83, 'x': 89, 'y': 97, 'z': 101 }
    
    hash1, hash2 = 1, 1
    i=len(word1)-1
    while i>=0:
        hash1*=primes[word1[i]]
        hash2*=primes[word1[i]]
        i=i-1
    return hash1 == hash2

def prime_hash_list(word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    
    hash1, hash2 = 1, 1
    i=len(word1)-1
    while i>=0:
        hash1*=primes[ord(word1[i])-97]
        hash2*=primes[ord(word1[i])-97]
        i=i-1
    return hash1 == hash2

if __name__ == "__main__":
    anagram_functions = [
        #exhaustive,
        checkoff,
        sort,
        lettercount_dict,
        lettercount_xor,
        lettercount_list,
        prime_hash_dict,
        prime_hash_list
    ]

    inputs = [
        ("eat", "ate"),
        ("tale", "late"),
        ("sneak", "snake"),
        ("listen", "silent"),
        ("allergy", "gallery"),
        ("calipers", "replicas"),
        ("cautioned", "education"),
        ("percussion", "supersonic"),
        ("calligraphy", "graphically"),
        ("snoozealarms", "alasnomorezs"),
        ("astronomers", "nomorestars"),
        ("adecimalpoint", "imadotinplace"),
        ("conversationalists", "conservationalists"),
        ("hydroxydeoxycorticosterones", "hydroxydeoxycorticosteroids"),
        ("theunitedstatesbureauoffisheries", "iraisethebasstofeedusinthefuture")
    ]
    comparison_data = {}
    comparison_data["memory"]={}
    comparison_data["compute"]={}

    for alg in anagram_functions:
        trials = 100
        compute_results = []
        memory_results = []
        #for input of increasing scale
        for pair in inputs:
            w1, w2 = pair
            #measure memory
            total_memory = 0
            for _ in range(trials):
                tracemalloc.start()
                alg(w1, w2)
                total_memory+=tracemalloc.get_traced_memory()[1]
                tracemalloc.stop()
            memory_results.append(total_memory/trials)
            
            #measure compute
            total_time=0
            for _ in range(trials):
                start = time.perf_counter()
                alg(w1, w2)
                total_time+=time.perf_counter()-start
            compute_results.append(total_time/trials)
        
        comparison_data["memory"][alg.__name__] = memory_results
        comparison_data["compute"][alg.__name__] = compute_results
    
    for label in ["memory", "compute"]:
        units = "bytes" if label == "memory" else "seconds"

        plt.xticks(rotation=20, ha='right')
        plt.ylabel(f'{label} ({units})')
        plt.title(f"is_anagram {label} comparisons")
        for alg in comparison_data[label]:
            x_labels = [str(n) for n in inputs]
            plt.plot(x_labels, comparison_data[label][alg], label = alg)
        plt.legend()
        plt.tight_layout()
        plt.show()