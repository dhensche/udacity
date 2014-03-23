__author__ = 'dhensche'

# CHALLENGE: Complexity of Parsing
#
# Because every HTML webpage and bit of embedded JavaScript must be parsed
# before it can be rendered, the efficiency of parsing is of critical
# importance.
#
# In the past, computer scientists and linguists developed special
# restricted classes of grammars that could be parsed rapidly. The
# memoization approach to parsing that we used in this class is named
# Earley's Algorithm after its inventor. It can handle any context-free
# grammar, but it is not always very efficient. In fact, if the size of the
# webpage is X tokens, it can sometimes take as many as X*X*X (i.e., X
# cubed) operations to determine if the string is in the language of the
# grammar or not. That would be really bad, because it means that if the
# size of your webpage doubles, it would take 8 times longer to load!
# That's not how you build a scalable business.
#
# (Later courses on computer science theory and the analysis and complexity
# of algorithms will provide you with the tools to determine why it could
# perform X*X*X but not X*X*X*X operations in the worst case. For now,
# simply assume it is true.)
#
# Since the exact time it takes to execute a program depends on your
# particular hardware, we will measure operations. In particular, every
# time our parser has to look over our grammar rules to compute the
# closure, if there are X grammar rules we charge it for X units of work.
# Similarly, whenever our parser has to look back at chart[j] to to
# reductions, if there are Y states in chart[j] we charge it for Y units of
# work.
#
# For this problem you should define a grammar and a list of tokens
# so that parsing the tokens requires at least 2*X*X*X "work operations"
# (as defined above), where X is the number of input tokens, the number
# of grammar rules, or the size of the largest grammar rule. In addition,
# you must find a answer where X > 10 (we want to see real poor
# performance, not a small corner case on tiny input) and also where X < 50
# (to avoid overloading our grading servers).
#
# Hint 1: You can make parsing take more time by increasing the size of the
# input string, but since that also increases X, you can't solve this
# problem with that alone. We're interested in seeing worst-case
# performance in proportion to the size of the input.
#
# Hint 2: This problem is intentionally open-ended. Computer science
# involves creativity. Make up some grammars and try them out.
#
# Hint 3: It doesn't even matter if your token string is in the language of
# the grammar or not. But if it's not, our parser often finds that out
# very early, so that probably won't be the example of poor performance
# you're looking for.
#
# Hint 4: Think about the concept from class that gave us the most
# difficulty when parsing and interpreting natural languages and computer
# languages alike. If you can think of such a thing, try to put a lot of it
# in your counter-example!

# Aside from "work_count", this is just a reprint of the parsing algorithm
# from class. You can't change the parsing algorithm for this problem, so
# just skip down to the end.

work_count = 0  # track one notion of "time taken"


def addtoset(theset, index, elt):
    if not (elt in theset[index]):
        theset[index] = [elt] + theset[index]
        return True
    return False


