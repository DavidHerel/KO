import gurobipy as g

#two partition problem - problem se zlodeji co si chteji rozdelit lup na pul (ty bankovky)
p = [100, 50, 50, 50, 20, 20, 10]
model = g.Model()

#binarni promenne
x = model.addVars(len(p), vtype=g.GRB.BINARY, name="x")

#nutno provazat vztahy mezi x
set1 = g.quicksum([x[ind]*p[ind] for ind in range(len(p))])
set2 = g.quicksum([(1- x[ind])*p[ind] for ind in range(len(p))])

#tady rekneme, ze se musi rovnat
model.addConstr(set1 == set2)

model.optimize()

#rika jestli to lze nebo nelze
#tenhle kus kodu rika jak, pokud to lze
if model.Status == g.GRB.OPTIMAL:
    for ind in range(len(p)):
        #0.5 a ne 0 tam je protoze ten Gurubi ty hodnoty nedrzi uplne ok
        print(p[ind], "in S1" if (x[ind].x > 0.5) else "in S2")