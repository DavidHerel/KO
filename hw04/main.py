#!/usr/bin/env python3
import math
import sys
from collections import deque

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

