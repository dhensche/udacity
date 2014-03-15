__author__ = 'dhensche'


def mymin(a,b):
    return a if a < b else b


def square(x): return x * x

print mymin(square(-2),square(3))