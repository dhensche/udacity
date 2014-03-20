__author__ = 'dhensche'


# Bonus Practice: Subsets

# This assignment is not graded and we encourage you to experiment. Learning is
# fun!

# Write a procedure that accepts a list as an argument. The procedure should
# print out all of the subsets of that list.

def expand(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


def expand_all(iterable):
    for size in range(len(iterable) + 1):
        yield [comb for comb in expand(iterable, size)]


def print_all_combinations(iterable):
    print [x for x_list in expand_all(iterable) for x in x_list]


print_all_combinations(['a','b','c'])