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
        characters = frozenset(characters)
        Token.__init__(self, characters)
        self.characters = characters
        self.inverted = inverted

    def match(self, char):
        return (self.inverted and char not in self.characters) or (not self.inverted and char in self.characters)


class RegExRepr:
    Alternate = Token('|')
    Concatenate = Token('@')
    ZeroOrMore = Token('*')
    OneOrMore = Token('+')
    ZeroOrOne = Token('?')
    LeftParen = Token('(')
    RightParen = Token(')')
    LeftSBracket = Token('[')
    RightSBracket = Token(']')
    Backslash = Token('\\')

    Epsilon = EpsilonToken()
    Wildcard = WildCardToken()

    operators = {Alternate: 1,
                 Concatenate: 2,
                 ZeroOrMore: 3,
                 OneOrMore: 3,
                 ZeroOrOne: 3}
    unary_ops = {ZeroOrOne, ZeroOrMore, OneOrMore}

    escape_sequences = {
        'd': CharacterClassToken(CharacterClassToken.digits),
        'D': CharacterClassToken(CharacterClassToken.digits, inverted=True),
        'w': CharacterClassToken(CharacterClassToken.alpha_digits),
        'W': CharacterClassToken(CharacterClassToken.alpha_digits, inverted=True),
        's': CharacterClassToken(CharacterClassToken.spaces),
        'S': CharacterClassToken(CharacterClassToken.spaces, inverted=True)
    }
    left_no_concat = {RightParen, Alternate}.union(unary_ops)
    right_no_concat = {LeftParen, Alternate}

    def __init__(self, regexp):
        self.regexp = regexp
        self.tokens = self.__tokenize()
        print(self.tokens)
        self.start, self.edges, self.accepts, self.allowable_tokens = self.__parse()

    @staticmethod
    def __evaluate_class(characters):
        tokens = []
        char = characters.popleft()
        inverted = char == '^'
        if not inverted:
            characters.appendleft(char)
        prev = None
        range_open = False
        while characters:
            char = characters.popleft()
            if char == ']':
                if range_open:
                    raise SyntaxError('Unclosed range in character class')
                else:
                    return CharacterClassToken(tokens, inverted), characters
            elif char == '-' and prev:
                if isinstance(prev, CharacterClassToken):
                    raise SyntaxError('Invalid character range')
                else:
                    range_open = True
                    continue
            elif char == '\\':
                char = characters.popleft()
                char = RegExRepr.escape_sequences.get(char, Token(char))
            else:
                char = Token(char)

            if isinstance(char, CharacterClassToken):
                if range_open:
                    raise SyntaxError('Invalid character range')
                else:
                    tokens += char.characters
            else:
                if range_open:
                    start_ord = ord(prev.s)
                    end_ord = ord(char.s)
                    if start_ord > end_ord:
                        raise SyntaxError('Invalid character range')
                    else:
                        range_open = False
                        tokens += [chr(code) for code in range(start_ord + 1, end_ord + 1)]
                else:
                    tokens += [char.s]

            prev = char
        raise SyntaxError('Unclosed character class')

    def __tokenize(self):
        tokens = []
        prev = None
        characters = deque(self.regexp)
        while characters:
            char = characters.popleft()
            if char == '\\':
                char = characters.popleft()
                char = RegExRepr.escape_sequences.get(char, Token(char))
            elif char == '*':
                char = RegExRepr.ZeroOrMore
            elif char == '+':
                char = RegExRepr.OneOrMore
            elif char == '?':
                char = RegExRepr.ZeroOrOne
            elif char == '|':
                char = RegExRepr.Alternate
            elif char == '.':
                char = RegExRepr.Wildcard
            elif char == '(':
                char = RegExRepr.LeftParen
            elif char == ')':
                char = RegExRepr.RightParen
            elif char == '[':
                char, characters = RegExRepr.__evaluate_class(characters)
            else:
                char = Token(char)

            # https://www.ssucet.org/pluginfile.php/2041/mod_resource/content/1/13-regextodfa/index.html#slide-24
            if prev and tokens and prev not in RegExRepr.right_no_concat and char not in RegExRepr.left_no_concat:
                tokens += [RegExRepr.Concatenate, char]
            else:
                tokens += [char]
            prev = char

        return tokens

    def __parse(self):
        postfix = self.__postfix()
        return self.__to_dfa(*self.__to_nfa(postfix))

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

    @staticmethod
    def __to_nfa(postfix_tokens):
        nfa_table = []
        allowable_tokens = set()
        counter = 0

        for elem in postfix_tokens:
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
                allowable_tokens |= {elem}
                s0.add_transition(elem, s1)
                nfa_table.append(deque([s0, s1]))

        return nfa_table[0], nfa_table[0][0].state_id, nfa_table[0][-1].state_id, allowable_tokens

    @staticmethod
    def __to_dfa(state_table, nfa_start, nfa_accepts, allowable_tokens):
        edges = {state.state_id: state for state in state_table}
        dfa_edges = {}

        def close_over(state, visited=set()):
            if state in visited:
                return frozenset()
            epsilon_states = {state.state_id}
            for (token, paths) in state.transitions.iteritems():
                if token == RegExRepr.Epsilon:
                    for path in paths:
                        epsilon_states |= {path.state_id}
                        epsilon_states |= close_over(path, visited | {state})

            return frozenset(epsilon_states)

        def move(states, token):
            outgoing = [edges[state].transitions[token] for state in states if token in edges[state].transitions]
            return set(*outgoing) if outgoing else set()

        dfa_start = close_over(edges[nfa_start])
        dfa_states = [dfa_start]
        dfa_accepts = set()
        updated = True
        while dfa_states and updated:
            dfa_state = dfa_states.pop()
            if nfa_accepts in dfa_state:
                dfa_accepts |= {dfa_state}

            for tok in allowable_tokens:
                if (dfa_state, tok) in dfa_edges:
                    continue
                reachable = frozenset(*[close_over(out) for out in move(dfa_state, tok)])
                if reachable:
                    dfa_states += [reachable]
                    if (dfa_state, tok) not in dfa_edges:
                        dfa_edges[(dfa_state, tok)] = set()
                    dfa_edges[(dfa_state, tok)] |= reachable

        return dfa_start, dfa_edges, dfa_accepts, allowable_tokens

    def matches(self, haystack):
        def helper(string, current):
            if string == "":
                return current in self.accepts
            else:
                for ((state, tok), paths) in self.edges.iteritems():
                    if tok.match(string[0]) and state == current:
                        if helper(string[1:], paths):
                            return True
                return False

        return helper(haystack, self.start)

    @staticmethod
    def precedence(char):
        return RegExRepr.operators.get(char, 4)


print RegExRepr('\([\w\t\n]+\)').matches('(956sadfssdafjsdoifioj3489asdfoij34890adflk3409\t\n8sajiofdf7)')