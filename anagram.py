def isAnagram(s: str, t: str) -> bool:
    # If lengths are different, they can't be anagrams
    if len(s) != len(t):
        return False
    
    return sorted(s) == sorted(t)

print(isAnagram('anagram','anagram'))

# this is better option.
'''Why this matters
Sorting takes $O(n \log n)$ time.
Hash Map takes $O(n)$ time because we only go through the strings once.'''

def isAnagramBetterSol(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    countS, countT = {}, {}

    for i in range(len(s)):
        countS[s[i]] = 1 + countS.get(s[i], 0)
        countT[t[i]] = 1 + countT.get(t[i], 0)
    
    return countS == countT


print(isAnagramBetterSol('anagram','anagram'))