__author__ = 'Derek'

# Implementing RE
# Challenge Problem
#
# Focus: All Units
#
#
# In this problem you will write a lexer, parser and interpreter for
# strings representing regular expressions. Your program will output
# a non-deterministic finite state machine that accepts the same language
# as that regular expression.
#
# For example, on input
#
# ab*c
#
# Your program might output
#
# edges = { (1,'a')  : [ 2 ] ,
#           (2,None) : [ 3 ] ,    # epsilon transition
#           (2,'b')  : [ 2 ] ,
#           (3,'c')  : [ 4 ] }
# accepting = [4]
# start = 1
#
# We will consider the following regular expressions:
#
#       single characters       #       a
#       regexp1 regexp2         #       ab
#       regexp *                #       a*
#       regexp1 | regexp2       #       a|b
#       ( regexp )              #       (a|b)* -- same as (?:a|b)
#
# That's it. We won't consider [a-c] because it's just a|b|c, and we won't
# consider a+ because it's just aa*. We will not worry about escape
# sequences. Single character can be a-z, A-Z or 0-9 -- that's it. No need
# to worry about strange character encodings. We'll use ( ) for regular
# expression grouping instead of (?: ) just to make the problem simpler.
#
# Don't worry about precedence or associativity. We'll fully parenthesize
# all regular expressions before giving them to you.
#
# You will write a procedure re_to_nfsm(re_string). It takes as input a
# single argument -- a string representing a regular expression. It returns
# a tuple (edges,accepting,start) corresponding to an NSFM that accepts the
# same language as that regular expression.
#
# Hint: Make a lexer and a paser and an interpreter. Your interpreter may
# find it handy to know the current state and the goal state. Make up as
# many new states as you need.
#
import ply.lex as lex
import ply.yacc as yacc
from collections import defaultdict

# Fill in your code here.
tokens = (
    'STAR',
    'BAR',
    'OPPAR',
    'CLPAR',
    'TOKEN'
    )

t_STAR = r'\*'
t_BAR = r'\|'
t_OPPAR = r'\('
t_CLPAR = r'\)'
t_TOKEN = r'[0-9a-zA-Z]'

def t_error(t):
    raise Exception("Lexer error.")

def p_start(p):
    "start : regexlist"
    p[0] = ('list', p[1])

def p_regexlist_plus_regex(p):
    "regexlist : regexlist regex"
    p[0] = p[1] + [p[2]]

def p_regexlist_to_empty(p):
    "regexlist :"
    p[0] = []

def p_regex_with_star(p):
    "regex : regex STAR"
    p[0] = ('star', p[1])

def p_regex_with_choice(p):
    "regex : regex BAR regex"
    p[0] = ('either', p[1], p[3])

def p_regex_to_regexlist(p):
    "regex : OPPAR regexlist CLPAR"
    p[0] = ('list', p[2])

def p_regex_to_token(p):
    "regex : TOKEN"
    p[0] = ('char', p[1])

def p_error(p):
    raise Exception("Parser error.")

precedence = (
    ('left', 'STAR'),
    ('left', 'BAR'),
    )

lexer = lex.lex()
parser = yacc.yacc()

def interpret(parse_tree, state, next_free, edges):
    type = parse_tree[0]
    value = parse_tree[1]
    if type == 'list':
        edges[state, None].append(next_free)
        state, next_free = next_free, next_free+1
        for regex in value:
            state, next_free = interpret(regex, state, next_free, edges)
        return state, next_free
    elif type == 'star':
        end, next_free = interpret(value, state, next_free, edges)
        edges[end, None].append(state)
        return state, next_free
    elif type == 'either':
        edges[state, None].append(next_free)
        end1, next_free = interpret(value, next_free, next_free+1, edges)
        edges[state, None].append(next_free)
        end2, next_free = interpret(parse_tree[2], next_free, next_free+1, edges)
        edges[end2, None].append(next_free)
        edges[end1, None].append(next_free)
        return next_free, next_free+1
    else: # token
        edges[state, value].append(next_free)
        return next_free, next_free+1

def re_to_nfsm(re_string):
    lexer.input(re_string)
    parse_tree = parser.parse(re_string, lexer=lexer)
    edges = defaultdict(list)
    accepting, _ = interpret(parse_tree, 0, 1, edges)
    return edges, [accepting], 0

print re_to_nfsm("a(b*)c")

# We have included some testing code ... but you really owe it to yourself
# to do some more testing here.

def nfsmaccepts(edges, accepting, current, string, visited):
# If we have visited this state before, return false.
    if (current, string) in visited:
        return False
    visited.append((current, string))

    # Check all outgoing epsilon transitions (letter == None) from this
    # state.
    if (current, None) in edges:
        for dest in edges[(current, None)]:
            if nfsmaccepts(edges, accepting, dest, string, visited):
                return True

    # If we are out of input characters, check if this is an
    # accepting state.
    if string == "":
        return current in accepting

    # If we are not out of input characters, try all possible
    # outgoing transitions labeled with the next character.
    letter = string[0]
    rest = string[1:]
    if (current, letter) in edges:
        for dest in edges[(current, letter)]:
            if nfsmaccepts(edges, accepting, dest, rest, visited):
                return True
    return False

def test(re_string, e, ac_s, st_s, strings):
    my_e, my_ac_s, my_st_s = re_to_nfsm(re_string)
    print my_e
    for string in strings:
        print nfsmaccepts(e,ac_s,st_s,string,[]) ==\
              nfsmaccepts(my_e,my_ac_s,my_st_s,string,[])

edges = { (1,'a')  : [ 2 ] ,
          (2,None) : [ 3 ] ,    # epsilon transition
          (2,'b')  : [ 2 ] ,
          (3,'c')  : [ 4 ] }
accepting_state = [4]
start_state = 1

test("a(b*)c", edges, accepting_state, start_state,
    [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  )

edges = { (1,'a')  : [ 2 ] ,
          (2,'b') :  [ 1 ] ,
          (1,'c')  : [ 3 ] ,
          (3,'d')  : [ 1 ] }
accepting_state = [1]
start_state = 1

test("((ab)|(cd))*", edges, accepting_state, start_state,
    [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  )
