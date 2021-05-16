#!/usr/bin/env python3
import math
import sys

import numpy as np
from copy import copy

best_cost = float(np.inf)
best_sol = []

def bradley(p, r, d, rest_tasks, c, upper, solution):
    global best_cost, best_sol

    stop_backtracking = False
    #stopping condition for recursion
    if (rest_tasks == []):
        return True, stop_backtracking, c, solution

    r_j = []
    for i in rest_tasks:
        r_j.append(r[i])
    if c <=min(r_j):
        #do not backtrack
        stop_backtracking = True

    #1)
    # missed deadline
    for i in rest_tasks:
        #prune this node
        if (max(c, r[i])+p[i] > d[i]):
            print("Pruned on 1. missed deadline")
            return False, stop_backtracking, c, solution

    #2)
    #Bound on the solution
    sum_p = 0
    for i in rest_tasks:
        sum_p += p[i]
    lb = max(c, min(r_j)) + sum_p
    #prune it
    if (lb >= upper):
        print("Pruned on 2. bound on the solution")
        return False, stop_backtracking, c, solution


    was_found = False
    glob_stop_backtrack = stop_backtracking
    curr_cost = float(np.inf)
    curr_sol = []
    for i in rest_tasks:
        new_sol = solution + [i]
        new_cost = max(r[i], c) + p[i]

        # temp_task = copy(rest_tasks)
        # temp_task.pop(i)
        temp_task = []
        for j in rest_tasks:
            if j !=i:
                temp_task.append(j)

        found, stop_backtrack, temp_cost, temp_sol = bradley(p, r, d, temp_task, new_cost, upper, new_sol)

        if (found):
            was_found = True
            # if temp_cost < best_cost:
            #     print("Best sol found")
            #     best_sol = temp_sol
            #     best_cost = temp_cost
            #     upper = temp_cost
            if temp_cost < curr_cost:
                curr_sol = temp_sol
                curr_cost = temp_cost
                upper = temp_cost
                print("Best sol found " + str(curr_sol) + "  " + str(curr_cost))
        glob_stop_backtrack = glob_stop_backtrack or stop_backtracking
        if stop_backtrack:
            print("Break pri i: " + str(i))
            break

    return was_found, glob_stop_backtrack, curr_cost, curr_sol

if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #INPUT PHASE

    #open file from 1st argument
    f = open(input, "r")

    n = int(f.readline())

    p =[]
    r=[]
    d=[]
    rest_tasks = []
    for i in range(n):
        first_line = list(map(int, f.readline().split()))
        p.append(first_line[0])
        r.append(first_line[1])
        d.append(first_line[2])
        rest_tasks.append(i)
        # print(i)
        # print(first_line[0])
        # print(first_line[1])
        # print(first_line[2])
        # print("---------")
    f.close()
    ub = max(d) + 1
    print(ub)

    solution, _, _, cur_sol = bradley(p, r, d, rest_tasks, 0, ub, [])
    print(cur_sol)
    if solution:
        print("solution found")
        pp = [0 for _ in range(n)]
        f = open(output, "w")
        start = 0
        answ = []
        for i in cur_sol:
            pp[i] = max(start, r[i])
            #f.write(str(max(start, r[i])) + "\n")
            print(max(start, r[i]))
            #answ.append(max(start, r[i]))
            start = max(start, r[i]) + p[i]
        f.write('\n'.join(map(str, pp)))
        f.close()
    else:
        print("Solution not found")
        f = open(output, "w")
        f.write("-1")
        f.close()