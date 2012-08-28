__author__ = 'dhensche'

class Parser():

    @staticmethod
    def closure (grammar, i, x, ab, cd):
        return [(rule[0], [], rule[1], i)
                    for rule in grammar
                    if cd <> [] and cd[0] == rule[0]]

    @staticmethod
    def shift (tokens, i, x, ab, cd, j):
        return (x, ab + [cd[0]], cd[1:], j) if cd <> [] and cd[0] == tokens[i] else None

    @staticmethod
    def reductions(chart, i, x, ab, cd, j):
        return [(state[0], state[1] + [x], state[2][1:], state[3])
                    for state in chart[j]
                    if state[2] <> [] and state[2][0] == x and cd == []]

    @staticmethod
    def add_to_chart(chart, index, state):
        if state in chart[index]: return False
        else:
            chart[index].append(state)
            return True

    @staticmethod
    def parse(tokens, grammar):
        tokens = tokens + ['end_of_input_marker']
        chart = {}
        start_rule = grammar[0]
        for i in range(len(tokens) + 1):
            chart[i] = []

        start_state = (start_rule[0], [], start_rule[1], 0)
        chart[0] = [start_state]

        for i in range(len(tokens)):
            while True:
                changes = False
                for state in chart[i]:
                    x,ab,cd,j = state

                    next_states = Parser.closure(grammar, i, x, ab, cd)
                    for next_state in next_states:
                        changes = Parser.add_to_chart(chart, i, next_state) or changes

                    next_state = Parser.shift(tokens, i, x, ab, cd, j)
                    if next_state is not None:
                        changes = Parser.add_to_chart(chart, i + 1, next_state) or changes

                    next_states = Parser.reductions(chart, i, x, ab, cd, j)
                    for next_state in next_states:
                        changes = Parser.add_to_chart(chart, i, next_state) or changes

                if not changes:
                    break

        accepting_state = (start_rule[0], start_rule[1], [], 0)

        for i in range(len(chart.keys())):
            print '== chart %s' % i
            for state in chart[i]:
                print '\t %s -> %s . %s from %s' % (state[0], ''.join(state[1]), ''.join(state[2]), state[3])
        return accepting_state in chart[len(tokens) - 1]

grammar1 = [
    ('S', ['P']),
    ('P', ['(', 'P', ')']),
    ('P', [])
]

tokens1 = [char for char in '(())']
print Parser.parse(tokens1, grammar1)

grammar2 = [
    ('S', ['id', '(', 'OPTARGS', ')']),
    ('OPTARGS', ['ARGS']),
    ('OPTARGS', []),
    ('ARGS', ['exp', ',', 'ARGS']),
    ('ARGS', ['exp'])
]

tokens2 = ['id', '(', 'exp', ',', 'exp', ')']
print Parser.parse(tokens2, grammar2)