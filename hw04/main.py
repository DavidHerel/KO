#!/usr/bin/env python3
import math
import sys
from collections import deque
from itertools import product
import gurobipy as g

import numpy as np

if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #INPUT PHASE

    #open file from 1st argument
    f = open(input, "r")

    first_line = list(map(int, f.readline().split()))
    n = first_line[0]
    w = first_line[1]
    h = first_line[2]


    S = np.zeros(shape=(n, h, w, 3))
    frame = 0
    all_lines = f.readlines()
    for line in all_lines:
        temp_line = list(map(int, line.split()))
        for j in range(h):
            for k in range(w):
                for pixel in range(3):
                    pixel_index = j*w*3+k*3+pixel
                    curr_pixel = temp_line[pixel_index]
                    S[frame, j, k, pixel] = curr_pixel
        #print(S[frame])
        #print("-----")
        frame+=1

    combinations = product(range(n), range(n))
    c = {}
    for i, j in combinations:
        if i != j:
            c[(i, j)] = np.absolute(S[i][:, -1, :] -S[j][:, 0, :]).sum()
    for i in range(n):
        c[(i, n)] = 0
        c[(n, i)] = 0

    #now LETS init model
    model = g.Model()
    model.Params.lazyConstraints = 1

    combinations_second = product(range(n+1), range(n+1))

    x = model.addVars(n+1  ,n+1, vtype=g.GRB.BINARY)

    model.addConstrs(x[i, j] == 1 for i, j in combinations_second if i != j)
    model.addConstrs(x[j, i] == 1 for i, j in combinations_second if i != j)
    model.addConstrs(x[i, i] == 0 for i in range(n+1))

    model.setObjective(sum([x[i,j] * c[i, j] for (i, j) in combinations_second if i != j]), sense=g.GRB.MINIMIZE)

    #TODO
    model.optimize(callback)

    #TODO
    #callback
    #najit cyklus
    # a je to


