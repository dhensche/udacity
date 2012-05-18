__author__ = 'dhensche'
# -----------------
# User Instructions
#
# This problem deals with the one-player game foxes_and_hens. This
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'.
#
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions,
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card.
#
# Your job is to define two functions. The first is do(action, state),
# where action is either 'gather' or 'wait' and state is a tuple of
# (score, yard, cards). This function should return a new state with
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an
# action based on the state. This strategy should average at least
# 1.5 more points than the take5 strategy.

import random
from functools import update_wrapper

all_actions = ['wait', 'gather']

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F'*foxes + 'H'*hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)

    return score + yard

def do(action, state):
    "Apply action to state, returning a new state."
    score, yard, cards = state
    index = random.randint(0, len(cards)-1)
    new_card = cards[index]
    cards = cards[:index] + cards[index + 1:]
    if action == 'wait':
        return (score, yard + 1, cards) if new_card == 'H' else (score, 0, cards)
    elif action == 'gather':
        return (score + yard, 0, cards)
        # Make sure you always use up one card.
        #
        # your code here

def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'

def average_score(strategy, N=1000):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)

def superior(A, B=take5):
    "Does strategy A have a higher average score than B, by more than 1.5 point?"
    avg_a = average_score(A)
    avg_b = average_score(B)
    diff = avg_a - avg_b
    print "The difference of %s - %s is %s" % (avg_a, avg_b, diff)
    return diff > 1.5

def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."
    def EU(action): return Q(state, action, U)
    return max(actions, key=EU)

def strategy(state):
    return best_action(state, all_actions, Q, U)

def Q(state, action, u):
    (score, yard, cards) = state
    count_f = cards.count('F')
    count_h = cards.count('H')
    if action == 'gather':
        total = 0
        if count_f:
            total += u((score + yard, 0, cards.replace('F', '', 1))) * count_f
        if count_h:
            total += u((score + yard, 0, cards.replace('H', '', 1))) * count_h
        return total / len(cards)
    else:
        total = 0
        if count_f:
            total += u((score, 0, cards.replace('F', '', 1))) * count_f
        if count_h:
            total += u((score, yard + 1, cards.replace('H', '', 1))) * count_h
        return total / len(cards)

@memo
def U(state):
    (score, yard, cards) = state
    if len(cards) == 0:
        return score + yard
    else:
        return max(Q(state, action, U) for action in all_actions)

def test():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or
            gather == (9, 0, 'F'*4 + 'H'*9))

    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))

    assert superior(strategy)
    return 'tests pass'

print test()

