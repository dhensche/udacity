__author__ = 'dhensche'

# Quiz: Eval Exp

# Write an eval_exp procedure to interpret JavaScript arithmetic expressions.
# Only handle +, - and numbers for now.


def eval_exp(tree):
    # ("number" , "5")
    # ("binop" , ... , "+", ... )
    nodetype = tree[0]
    if nodetype == "number":
        return int(tree[1])
    elif nodetype == "binop":
        left_val = eval_exp(tree[1])
        operator = tree[2]
        right_val = eval_exp(tree[3])
        if operator == '-':
            return left_val - right_val
        elif operator == '+':
            return left_val + right_val
        else:
            return None
            # QUIZ: (1) evaluate left and right child
            # (2) perform "operator"'s work


test_tree1 = ("binop", ("number", "5"), "+", ("number", "8"))
print eval_exp(test_tree1) == 13

test_tree2 = ("number", "1776")
print eval_exp(test_tree2) == 1776

test_tree3 = ("binop", ("number", "5"), "+", ("binop", ("number", "7"), "-", ("number", "18")))
print eval_exp(test_tree3) == -6