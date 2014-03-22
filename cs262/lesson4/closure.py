__author__ = 'dhensche'

# Writing Closure

# We are currently looking at chart[i] and we see x => ab . cd from j

# Write the Python procedure, closure, that takes five parameters:

# grammar: the grammar using the previously described structure
#   i: a number representing the chart state that we are currently looking at
#   x: a single nonterminal
#   ab and cd: lists of many things

# The closure function should return all the new parsing states that we want to
# add to chart position i

# Hint: This is tricky. If you are stuck, do a list comphrension over the grammar rules.


def closure(grammar, i, x, ab, cd):
    """
    This works by looking at the first token after the dot (if there is any) and finding any rules in the grammar
    where the lhs matches the token. It then expands the closure over these rules by creating a next state with values
    (lhs of rule, empty list -- new rule so at the beginning, rhs of rule, i)
    @param grammar: The grammar rules to parse with
    @param i: The current number of tokens consumed
    @param x: The current non-terminal being examined
    @param ab: The tokens before the dot
    @param cd: The tokens after the dot
    @return: The next_states determined from evaluating the closure
    """
    return [(rule[0], [], rule[1], i) for rule in grammar if rule[0] == cd[0]] if len(cd) > 0 else []


grammar = [
    ("exp", ["exp", "+", "exp"]),
    ("exp", ["exp", "-", "exp"]),
    ("exp", ["(", "exp", ")"]),
    ("exp", ["num"]),
    ("t", ["I", "like", "t"]),
    ("t", [""])
]

print closure(grammar, 0, "exp", ["exp", "+"], ["exp"]) == [('exp', [], ['exp', '+', 'exp'], 0),
                                                            ('exp', [], ['exp', '-', 'exp'], 0),
                                                            ('exp', [], ['(', 'exp', ')'], 0), ('exp', [], ['num'], 0)]
print closure(grammar, 0, "exp", [], ["exp", "+", "exp"]) == [('exp', [], ['exp', '+', 'exp'], 0),
                                                              ('exp', [], ['exp', '-', 'exp'], 0),
                                                              ('exp', [], ['(', 'exp', ')'], 0),
                                                              ('exp', [], ['num'], 0)]
print closure(grammar, 0, "exp", ["exp"], ["+", "exp"]) == []
