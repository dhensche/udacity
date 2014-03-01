__author__ = 'dhensche'

# Specifying Tokens

# Write code for the LANGLESLASH token to match </ in our HTML.

def t_LANGLESLASH(token):
    r'</'
    return token
