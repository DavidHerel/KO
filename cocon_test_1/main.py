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

    # GUROBIPY
    model = g.Model()
    # get binary values
    x = {(i, j): model.addVar(vtype=g.GRB.BINARY)
         for i, j in permutations(range(1, nodes + 1), 2)}

    print("Preprocessing")
    end = time.time()
    print(end - start)

    start = time.time()
    #THIS TAKES A TON OF TIME
    # triangle inequalities
    for i, j, k in combinations(range(1, nodes + 1), 3):
        model.addConstr(x[(i, j)] + x[(j,k)]-x[(i,k)] <= 1.0)
        model.addConstr(-1*x[(i, j)] - 1* x[(j, k)] + x[(i, k)] <= 0.0)
    print("Loading constraints")
    end = time.time()
    print(end - start)

    start = time.time()
    # set objective
    res = 0
    res2 = 0
    for j in range(1, nodes + 1):
        for k in range(1, j):
            if j != k:
                res += c[k][j] * x[(k, j)]
        for l in range(j + 1, nodes + 1):
            if l != j:
                res2 += c[l][j] * (1 - x[(j, l)])

    model.setObjective(res + res2, g.GRB.MINIMIZE)
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

        #get the edges which we dont want
        for j in range(1, nodes + 1):
            for k in range(1, j):
                if j != k:
                    temp_1 = (c[k][j]*x[(k, j)].x)
                    if(temp_1>0):
                        #print(temp_1)
                        #print("i: " + str(k) + " j: " + str(j))
                        #edges.append((k,j))
                        edge_str = ("\n" + str(k) + " " + str(j))
                        # print(edge_str)
                        f.write(edge_str)
            for l in range(j + 1, nodes + 1):
                if l != j:
                    temp_2 = (c[l][j]*(1-x[(j, l)].x))
                    if (temp_2 > 0):
                        #print(temp_2)
                        #print("i: " + str(l) + " j: " + str(j))
                        #edges.append((l, j))
                        edge_str = ("\n" + str(l) + " " + str(j))
                        # print(edge_str)
                        f.write(edge_str)


        #sort them
        """
        edges.sort()
        for e in edges:
            edge_str = ("\n"+str(e[0]) + " " +str(e[1]))
            #print(edge_str)
            f.write(edge_str)
        """
        f.close()

        print("Getting the result")
        end = time.time()
        print(end - start)