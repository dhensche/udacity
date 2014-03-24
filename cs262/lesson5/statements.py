__author__ = 'dhensche'

# QUIZ: Evaluating Statements


def eval_stmts(tree, environment):
    stmttype = tree[0]
    if stmttype == "assign":
        # ("assign", "x", ("binop", ..., "+",  ...)) <=== x = ... + ...
        variable_name = tree[1]
        right_child = tree[2]
        new_value = eval_exp(right_child, environment)
        env_update(environment, variable_name, new_value)
    elif stmttype == "if-then-else":  # if x < 5 then A;B; else C;D;
        if bool(tree[1]):
            eval_stmts(tree[2], environment)
        else:
            eval_stmts(tree[3], environment)


def eval_exp(exp, env):
    etype = exp[0]
    if etype == "number":
        return float(exp[1])
    elif etype == "string":
        return exp[1]
    elif etype == "true":
        return True
    elif etype == "false":
        return False
    elif etype == "not":
        return not (eval_exp(exp[1], env))


def env_update(env, vname, value):
    env[vname] = value


ENVIRONMENT = {"x": 2}
TREE = ("if-then-else", ("true", "true"), ("assign", "x", ("number", "8")), ("assign", "x", "5"))
eval_stmts(TREE, ENVIRONMENT)
print ENVIRONMENT == {"x": 8}