__author__ = 'dhensche'

# Quoted Strings

# Suppose a string starts with " and ends with " and contains any number of
# characters except ". Write a definition for t_STRING.

# Match Exactly:
#     "cuneiform"
#     "sumerian writing"
# Do Not Match Exactly:
#     "esc \" ape"
#     League of Nations Treaty Series 

def t_STRING(token):
    r'"[^"]*"'
    return token