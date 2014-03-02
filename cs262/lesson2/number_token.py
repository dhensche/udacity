__author__ = 'dhensche'

# Numbers

# Write a indentifier token rule for Javascript numbers that converts the value
# of the token to a float.

# The token rule should match:

#    12
#    5.6
#    -1.
#    3.14159
#    -8.1
#    867.5309

# The token rule should not match:

#    1.2.3.4
#    five
#    jenny


def t_NUMBER(token):
    r'-?\d+(?:\.\d*)?'
    token.value = float(token.value)
    return token

