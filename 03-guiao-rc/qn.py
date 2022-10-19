domain = {"R1": [1,2,3,4],
           "R2": [1,2,3,4],
           "R3": [1,2,3,4],
           "R4": [1,2,3,4]}

edges = [(v1,v2) for v1 in domain for v2 in domain if v1!=v2]

def queenconstraint(r1, c1, r2, c2):
    if c1 == c2:
        return False
    l1 = int(r1[1:])
    l2 = int(r2[1:])
    return abs(c2-c1)!=abs(l2-l1)
    
constraints = {e : queenconstraint for e in edges}
print(constraints)