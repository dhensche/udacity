__author__ = 'dhensche'

# -----------------
# User Instructions
#
# This homework deals with anagrams. An anagram is a rearrangement
# of the letters in a word to form one or more new words.
#
# Your job is to write a function anagrams(), which takes as input
# a phrase and an optional argument, shortest, which is an integer
# that specifies the shortest acceptable word. Your function should
# return a set of all the possible combinations of anagrams.
#
# Your function should not return every permutation of a multi word
# anagram: only the permutation where the words are in alphabetical
# order. For example, for the input string 'ANAGRAMS' the set that
# your function returns should include 'AN ARM SAG', but should NOT
# include 'ARM SAG AN', or 'SAG AN ARM', etc...

def anagrams(phrase, shortest=2):
    """Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words
    have length >= shortest. Phrases in answer must have words in
    lexicographic order (not all permutations)."""
    letters = phrase.replace(' ', '')
    anagram = anagram_solver(letters, shortest)
    return anagram
    # your code here


anagram_cache = dict()
def anagram_solver(all_letters, min_length=2):
    results = set()
    def helper(letters, t_results):
        if len(t_results) > 0:
            key = tuple(sorted(letters))
            if key in anagram_cache:
                for permutation in anagram_cache[key]:
                    results.add(' '.join(sorted(t_results | set(permutation.split(' ')))))
                return
            else:
                anagram_cache[key] = anagram_solver(letters, min_length)
        for word in find_words(letters, min_length):
            new_letters = removed(letters, word)

            if len(letters) == (len(new_letters) + len(word)):
                if len(new_letters) is 0:
                    results.add(' '.join(sorted(t_results | set([word]))))
                    return
                else:
                    helper(new_letters, t_results | set([word]))

    helper(all_letters, set())
    return results

# ------------
# Helpful functions
#
# You may find the following functions useful. These functions
# are identical to those we defined in lecture.

def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

word_cache = dict()

def find_words(letters, min_length=1):
    key = tuple(sorted(letters))
    if key in word_cache: return word_cache[key]
    word_cache[key] = extend_prefix('', letters, set(), min_length)
    return word_cache[key]

def extend_prefix(pre, letters, results, min_length=1):
    if pre in WORDS and len(pre) >= min_length: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            extend_prefix(pre+L, letters.replace(L, '', 1), results, min_length)
    return results

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words.txt')

# ------------
# Testing
#
# Run the function test() to see if your function behaves as expected.

def test():
    assert 'DOCTOR WHO' in anagrams('TORCHWOOD')
    assert 'BOOK SEC TRY' in anagrams('OCTOBER SKY')
    assert 'SEE THEY' in anagrams('THE EYES')
    assert 'LIVES' in anagrams('ELVIS')
    assert anagrams('PYTHONIC') == set([
        'NTH PIC YO', 'NTH OY PIC', 'ON PIC THY', 'NO PIC THY', 'COY IN PHT',
        'ICY NO PHT', 'ICY ON PHT', 'ICY NTH OP', 'COP IN THY', 'HYP ON TIC',
        'CON PI THY', 'HYP NO TIC', 'COY NTH PI', 'CON HYP IT', 'COT HYP IN',
        'CON HYP TI'])
    return 'tests pass'

print test()
