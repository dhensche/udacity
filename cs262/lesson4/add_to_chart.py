__author__ = 'dhensche'

# Addtochart

# Let's code in Python! Write a Python procedure addtochart(chart,index,state)
# that ensures that chart[index] returns a list that contains state exactly
# once. The chart is a Python dictionary and index is a number. addtochart
# should return True if something was actually added, False otherwise. You may
# assume that chart[index] is a list.


def addtochart(chart, index, state):
    if state in chart[index]:
        return False
    else:
        chart[index] += [state]
        return True




