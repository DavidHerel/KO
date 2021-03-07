import gurobipy as g

#data -----------------
# minimize -x + 2y s.t.
#   -4x -9y <= -18
#   (3/2)x - y <= 27/4
#   (8/17)x - y >= -2
model = g.Model()

#variables - continuous = LP problem
x = model.addVar(lb=-g.GRB.INFINITY, ub=g.GRB.INFINITY, obj=0.0,
                 vtype=g.GRB.CONTINUOUS, name="x",
                 column=None)
y = model.addVar(lb=-g.GRB.INFINITY, ub=g.GRB.INFINITY, obj=0.0,
                 vtype=g.GRB.CONTINUOUS, name="y",
                 column=None)

#conditions/constrains
model.addConstr(-4 * x -9 * y <= -18, name="C1")
model.addConstr(3/2 * x -y <= 27/4, name="C2")
model.addConstr(8/17 * x -y >= -2, name="C3")

#objective
model.setObjective(-x + 2 * y, g.GRB.MINIMIZE)

model.optimize()

print("Obj", model.objVal)
print("X", x.X)
print("Y", y.X)

#prechod z LP na ILP - omezime X na celociselne
#branch and bound - delim a osekavam to co uz neni perspektivni - ZAOKROHLOVANI NEFUNGUJE DEVKO

#hw - udelat problemy z pdf dokumentu

