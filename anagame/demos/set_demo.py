if __name__ == "__main__":
    print("------Creating Sets-----")
    set1 = {} #This makes a dictionary, not a set
    set1 = {"A"} #This makes a set
    set2 = set()
    list1 = ["A", "B", "B", "C"]
    set3 = set(list1)
    set4 = set3.copy()
    print(set1)
    print(set2)
    print(set3)
    print(set4)

    print("------Adding and Removing Elements in a Set-----")
    anagrams = {"art", "rat"}  #{"art", "rat"}
    print(anagrams)
    anagrams.add("tar")    #{"tar","art", "rat"}
    print(anagrams)
    anagrams.add("art")    #{"tar","art", "rat"}
    print(anagrams)
    anagrams.remove("art") #{"tar","rat"}
    print(anagrams)
    print(len(anagrams)) #2

    print("------Combigning and Comparing Sets-----")
    A = {1,2,3,4,5}
    A2 = {1,5,3,4,2}
    B = {3,4,5}
    print(A==A2)
    print(A==B)
    print(A.union(B))
    print(A.intersection(B))
    print(A.difference(B))
    print(B.difference(A))
    print(A.symmetric_difference(B))
    print(B.symmetric_difference(A))
    print(A.issubset(B))