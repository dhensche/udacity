__author__ = 'dhensche'

def small_words(words):
    for word in words:
        if len(word) < 4:
            yield word