import sys
import gurobipy as g

def opt_model(q):
    # minimize sum(zi)
    #   qi-vi <= zi
    #   vi-qi <= zi
    #   zi    >= 0
    model = g.Model()

    hours = len(q)

    # variables - discrete = LP problem
    z = model.addVars(hours, lb=0, ub=g.GRB.INFINITY, obj=1.0,
                     vtype=g.GRB.INTEGER, name="z")
    v = model.addVars(hours, lb=0, ub=g.GRB.INFINITY, obj=0.0,
                     vtype=g.GRB.INTEGER, name="v")
    model.update()

    #TODO - rewrite this part
    #make a sum of i-7 till i
    sum_v = [sum([v[j % hours] for j in range(i - 7, i + 1)]) for i in range(hours)]
    [print([v[j % hours] for j in range(i - 7, i + 1)]) for i in range(hours)]

    # conditions/constrains
    for i in range(hours):
        model.addConstr(q[i] - sum_v[i] <= z[i])
        model.addConstr(sum_v[i] - q[i] <= z[i])
        model.addConstr(z[i] >= 0) #not needed cuz of lb=0

    # objective
    #model.setObjective(z, g.GRB.MINIMIZE) #not needed cuz of obj = 1.0

    model.optimize()

    #first round then convert to int
    result = int(round(model.objVal))
    shifts = [int(round(v[i].x)) for i in range(hours)]
    print(result)
    print(shifts)

    return result, shifts

if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #open file from 1st argument
    f = open(input, "r")
    #read the string from the file, split it by space, map int() to every string - to make it int, and then wrap it as a list
    q = list(map(int, f.read().split()))
    f.close()

    #function to find optimal solution
    result, shifts = opt_model(q)

    #output it to a file
    f = open(output, "a")
    f.write(str(result)+"\n")
    f.write(' '.join(map(str, shifts)))
    f.close()

