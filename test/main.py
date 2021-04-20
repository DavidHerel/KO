#!/usr/bin/env python3

import sys
import gurobipy as g
import string

if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #open file from 1st argument
    f = open(input, "r")

    #HANDLING DATA
    is_knight = [[False for y in range(8)] for x in range(8)]

    is_rook = [[False for y in range(8)] for x in range(8)]

    #read the string from the file, split it by space, map int() to every string - to make it int, and then wrap it as a list
    temp_data = list(map(int, f.readline().split()))
    rook_number = temp_data[0]
    rook_pos = []
    rook_pos_A = []
    rook_pos_B = []
    print(rook_number)
    for i in range(rook_number):
        pos = f.readline()
        rook_pos.append(pos)
        posA = ord(pos[0]) - 96
        posB = int(pos[1])
        rook_pos_A.append(posA)
        rook_pos_B.append(posB)
        print(posA)
        print(posB)
        is_rook[posA-1][posB-1] = True
    f.close()

    #SOLVER
    print(is_rook)
    m = g.Model()

    # All possible moves of a knight
    X_move = [2, 1, -1, -2, -2, -1, 1, 2];
    Y_move = [1, 2, 2, 1, -1, -2, -2, -1];

    M = 200
    constr_count = 0
    #jestli je na dane pozici knight nebo neni
    a = m.addVars(8, 8, vtype=g.GRB.BINARY)
    for x in range(0,8):
        for y in range(0,8):
            #it is not in rook pos
            if (not (x+1) in rook_pos_A) and (not (y+1) in rook_pos_B):
                #on all possible directions there are no other knights
                for i in range(8):
                    if (x+X_move[i] >= 0 and x+X_move[i] < 8 and y+Y_move[i] >= 0 and y+Y_move[i] < 8):
                        m.addConstr(a[x,y] >= a[x+X_move[i], y+Y_move[i]] +1 - M*(1 - a[x,y] ))
                        constr_count+=1

            else:
                m.addConstr(a[x, y] == 0)
                constr_count += 1
    #print(constr_count)
    m.setObjective(a.sum(), g.GRB.MAXIMIZE)
    m.optimize()

    # if result exists
    if m.Status == g.GRB.OPTIMAL:
        f = open(output, "a")
        # first round then convert to int
        result = int(round(m.objVal))
        print(result)
        f.write(str(result) + "\n")
        for x in range(0, 8):
            for y in range(0, 8):
                if a.sum(x,y).getValue() > 0.5:
                    print(str(chr(x+97)) + str(y+1))
                    f.write(str(chr(x+97)) + str(y+1)+"\n")