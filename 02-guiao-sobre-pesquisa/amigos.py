from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

def amigos_constraint(a1, v1, a2, v2):
    b1, c1 = v1
    b2, c2 = v2

    if b1 == b2 or c1 == c2:
        return False

    if a1 == b1 or a1 == c1 or a2 == b2 or a2 == c2:
        return False

    if b1 == c1 or b2 == c2:
        return False

    if c1 == "Claudio" and b1 != "Bernardo":
        return False
    if c2 == "Claudio" and b2 != "Bernardo":
        return False

    return True

def make_constraint_graph(amigos):
    return {(X,Y): amigos_constraint for X in amigos for Y in amigos if X != Y}

def make_domain(amigos):
    return {a: [(b,c) for b in amigos for c in amigos] for a in amigos}

cs = ConstraintSearch(make_domain(amigos), make_constraint_graph(amigos))

print(cs.search())
