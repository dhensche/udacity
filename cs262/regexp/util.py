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


class Token:
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return str(self.s)

    def match(self, char):
        return char == self.s


class WildCardToken(Token):
    def __init__(self):
        Token.__init__(self, 'ANY')

    def match(self, char):
        return True


class CharacterClassToken(Token):
    digits = {c for c in '0123456789'}
    spaces = {c for c in '\t\n\f\r '}
    alpha_digits = {c for c in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'}

    def __init__(self, characters, inverted=False):
        Token.__init__(self, characters)
        self.characters = characters
        self.inverted = inverted

    def match(self, char):
        return not self.inverted != char in self.characters


class RegExRepr:
    DigitClass = CharacterClassToken(CharacterClassToken.digits)
    NonDigitClass = CharacterClassToken(CharacterClassToken.digits, inverted=True)
    WordClass = CharacterClassToken(CharacterClassToken.alpha_digits)
    NonWordClass = CharacterClassToken(CharacterClassToken.alpha_digits, inverted=True)
    WhitespaceClass = CharacterClassToken(CharacterClassToken.spaces)
    NonWhitespaceClass = CharacterClassToken(CharacterClassToken.spaces, inverted=True)
    Alternate = Token('|')
    Concatenate = Token('@')
    ZeroOrMore = Token('*')
    OneOrMore = Token('+')
    ZeroOrOne = Token('?')
    Backslash = Token('\\')
    Epsilon = Token('~')

    # Used strictly in translating to something my re_to_nfa can understand
    Wildcard = WildCardToken()

    operators = {Alternate: 1,
                 Concatenate: 2,
                 ZeroOrMore: 3,
                 OneOrMore: 3,
                 ZeroOrOne: 3}
    unary_ops = {ZeroOrOne, ZeroOrMore, OneOrMore}
    binary_ops = {Alternate}

    def __init__(self, regexp):
        self.regexp = regexp
        self.tokens = self.__tokenize()
        self.postfix = self.__postfix()
        print self.tokens

    def __tokenize(self):
        tokens = []
        prev = None
        left_no_concat = {')'}.union(RegExRepr.binary_ops).union(RegExRepr.unary_ops)
        right_no_concat = {'('}.union(RegExRepr.binary_ops)
        for char in self.regexp:
            if prev is not None and prev == RegExRepr.Backslash:
                tokens.pop()
                if tokens[-1] == RegExRepr.Concatenate:
                    tokens.pop()
                if char == 'd':
                    char = RegExRepr.DigitClass
                elif char == 'D':
                    char = RegExRepr.NonDigitClass
                elif char == 'w':
                    char = RegExRepr.WordClass
                elif char == 'W':
                    char = RegExRepr.NonWordClass
                elif char == 's':
                    char = RegExRepr.WhitespaceClass
                elif char == 'S':
                    char = RegExRepr.NonWhitespaceClass
                else:
                    char = Token(char)
            else:
                if char == '*':
                    char = RegExRepr.ZeroOrMore
                elif char == '+':
                    char = RegExRepr.OneOrMore
                elif char == '?':
                    char = RegExRepr.ZeroOrOne
                elif char == '|':
                    char = RegExRepr.Alternate
                elif char == '.':
                    char = RegExRepr.Wildcard
                elif char == '\\':
                    char = RegExRepr.Backslash
                else:
                    char = Token(char)

            # https://www.ssucet.org/pluginfile.php/2041/mod_resource/content/1/13-regextodfa/index.html#slide-24
            if prev is not None and prev not in right_no_concat and char not in left_no_concat:
                tokens += [RegExRepr.Concatenate, char]
            else:
                tokens += [char]
            prev = char
        return tokens

    def __postfix(self):
        result = []
        stack = []

        for token in self.tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack[-1] != '(':
                    result.append(stack.pop())
                stack.pop()
            elif token in RegExRepr.operators:
                char_precedence = RegExRepr.precedence(token)
                while stack and stack[-1] != '(' and RegExRepr.precedence(stack[-1]) > char_precedence:
                    result.append(stack.pop())

                if stack and char_precedence == RegExRepr.precedence(stack[-1]):
                    result.append(stack.pop())
                    stack.append(token)
                else:
                    if token in RegExRepr.unary_ops:
                        result.append(token)
                    else:
                        stack.append(token)
            else:
                result.append(token)

        while stack:
            result.append(stack.pop())
        return result

    def to_nfa(self):
        nfa_table = []
        counter = 0

        for elem in self.postfix:
            if elem == RegExRepr.Concatenate:
                e2 = nfa_table.pop()
                e1 = nfa_table.pop()
                e1[-1].add_transition(RegExRepr.Epsilon, e2[0])
                e1 += e2
                nfa_table.append(e1)
            elif elem == RegExRepr.Alternate:
                e2 = nfa_table.pop()
                e1 = nfa_table.pop()
                counter += 1
                start = State(counter)
                counter += 1
                end = State(counter)
                start.add_transition(RegExRepr.Epsilon, e2[0])
                start.add_transition(RegExRepr.Epsilon, e1[0])
                e1[-1].add_transition(RegExRepr.Epsilon, end)
                e2[-1].add_transition(RegExRepr.Epsilon, end)
                e2.append(end)
                e1.appendleft(start)
                e1 += e2
                nfa_table.append(e1)
            elif elem == RegExRepr.ZeroOrMore:
                e1 = nfa_table.pop()
                e1[0].add_transition(RegExRepr.Epsilon, e1[-1])
                e1[-1].add_transition(RegExRepr.Epsilon, e1[0])
                nfa_table.append(e1)
            elif elem == RegExRepr.OneOrMore:
                e1 = nfa_table.pop()
                e1[-1].add_transition(RegExRepr.Epsilon, e1[0])
                nfa_table.append(e1)
            elif elem == RegExRepr.ZeroOrOne:
                e1 = nfa_table.pop()
                e1[0].add_transition(RegExRepr.Epsilon, e1[-1])
                nfa_table.append(e1)
            else:
                counter += 1
                s0 = State(counter)
                counter += 1
                s1 = State(counter)
                s0.add_transition(elem, s1)
                nfa_table.append(deque([s0, s1]))

        starting_state = nfa_table[0][0].state_id
        accepting_state = nfa_table[0][-1].state_id
        return nfa_table, starting_state, accepting_state

    @staticmethod
    def precedence(char):
        return RegExRepr.operators.get(char, 4)

print RegExRepr('a\w+b').to_nfa()
print len(CharacterClassToken.alpha_digits)