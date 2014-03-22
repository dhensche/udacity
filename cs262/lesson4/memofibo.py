__author__ = 'dhensche'

# Memofibo

# Submit via the interpreter a definition for a memofibo procedure that uses a
# chart. You are going to want the Nth value of the chart to hold the Nth
# fibonacci number if you've already computed it and to be empty otherwise.

chart = {}


def memofibo(n):
    if n <= 2:
        return 1
    elif n in chart:
        return chart[n]
    else:
        chart[n] = memofibo(n - 1) + memofibo(n - 2)
        return chart[n]


print memofibo(6)


