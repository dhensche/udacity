import random

__author__ = 'Derek'
#
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the absolute value of the difference
# between each element in L and x: SUM_{i=0}^{n-1} |L[i] - x|
# 
# Your code should run in Theta(n) time
#

def partition(L, v):
    P_f, P_l = [], []
    for val in L:
        if val < v: P_f += [val]
        elif val > v: P_l += [val]

    return P_f, [v], P_l

# Runs in Theta(n) time -- from class
def top_k(L, k):
    v = L[random.randrange(len(L))]
    left, middle, right = partition(L, v)
    if len(left) == k: return left
    if len(left) + 1 == k: return left + middle
    if len(left) > k: return top_k(left, k)
    return left + middle + top_k(right, k - len(left) - 1)

# max runs in Theta(n) time and so does top_k so Theta(n + n) == Theta(n)
def minimize_absolute(L):
    midpoint = len(L)/2 if len(L) % 2 == 0 else len(L)/2 + 1
    return max(top_k(L, midpoint))

print minimize_absolute([2, 2, 3, 4])
