__author__ = 'dhensche'

# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I created ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""

TARGETS = dict(reduce(lambda x, y: dict(x.items() + y.items()), [{('S%d' % x): x, ('D%d' % x):x*2, ('T%d' % x):x*3} for x in range(1,21)]).items() + {'DB': 50, 'SB': 25, 'OFF': 0}.items())
POSSIBLE_SCORES = [0] + sorted(set(TARGETS.values()), reverse=True)
SECTIONS = {'20': ['1', '5'], '1': ['20', '18'], '18': ['1', '4'],
            '4': ['18', '13'], '13': ['4', '6'], '6': ['13', '10'],
            '10': ['6', '15'], '15': ['10', '2'], '2': ['15', '17'],
            '17': ['2', '3'], '3': ['17', '19'], '19': ['3', '7'],
            '7': ['19', '16'], '16': ['7', '8'], '8': ['16', '11'],
            '11': ['8', '14'], '14': ['11', '9'], '9': ['14', '12'],
            '12': ['9', '5'], '5': ['12', '20']}

def name(d, needs_double=False):
    if not needs_double:
        if d <= 20:
            return 'S%d' % d
        elif d % 3 is 0 and d <= 60:
            return 'T%d' % (d / 3)
        elif d % 2 is 0 and d <= 40:
            return 'D%d' % (d / 2)
        elif d == 25:
            return 'SB'
        elif d == 50:
            return 'DB'
        else:
            return ''
    else:
        if d % 2 is 0:
            return 'D%d' % (d / 2)
        else:
            return name(d)

def double_out(total):
    scores = []
    for score1 in POSSIBLE_SCORES:
        for score2 in POSSIBLE_SCORES:
            score3 = (total - score1 - score2)
            if score3 in POSSIBLE_SCORES:
                scores = filter(lambda x: x != 0, [score1, score2, score3])
                darts = sorted(map(name, scores), reverse=True)
                if darts[-1][0] == 'D': return darts

    if not len(scores): return None

    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    # your code here

"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""

def neighbors(target):
    if target == 'DB' or target == 'SB':
        return SECTIONS.keys()
    return SECTIONS[target[1:]]

def outcome(target, miss):
    miss = miss * 0.2 if target[0] == 'S' else 3 * miss if target == 'DB' else miss
    hit = 1 - miss
    around_me = neighbors(target)
    h_miss = miss * (1.0/len(around_me))
    distribution = {target: hit ** 2}

    for neighbor in around_me:
        side = 'S' if target == 'DB' or target == 'SB' else target[0]
        if target == 'SB' or target == 'DB':
            distribution[target] = hit
            if target == 'SB':
                distribution['DB'] = 0.25 * miss
                distribution[side + neighbor] = 0.75 * h_miss
            else:
                distribution['SB'] = (1.0 / 3) * miss
                distribution[side + neighbor] = (2.0 / 3) * h_miss
        else:
            distribution[side + neighbor] = hit * h_miss

            if side == 'T':
                distribution['S' + neighbor] = miss * h_miss
                distribution['S' + target[1:]] = hit * miss
            elif side == 'S':
                distribution['T' + neighbor] = miss * 0.5 * h_miss
                distribution['D' + neighbor] = miss * 0.5 * h_miss
                distribution['T' + target[1:]] = miss * 0.5 * hit
                distribution['D' + target[1:]] = miss * 0.5 * hit
            else:
                distribution['OFF'] = miss * 0.5
                distribution['S' + neighbor] = miss * 0.5 * h_miss
                distribution['S' + target[1:]] = miss * 0.5 * hit


    "Return a probability distribution of [(target, probability)] pairs."
    return distribution

def best_target(miss):
    "Return the target that maximizes the expected score."
    #your code here
    return max([(sum(map(lambda x: TARGETS[x[0]] * x[1], outcome(target, miss).iteritems())), target) for target in TARGETS.keys() if target != 'OFF'])[1]

def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
        for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1),
            {'T20': 0.81, 'S1': 0.005, 'T5': 0.045,
             'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
        outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
             'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
             'S7': 0.016, 'SB': 0.64}))


print(outcome('SB', 0.2))
print test_darts2()
