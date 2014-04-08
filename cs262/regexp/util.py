from collections import deque

__author__ = 'dhensche'


class State:
    def __init__(self, state_id):
        self.state_id = state_id
        self.transitions = {}

    def add_transition(self, elem, next_state):
        next_states = self.transitions.get(elem, [])
        self.transitions[elem] = next_states + [next_state]

    def __repr__(self):
        result = []
        for (elem, next_states) in self.transitions.iteritems():
            for next_state in next_states:
                result += [str(self.state_id) + '--' + str(elem) + '->' + str(next_state.state_id)]
        return '\n'.join(result)


def re_to_fa(regexp):
    postfix_re = re_to_postfix(regexp)
    nfa_table = []
    allowable_characters = []
    counter = 0

    for elem in postfix_re:
        if elem == CONCATENATE:
            e2 = nfa_table.pop()
            e1 = nfa_table.pop()
            e1[-1].add_transition(EPSILON, e2[0])
            e1 += e2
            nfa_table.append(e1)
        elif elem == ALTERNATE:
            e2 = nfa_table.pop()
            e1 = nfa_table.pop()
            counter += 1
            start = State(counter)
            counter += 1
            end = State(counter)
            start.add_transition(EPSILON, e2[0])
            start.add_transition(EPSILON, e1[0])
            e1[-1].add_transition(EPSILON, end)
            e2[-1].add_transition(EPSILON, end)
            e2.append(end)
            e1.appendleft(start)
            e1 += e2
            nfa_table.append(e1)
        elif elem == ZERO_OR_MORE:
            e1 = nfa_table.pop()
            e1[0].add_transition(EPSILON, e1[-1])
            e1[-1].add_transition(EPSILON, e1[0])
            nfa_table.append(e1)
        elif elem == ONE_OR_MORE:
            e1 = nfa_table.pop()
            e1[-1].add_transition(EPSILON, e1[0])
            nfa_table.append(e1)
        elif elem == ZERO_OR_ONE:
            e1 = nfa_table.pop()
            e1[0].add_transition(EPSILON, e1[-1])
            nfa_table.append(e1)
        else:
            counter += 1
            s0 = State(counter)
            counter += 1
            s1 = State(counter)
            s0.add_transition(elem, s1)
            nfa_table.append(deque([s0]))
            allowable_characters.append(elem)

    starting_state = nfa_table[0][0].state_id
    accepting_state = nfa_table[0][-1].state_id
    return nfa_table, allowable_characters, starting_state, accepting_state


class Operator:
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return str(self.s)

ALTERNATE = Operator('|')
CONCATENATE = Operator('@')
ZERO_OR_MORE = Operator('*')
ONE_OR_MORE = Operator('+')
ZERO_OR_ONE = Operator('?')
EPSILON = Operator('~')

operators = {ALTERNATE: 1,
             CONCATENATE: 2,
             ZERO_OR_MORE: 3,
             ONE_OR_MORE: 3,
             ZERO_OR_ONE: 3}
unary_ops = {ZERO_OR_ONE, ZERO_OR_MORE, ONE_OR_MORE}
binary_ops = {ALTERNATE}


def re_to_postfix(regexp):
    explicit = explicitly_concatenate(regexp)
    result = []
    stack = []

    for char in explicit:
        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()
        elif char in operators:
            char_precedence = precedence(char)
            while stack and stack[-1] != '(' and precedence(stack[-1]) > char_precedence:
                result.append(stack.pop())

            if stack and char_precedence == precedence(stack[-1]):
                result.append(stack.pop())
                stack.append(char)
            else:
                if char in unary_ops:
                    result.append(char)
                else:
                    stack.append(char)
        else:
            result.append(char)

    while stack:
        result.append(stack.pop())
    return result


def precedence(char):
    return operators.get(char, 4)


def explicitly_concatenate(regexp):
    result = []
    prev = None
    left_no_concat = {')'}.union(binary_ops).union(unary_ops)
    right_no_concat = {'('}.union(binary_ops)
    for char in regexp:
        if char == '*':
            char = ZERO_OR_MORE
        elif char == '+':
            char = ONE_OR_MORE
        elif char == '?':
            char = ZERO_OR_ONE
        elif char == '|':
            char = ALTERNATE
        #if prev == '\\':
            #result[-1] = result[-1] + char
        # based on https://www.ssucet.org/pluginfile.php/2041/mod_resource/content/1/13-regextodfa/index.html#slide-24
        if prev is not None and prev not in right_no_concat and char not in left_no_concat:
            result += [CONCATENATE, char]
        else:
            result += [char]
        prev = char
    return result


print re_to_fa('(adb)?|c')