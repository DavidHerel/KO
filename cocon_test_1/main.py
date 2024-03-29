#!/usr/bin/env python3

import sys
from itertools import combinations
from itertools import permutations
import time

import gurobipy as g

if  __name__ == '__main__':
    start = time.time()
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

    # list of: from node
    e1 = [0] * number_of_edges
    # list of: to node
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

    #create matrix of weights
    c = [[0 for i in range(nodes+1)] for j in range(nodes+1)]

    #fill the matrix of weights
    for index in range(number_of_edges):
        c[e1[index]][e2[index]]=weights[index]

    print("Preprocessing")
    end = time.time()
    print(end - start)

    start = time.time()
    #this takes TONS OF TIME
    # GUROBIPY
    model = g.Model()

    # get binary values if e(i,j) is selected
    x = {(e1[i], e2[i]): model.addVar(vtype=g.GRB.BINARY)
         for i in range(len(e1))}

    # get real values if node i is on y position in topological ordering
    y = {i: model.addVar(vtype=g.GRB.INTEGER, ub=nodes+1)
         for i in range(1, nodes + 1)}

    model.update()
    print("Loading binary E")
    end = time.time()
    print(end - start)

    bigM = 1000000;
    start = time.time()

    #for edge: y_i < y_j
    for i in range(len(e1)):
        #+ 1, cuz < is not supported
        model.addConstr(y[e1[i]] + 1 <= (y[e2[i]]  + bigM*x[(e1[i], e2[i])]))

    print("Loading constraints")
    end = time.time()
    print(end - start)

    start = time.time()

    # set objective
    res = 0
    for i in range(len(e1)):
        res += c[e1[i]][e2[i]]*x[(e1[i], e2[i])]

    model.setObjective(res, g.GRB.MINIMIZE)
    print("Setting up objective")
    end = time.time()
    print(end - start)

    start = time.time()
    print("Optimization started")
    # optimize it
    model.optimize()

    print("Opt lasted:")
    end = time.time()
    print(end - start)

    start = time.time()
    # if result exists
    if model.Status == g.GRB.OPTIMAL:
        # first round then convert to int
        result = int(round(model.objVal))
        f = open(output, "w")
        f.write(str(result))
        #print(str(result))
        #edges = []

        for i in range(len(e1)):

            if (x[(e1[i], e2[i])].x >=0.5):
                edge_str = ("\n" + str(e1[i]) + " " + str(e2[i]))
                print(edge_str)
                #print("X_ij: " + str(x[(e1[i], e2[i])].x))
                #print("I: " + str(y[e1[i]].x) + " j: " + str(y[e2[i]].x))
                f.write(edge_str)

        #sort them
        f.close()

        print("Getting the result")
        end = time.time()
        print(end - start)