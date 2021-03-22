#!/usr/bin/env python3

import sys
from itertools import combinations
from itertools import permutations

import gurobipy as g

if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #open file from 1st argument
    f = open(input, "r")

    # read the string from the file, split it by space, map int() to every string - to make it int, and then wrap it as a list
    lines = f.readlines()
    f.close()

    # PREPROCESSING PART
    #
    #

    # number of edges
    number_of_edges = list(map(int, lines[0].split()))
    number_of_edges = number_of_edges[0]

    # list from node
    e1 = [0] * number_of_edges
    # list to node
    e2 = [0] * number_of_edges
    #list of weights
    weights = [0] * number_of_edges
    # load the file and fill the values
    for index in range(number_of_edges):
        # get values
        e = list(map(int, lines[index + 1].split()))
        i = e[0]
        j = e[1]
        w = e[2]

        # fill edges
        e1[index] = i
        e2[index] = j
        #fill weights
        weights[index] = w

    # number of nodes
    nodes = max(max(e1), max(e2))

    # GUROBIPY
    c = [[0 for i in range(nodes+1)] for j in range(nodes+1)]

    for index in range(number_of_edges):
        c[e1[index]][e2[index]]=weights[index]


    model = g.Model()
    # get the first half of binary values, the rest is:: x_{j,i} = 1-x_{i,j}
    x = {(i, j): model.addVar(vtype=g.GRB.BINARY)
         for i, j in permutations(range(1, nodes + 1), 2)}

    model.update()

    # triangle inequalities
    for i, j, k in combinations(range(1, nodes + 1), 3):
        lhs = g.LinExpr([(1, x[(i, j)]), (1, x[(j, k)]), (-1, x[(i, k)])])
        model.addConstr(lhs, g.GRB.LESS_EQUAL, 1.0)
        lhs = g.LinExpr([(-1, x[(i, j)]), (-1, x[(j, k)]), (1, x[(i, k)])])
        model.addConstr(lhs, g.GRB.LESS_EQUAL, 0.0)

    # set objective

    # obj2 = [    for i, j in combinations(range(1, nodes+1), 2)]
    res = 0
    res2 = 0
    for j in range(1, nodes + 1):
        for k in range(1, j):
            if j != k:
                res += c[k][j] * x[(k, j)]
        for l in range(j + 1, nodes + 1):
            if l != j:
                res2 += c[l][j] * (1 - x[(j, l)])

    # obj = [(c[i][j], x[(i, j)]) for i, j in combinations(range(1, nodes + 1), 2)]
    model.setObjective(res + res2, g.GRB.MINIMIZE)



    # optimize it
    model.optimize()

    # if result exists
    if model.Status == g.GRB.OPTIMAL:
        # first round then convert to int
        result = int(round(model.objVal))

        for j in range(1, nodes + 1):
            for k in range(1, j):
                if j != k:
                    temp_1 = (c[k][j]*x[(k, j)].x)
                    if(temp_1>0):
                        print(temp_1)
                        print("i: " + str(k) + " j: " + str(j))
            for l in range(j + 1, nodes + 1):
                if l != j:
                    temp_2 = (c[l][j]*(1-x[(j, l)].x))
                    if (temp_2 > 0):
                        print(temp_2)
                        print("i: " + str(l) + " j: " + str(j))

        #printing x
        """
        for i, j in permutations(range(1, nodes + 1), 2):
            #if(x[(i,j)].x >= 0.1 and c[i][j] > 0):
            print(x[(i,j)].x)
            print("i: " +str(i)+ " j: " + str(j))
        """