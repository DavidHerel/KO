#!/usr/bin/env python3

import sys
import gurobipy as g

if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #open file from 1st argument
    f = open(input, "r")

    #read the string from the file, split it by space, map int() to every string - to make it int, and then wrap it as a list
    q = list(map(int, f.read().split()))
    f.close()

    #find optimal solution
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
    model.update() #needed to have a print working

    # make a sum of i-7 till i
    sum_v = [0]*24
    for i in range(hours):
        # e.g. if we want midnight (0-1) we need 17-18,18-19,19-20,20-21,21-22,22-23,23-24,0-1...==8
        sum_v[i] = sum([v[j % hours] for j in range(i - 7, i + 1)])
        #print(sum_v[i])

    # conditions/constrains
    for i in range(hours):
        model.addConstr(q[i] - sum_v[i] <= z[i], name = "C1") #first cond
        model.addConstr(sum_v[i] - q[i] <= z[i], name = "C2") #second cond
        model.addConstr(z[i] >= 0, name = "C3")  # not needed cuz of lb=0

    # objective
    # model.setObjective(z, g.GRB.MINIMIZE) #not needed cuz of obj = 1.0

    model.optimize()

    #if result exists
    if model.Status == g.GRB.OPTIMAL:

        # first round then convert to int
        result = int(round(model.objVal))

        #same for shifts
        shifts = [0]*24
        for i in range(hours):
            shifts[i] = int(round(v[i].x))

        #print(result)
        #print(shifts)

        #output it to a file
        f = open(output, "a")
        f.write(str(result)+"\n")
        f.write(' '.join(map(str, shifts)))
        f.close()

