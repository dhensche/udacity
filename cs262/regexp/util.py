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


class EpsilonToken(Token):
    def __init__(self):
        Token.__init__(self, '~')

    def match(self, char):
        return False


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
    LeftParen = Token('(')
    RightParen = Token(')')
    Backslash = Token('\\')
    Epsilon = EpsilonToken()

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
        self.state_table, self.start, self.accept = self.__to_nfa()
        self.states = self.__collapse_table()

    def __tokenize(self):
        tokens = []
        prev = None
        left_no_concat = {RegExRepr.RightParen}.union(RegExRepr.binary_ops).union(RegExRepr.unary_ops)
        right_no_concat = {RegExRepr.LeftParen}.union(RegExRepr.binary_ops)
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
                elif char == '(':
                    char = RegExRepr.LeftParen
                elif char == ')':
                    char = RegExRepr.RightParen
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
            if token == RegExRepr.LeftParen:
                stack.append(token)
            elif token == RegExRepr.RightParen:
                while stack[-1] != RegExRepr.LeftParen:
                    result.append(stack.pop())
                stack.pop()
            elif token in RegExRepr.operators:
                char_precedence = RegExRepr.precedence(token)
                while stack and stack[-1] != RegExRepr.LeftParen and RegExRepr.precedence(stack[-1]) > char_precedence:
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

    def __to_nfa(self):
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

        return nfa_table[0], nfa_table[0][0].state_id, nfa_table[0][-1].state_id

    def __collapse_table(self):
        states = {}
        accepts = {self.accept}

        def collapse(current, transitions, final_states):
            final_paths = []
            for (token, paths) in transitions.iteritems():
                if token == RegExRepr.Epsilon:
                    for path in paths:
                        if path.state_id in final_states:
                            final_states |= {current.state_id}
                        final_paths += collapse(current, path.transitions, final_states)
                else:
                    final_paths += [(token, path.state_id) for path in paths]

            return final_paths

        for state in self.state_table:
            for (tok, next_state) in collapse(state, state.transitions, accepts):
                key = (state.state_id, tok)
                next_states = states.get(key, [])
                states[key] = next_states + [next_state]

        self.accept = accepts
        return states

    def __nfsmaccepts(self, current, visited):
        if current in self.accept:
            return ''
        elif current in visited:
            return None
        else:
            for edge, next_states in self.states.items():
                for next_state in next_states:
                    if current is edge[0]:
                        visited += [current]
                        sample_string = self.__nfsmaccepts(next_state, visited)
                        if sample_string is not None:
                            return edge[1] + sample_string
            return None

    def __nfsmtrim(self):
        """This trims off the edges that don't lead to an accepting state and any accepting states
        that are unreachable. It does this by going over the existing edges and seeing if an accepting
        state can be reached from it using nfsmaccepts. If one can be reached the edge is valid and retained,
        otherwise it is dropped from the valid edges.

        @return: trimmed edges and accepting states
        """
        new_edges = {}
        good_states = []
        for edge, next_states in self.states.iteritems():
            for next_state in next_states:
                if self.__nfsmaccepts(next_state, []) is not None:
                    if edge not in new_edges:
                        new_edges[edge] = []
                    new_edges[edge] += [next_state]
                    good_states += [next_state]

        return new_edges, [state for state in self.accept if state in good_states]

    def matches(self, haystack):
        def helper(string, current):
            if string == "":
                return current in self.accept
            else:
                for ((state, tok), paths) in self.states.iteritems():
                    if tok.match(string[0]) and state == current:
                        return any(helper(string[1:], path) for path in paths)
                    elif tok == RegExRepr.Epsilon and state == current:
                        return any(helper(string, path) for path in paths)
                return False

        return helper(haystack, self.start)

    @staticmethod
    def precedence(char):
        return RegExRepr.operators.get(char, 4)

print RegExRepr('a|b|C|D|E|F|G').matches('D')