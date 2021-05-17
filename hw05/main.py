#!/usr/bin/env python3
import math
import sys

import numpy as np
from copy import copy

p,r,d = [], [], []
best_sol, best_cost = [], np.inf
glob_was_found = False

def bratley(rest_tasks, c, upper, solution, int_time):
    global p,r,d, best_sol, best_cost, glob_was_found

    stop_backtracking = False
    #3) stop backtracking
    #stopping condition for recursion
    if (rest_tasks == []):
        return c, solution, True, stop_backtracking, int_time
    else:
        was_found = False
        curr_cost = np.inf
        sum_p = 0
        r_j = []
        for i_k in range(len(rest_tasks)):
            i = rest_tasks[i_k]
            r_j.append(r[i])
            sum_p += p[i]
        if c <=min(r_j):
            #do not backtrack
            stop_backtracking = True

        #2)
        #Bound on the solution
        lb = max(c, min(r_j)) + sum_p
        #prune it
        if (lb >= upper):
            print("Pruned on 2. bound on the solution")
            return c, solution, was_found, stop_backtracking, int_time

        #1)
        # missed deadline
        for i_k in range(len(rest_tasks)):
            i = rest_tasks[i_k]
            #prune this node
            if (max(c, r[i])+p[i] > d[i]):
                print("Pruned on 1. missed deadline")
                return c, solution, was_found, stop_backtracking, int_time

        for i_k in range(len(rest_tasks)):
            i = rest_tasks[i_k]
            temp_task = rest_tasks.copy()
            temp_task.remove(i)
            int_time = max(int_time, p[i]) + i
            cost_upg = max(c, r[i])
            new_sol = solution.copy()
            new_sol.append(i)

            temp_cost, temp_sol, found, stop_backtrack, int_time  = bratley(temp_task, cost_upg + p[i], upper, new_sol, int_time)

            if (int_time >= 0 and found):
                if temp_cost < best_cost:
                    #print("Best sol found")
                    best_sol = temp_sol
                    int_time+=1
                    best_cost = temp_cost
                    upper = temp_cost
                    #print("Tady")
                if temp_cost < curr_cost:
                    int_time += 1
                    curr_cost = temp_cost
                    upper = temp_cost
                    #print("Tady")
                    #print("Best sol found " + str(curr_sol) + "  " + str(curr_cost))
                was_found = True
                glob_was_found = True
            if int_time >= 0 and stop_backtrack:
                stop_backtracking = True
                print("Break pri i: " + str(i))
                print("Int time "  + str(int_time))
                return best_cost, best_sol, was_found, stop_backtracking, int_time
        return best_cost, best_sol, was_found, stop_backtracking, int_time + 1

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
    final_starting_times = ["-1" for i in range(n)]
    offset = 0
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
    int_time = 0
    bratley(rest_tasks, 0, ub, [], int_time)
    print(best_sol)
    if glob_was_found:
        print("solution found")
        f = open(output, "w")
        for i_k in range(len(best_sol)):
            i = best_sol[i_k]
            final_starting_times[i] = str(max(r[i], offset))
            #print("Offset: " + str(start) + " " + " r_i: " + str(r[i]))
            #print(max(r[i], offset))
            offset = int(final_starting_times[i]) + p[i]
        for i_k in range(len(final_starting_times)):
            f.write(final_starting_times[i_k] + "\n")
        f.close()
    else:
        print("Solution not found")
        f = open(output, "w")
        f.write("-1")
        f.close()