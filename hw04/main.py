#!/usr/bin/env python3
import math
import sys
from collections import deque
from itertools import product
import gurobipy as g

import numpy as np

def find_cycle(path, starting):
    cycle_vertexes = []
    #print(path)
    #print(starting)
    #print(len(cycle))
    #pridam prvni prvek
    q = deque()
    q.appendleft(starting)
    while q:
        node = q.pop()
        #print("exploring")
        cycle_vertexes.append(node)
        if (path[node] not in cycle_vertexes):
            q.appendleft(path[node])
    return cycle_vertexes

def shortest_cycle(graph):
    #print("graph")
    #print(graph)
    path = {}
    #set all vertexes as unvisited
    visited = [0]*len(graph)
    for v in graph:
        if visited[v] == 0:
            c = find_cycle(graph, v)
            #print("cyklus")
            #print(cycle)
            for j in c:
                visited[j] = 1
            if len(c) < len(path) or len(path) == 0:
                path = c

    return len(path), path

def callback(m, where):
    if where == g.GRB.Callback.MIPSOL:
        graph = {i: j for (i, j) in combinations_second if i != j and m.cbGetSolution(x[i, j]) == 1}
        length, cycle = shortest_cycle(graph)
        if length == n+1:
            return
        else:
            edges = []
            edges.append((cycle[-1], cycle[0]))
            for i in range(length-1):
                v_a = cycle[i]
                v_b = cycle[i+1]
                edges.append((v_a, v_b))
            #print("edges 1")
            #print(edges)
            m.cbLazy(length - 1 >= sum([x[i, j] for i, j in edges]))
    else:
        return

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
        c[(n, i)] = 0
        c[(i, n)] = 0

    #now LETS init model
    model = g.Model()
    model.Params.lazyConstraints = 1

    combinations_second = list(product(range(n+1), range(n+1)))

    x = model.addVars(n+1 , n+1, vtype=g.GRB.BINARY)

    #model.addConstrs(x.sum(i, j) == 1 for i, j in combinations_second if i != j)
    #model.addConstrs(x.sum(j, i) == 1 for i, j in combinations_second if i != j)
    model.addConstrs(x.sum(i, '*') == 1 for i in range(n+1))
    model.addConstrs(x.sum('*', i) == 1 for i in range(n+1))
    model.addConstrs(x[i, i] == 0 for i in range(n+1))

    model.setObjective(sum([x[i,j] * c[i, j] for (i, j) in combinations_second if i != j]), sense=g.GRB.MINIMIZE)

    model.optimize(callback)

    graph = {}
    for i,j in x.items():
        if j.x >= 0.5:
            graph[i[0]]=i[1]

    #print(graph)

    f_output = open(output, "w")

    cur = graph[n]
    while cur != n:
        f_output.write(str(cur + 1) + " ")
        cur = graph[cur]
