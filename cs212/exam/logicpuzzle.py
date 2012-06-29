__author__ = 'dhensche'

import itertools

"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon. -----------------------
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager. ----------------------
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

def either(role, p1 ,p2):
    return role is p1 or role is p2

def double_either(r1, r2, p1, p2):
    return (r1 is p1 and r2 is p2) or (r1 is p2 and r2 is p1)

def after(d1, d2):
    return d1 == 1 + d2

def logic_puzzle():
    days = monday, tuesday, wednesday, thursday, friday = [1,2,3,4,5]
    orderings = list(itertools.permutations(days))

    return next(map(lambda pair: pair[1], sorted([(Hamming, 'Hamming'), (Knuth, 'Knuth'), (Minsky, 'Minsky'), (Simon, 'Simon'), (Wilkes, 'Wilkes')]))
                for (Hamming, Knuth, Minsky, Simon, Wilkes) in orderings
                if after(Knuth, Simon)
                for (programmer, writer, manager, designer, _) in orderings
                if programmer is not Wilkes and writer is not Minsky and after(Knuth, manager) and thursday is not designer
                for (droid, tablet, laptop, iphone, _) in orderings
                if double_either(programmer, droid, Wilkes, Hamming) and designer is not droid and not either(manager, tablet, Knuth) and friday is not tablet and either(tuesday, tablet, iphone) and wednesday is laptop and double_either(laptop, Wilkes, monday, writer)
    )


print logic_puzzle()