def parse(_tokens, _grammar):
    global work_count
    work_count = 0
    _tokens = _tokens + ["end_of_input_marker"]
    chart = {}
    start_rule = _grammar[0]
    for ti in range(len(_tokens) + 1):
        chart[ti] = []
    start_state = (start_rule[0], [], start_rule[1], 0)
    chart[0] = [start_state]
    for ti in range(len(_tokens)):
        while True:
            changes = False
            for state in chart[ti]:
                # State ===   x -> a b . c d , j
                x = state[0]
                ab = state[1]
                cd = state[2]
                j = state[3]

                # Current State ==   x -> a b . c d , j
                # Option 1: For each grammar rule c -> p q r
                # (where the c's match)
                # make a next state               c -> . p q r , ti
                # English: We're about to start parsing a "c", but
                # "c" may be something like "exp" with its own
                # production rules. We'll bring those production rules in.
                next_states = [(rule[0], [], rule[1], ti)
                               for rule in _grammar if cd != [] and cd[0] == rule[0]]
                work_count = work_count + len(_grammar)
                for next_state in next_states:
                    changes = addtoset(chart, ti, next_state) or changes

                # Current State ==   x -> a b . c d , j
                # Option 2: If tokens[ti] == c,
                # make a next state               x -> a b c . d , j
                # in chart[ti+1]
                # English: We're looking for to parse token c next
                # and the current token is exactly c! Aren't we lucky!
                #  So we can parse over it and move to j+1.
                if cd != [] and _tokens[ti] == cd[0]:
                    next_state = (x, ab + [cd[0]], cd[1:], j)
                    changes = addtoset(chart, ti + 1, next_state) or changes

                # Current State ==   x -> a b . c d , j
                # Option 3: If cd is [], the state is just x -> a b . , j
                # for each p -> q . x r , l in chart[j]
                # make a new state                p -> q x . r , l
                # in chart[ti]
                # English: We just finished parsing an "x" with this token,
                #  but that may have been a sub-step (like matching "exp -> 2"
                #  in "2+3"). We should update the higher-level rules as well.
                next_states = [(jstate[0], jstate[1] + [x], (jstate[2])[1:],
                                jstate[3])
                               for jstate in chart[j]
                               if cd == [] and jstate[2] != [] and (jstate[2])[0] == x]
                work_count = work_count + len(chart[j])
                for next_state in next_states:
                    changes = addtoset(chart, ti, next_state) or changes

            # We're done if nothing changed!
            if not changes:
                break

                # Comment this block back in if you'd like to see the chart printed.
                #
                # for ti in range(len(tokens)):
                # print "== chart " + str(ti)
                # for state in chart[ti]:
                #     x = state[0]
                #     ab = state[1]
                #     cd = state[2]
                #     j = state[3]
                #     print "    " + x + " ->",
                #     for sym in ab:
                #       print " " + sym,
                #     print " .",
                #     for sym in cd:
                #       print " " + sym,
                #     print "  from " + str(j)

    accepting_state = (start_rule[0], start_rule[1], [], 0)
    return accepting_state in chart[len(_tokens) - 1]


# ####################################################################
# We've rigged up a simple testing framework for you.

def test_it(_grammar, _tokens):
    x = max(len(_grammar), len(_tokens), max([len(rule[1]) for rule in _grammar]))
    print "x =", x, " work =", work_count, " 2*X^3 =", 2 * x * x * x
    if work_count > 2 * x * x * x and 10 < x < 50:
        print "Success! Copy these down and submit them."
        print "grammar = ", _grammar
        print "tokens = ", _tokens


# You should start changing code around here.

grammar = [
    ("S", ["P"]),
    ("P", ["(", "P", ")"]),
    ("P", ["(", "P", "("]),
    ("P", [")", "P", ")"]),
    ("P", []),
]

for i in [5, 10, 15, 20, 25]:
    # Make i nested balanced parentheses.
    tokens = ["(" for li in range(i)] + [")" for ri in range(i)]
    test_it(grammar, tokens)

# If you run this and look closely, you'll see that as X doubles
# from 5 to 10, the work_count roughly doubles as well, and so on.
# So the work done when we parse strings in this balanced
# parentheses grammar behaves like X^1, not X^3. So this isn't the
# answer. Use your creativity to find something that is.

grammar = [
    ("S", ["P"]),
    ("P", ["(", "P", ")"]),
    ("P", ["(", "P", "("]),
    ("P", [")", "P", ")"]),
    ("P", []),
]  # put your final answer here
tokens = ['(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', '(', ')', ')',
          ')', ')', ')', ')', ')', ')', ')', ')', ')', ')', ')', ')', ')', ')', ')', ')', ')', ')']
# put your final answer here


# even better!!!
worse_grammar = [
    ("S", ["P"]),
    ("P", ["(", "P", ")"]),
    ("P", ["(", "(", "P"]),
    ("P", ["P", ")", ")"]),
    ("P", []),
    ]