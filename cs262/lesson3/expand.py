__author__ = 'dhensche'


grammar = [
    ('exp', ['exp', '+', 'exp']),
    ('exp', ['exp', '-', 'exp']),
    ('exp', ['(', 'exp', ')']),
    ('exp', ['num'])
]


def expand(tokens, grammar):
    for pos in range(len(tokens)):
        for rule in grammar:
            if rule[0] == tokens[pos]:
                yield tokens[:pos] + rule[1] + tokens[pos + 1:]


depth = 2
utterances = [['exp']]
for x in range(depth):
    for sentence in utterances:
        utterances = utterances + [i for i in expand(sentence, grammar)]

print utterances