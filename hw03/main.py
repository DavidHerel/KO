#!/usr/bin/env python3
import math
import sys
from collections import deque

import numpy as np

#TODO
"""
TODO:
PSEUDO CODE
Udelam graf pro kazde dvojce co josu vedle sebe pr> f1 do f2, f2 do f3,....fp-1 do fp

Pro Kazdou tu dvojici sestavim graf takovy ze: dva nove uzele (s a t), na konci a na zacatku. A to tak ze pujde hrana do vsech F1 s low a up 1. To same pro t ale z F2 do t.
A mezi F1 a F2 bude kazdy s kazdym s l 0 a up 1. A cost bude euklid((x1,y1),(x2,y2)) DONE
1) Init feasable flow - transformace G do G' a na to FF DONE
2) Z init flow vyrobim residualni graf - pridam hrany (pro kazdou hranu pridam opacnou), predelam nove omezeni (costy - zaporny/kladny) DONE
3) Pustim na nej Belman forda (na ten res. graf) dokud nebudu mit negativni cykly (While true) - najde mi to zlepsujici cyklus, a zlepsujici velikost, (c a delta)
4) IF kdyz je delta 0 nebo mensi tak koncim cyklus
5) ELSE pokud je to vetsi tak pro kazdou hranu z cyklu updatnu jeji flow (jestli je dopredna nebo neni) prictu/odectu k ni deltta
"""
class Node:

    #input edges - number of input edges to node
    #output edges - number of output edges from node
    #my_id
    def __init__(self, input_edges, output_edges, my_id):
        self.balance = 0
        self.input_edges = input_edges
        self.my_id = my_id
        self.output_edges = output_edges

    def count_balance(self):
        sum_in = sum(e.lower_bound for e in self.input_edges)
        sum_out = sum(e.lower_bound for e in self.output_edges)
        return sum_in - sum_out

#class for Edge
class Edge:

    #init lower bound, flow, upper boud, from node, to node
    def __init__(self, lower_bound, flow, upper_bound, price, from_node, to_node, is_residual, pair_edge = None):
        self.used = False
        self.lower_bound = lower_bound
        self.flow = flow
        self.upper_bound = upper_bound
        self.price = price
        self.from_node = from_node
        self.to_node = to_node
        self.is_residual = is_residual
        self.pair_edge = pair_edge

class Graph:

    #graph has nodes and edges
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.starting_node = 0
        self.ending_node = len(self.nodes) - 1
        self.edges = edges
        self.max_flow = -1

    #insert edge to the graph - also modify input and output nodes
    def insert_edge(self, lower_bound, flow, upper_bound, price, from_node, to_node, is_residual):
        #create edge
        e = Edge(lower_bound, flow, upper_bound, price, from_node, to_node, is_residual)
        #put it into list
        self.edges.append(e)
        #modify this node stats
        self.nodes[to_node].input_edges.append(e)
        self.nodes[from_node].output_edges.append(e)

    def insert_edge(self, edge):
        self.edges.append(edge)

def solve(G, residual_G):
    while True:


if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #INPUT PHASE

    #open file from 1st argument
    f = open(input, "r")

    #read the first line of input file
    temp_data = list(map(int, f.readline().split()))
    #number of players
    players = temp_data[0]
    #number of frames
    frames = temp_data[1]

    # read frame
    prev_frame = list(map(int, f.readline().split()))

    #for every pair lets do this:
    for i in range(frames-1):
        # nodes= 2*n(for input and output node), and EDGES - empty
        nodes = []
        edges = []
        res_nodes = []
        res_edges = []
        for i in range(players + players):
            nodes.append(Node([],[], i))
            res_nodes.append(Node([],[], i))

        #make graph
        G = Graph(nodes, edges)
        residual_G = Graph(res_nodes, res_edges)

        #read second frame to ensure 2nd layer
        curr_frame = list(map(int, f.readline().split()))

        curr_cord = 0
        for node_index in range(players):
            #read line with coords
            x_coord = prev_frame[curr_cord]
            y_coord = prev_frame[curr_cord+1]

            curr_cord_second = 0
            for second_node_index in range(players, 2*players):

                #read line with coords
                x_coord_second = curr_frame[curr_cord_second]
                y_coord_second = curr_frame[curr_cord_second+1]

                #count distance = price
                dist = math.sqrt(pow(x_coord-x_coord_second, 2) + pow(y_coord-y_coord_second,2))

                flow = 0
                if (node_index + players == second_node_index):
                    flow = 1

                #add first layer edge
                e1 = Edge(0, flow, 1, dist, node_index, second_node_index, False)

                res_e1 = Edge(0, 0, 1-flow, dist, node_index, second_node_index, False)
                res_e2 = Edge(0, 0, flow, -1*dist, second_node_index, node_index, True)
                res_e1.pair_edge=res_e2
                res_e2.pair_edge=res_e1

                G.insert_edge(e1)
                residual_G.insert_edge(res_e1)
                residual_G.insert_edge(res_e2)

                curr_cord_second+=1

            curr_cord+=1

        #lets solve the graph
        solve(G, residual_G)

        prev_frame = curr_frame

    #close the file
    f.close()


    #if there does not exist solution
    if G is None:
        f = open(output, "w")
        f.write('-1')
        f.close()
    #exist:
    else:

        f = open(output, "w")
        #customers
        for i in range(1, C+1):
            #
            for e in G.nodes[i].output_edges:
                if e.flow > 0:
                    f.write(str(e.to_node-C) + " ")
            f.write("\n")
        f.close()
