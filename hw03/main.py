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
    def __init__(self, lower_bound, flow, upper_bound, price, from_node, to_node, is_residual, pair_edge = None, edge_id = None):
        self.used = False
        self.lower_bound = lower_bound
        self.flow = flow
        self.upper_bound = upper_bound
        self.price = price
        self.from_node = from_node
        self.to_node = to_node
        self.is_residual = is_residual
        self.pair_edge = pair_edge
        self.edge_id = edge_id

class Graph:

    #graph has nodes and edges
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.starting_node = 0
        self.ending_node = len(self.nodes) - 1
        self.edges = edges
        self.max_flow = -1
        self.adj_matrix = [[None for x in range(len(nodes)+1)] for y in range(len(nodes)+1)]

    #insert edge to the graph - also modify input and output nodes
    def insert_edge(self, lower_bound, flow, upper_bound, price, from_node, to_node, is_residual):
        #create edge
        e = Edge(lower_bound, flow, upper_bound, price, from_node, to_node, is_residual)
        #put it into list
        self.edges.append(e)
        #modify this node stats
        self.nodes[to_node].input_edges.append(e)
        self.nodes[from_node].output_edges.append(e)

        self.adj_matrix[from_node][to_node] = e

    def insert_edge(self, edge):
        self.edges.append(edge)
        self.adj_matrix[edge.from_node][edge.to_node] = edge

    def find_edge_by_id(self, id):
        for edge in self.edges:
            if (edge.edge_id == id):
                return edge
        print("Error in find edge by id function")
        return None

    def find_edges_by_id(self, id):
        edges_temp = []
        for edge in self.edges:
            if (edge.edge_id == id):
                edges_temp.append(edge)
        return edges_temp[0], edges_temp[1]

def bellman_ford(residual_G):
    dist, pred, edges = {}, {}, {}

    # create virtual source node
    source = '-1'
    dist[source] = 0

    for edge in residual_G.edges:
        if edge.upper_bound:
            str_from = f'{edge.from_node}'
            str_to = f'{edge.to_node}'
            # set distance to infinity
            dist[str_from], dist[str_to] = float('inf'), float('inf')
            # create valid residuals
            edges[(str_from, str_to)] = edge

            # introduce new edges from the start to the all vertices
            edges[(source, str_from)] = Edge(0, 0, 1, 0, -1, edge.from_node, False)
            edges[(source, str_to)] = Edge(0, 0, 1, 0, -1, edge.to_node, False)

    for _ in range(len(edges.keys()) - 1):
        for (u, v), edge in edges.items():
            #if (v == '4'):
                #print(str(dist[u]) + str(" ") + str(edge.price) + " " + str(dist[v]))
            if dist[u] + edge.price < dist[v]:
                dist[v] = dist[u] + edge.price
                pred[v] = u


    in_cycle = None
    for (u, v), edge in edges.items():
        if dist[u] + edge.price < dist[v]:
            in_cycle = v
            break

    # backtrack cycle
    if in_cycle:
        #print("pred")
        #print(pred)
        cycle = backtrack_cycle(pred, in_cycle)
        #print(len(cycle))
        return cycle_walk(cycle[0], cycle, residual_G)
    return 0, []

def backtrack_cycle(pred, start):
    cycle, cur = [start], pred[start]
    #print(len(cycle))
    while cur not in cycle:
        cycle.append(cur)
        #print(cur + " added to cycle")
        cur = pred[cur]
    #print(cycle)
    cycle_starts_idx = cycle.index(cur)
    #print(cur)
    #print(cycle_starts_idx)
    return cycle[cycle_starts_idx:][::-1]

def cycle_walk(first, cycle, residual_G):
    capacity, previous = float('inf'), first
    cycle.append(first)

    final = []
    for current in cycle[1:]:
        final.append((previous, current))
        #print("Do cyklu pridano: " + str(previous) + " " + str(current))
        capacity, previous = min(capacity, residual_G.adj_matrix[int(previous)][int(current)].upper_bound), current

    return capacity, final


def solve(G, residual_G):
    while True:
        delta, cycle = bellman_ford(residual_G)
        if (delta <= 0):
            break
        else:
            counter = 0
            #print(len(cycle))
            for (i, j) in cycle:
                #error maybe here
                #print(i, j)
                if G.adj_matrix[int(i)][int(j)] != None:
                    #print("jsem tu " + str(counter))
                    G.adj_matrix[int(i)][int(j)].flow += delta
                    counter+=1
                else:
                    G.adj_matrix[int(j)][int(i)].flow -= delta
                residual_G.adj_matrix[int(i)][int(j)].upper_bound -= delta
                residual_G.adj_matrix[int(j)][int(i)].upper_bound += delta
    return G

if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #INPUT PHASE

    #open file from 1st argument
    f = open(input, "r")
    f_output = open(output, "w")
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
        for node_index in range(1, players+1):
            #read line with coords
            x_coord = prev_frame[curr_cord]
            y_coord = prev_frame[curr_cord+1]

            curr_cord_second = 0
            for second_node_index in range(players+1, 2*players+1):

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
                e1.edge_id = curr_cord + curr_cord_second
                #print("coords 1: " + str(x_coord) + " " + str(y_coord))
                #print("coords 2: " + str(x_coord_second) + " " + str(y_coord_second))
                #print(dist)
                res_e1 = Edge(0, 0, 1-flow, dist, node_index, second_node_index, False)
                res_e2 = Edge(0, 0, flow, -1*dist, second_node_index, node_index, True)

                res_e1.pair_edge=res_e2
                res_e2.pair_edge=res_e1

                res_e1.edge_id = curr_cord + curr_cord_second
                res_e2.edge_id = curr_cord + curr_cord_second

                G.insert_edge(e1)
                residual_G.insert_edge(res_e1)
                residual_G.insert_edge(res_e2)

                curr_cord_second+=2

            curr_cord+=2

        #print("Edges number: " + str(len(G.edges)))
        #print("Residual edges number: " + str(len(residual_G.edges)))
        #lets solve the graph
        new_G = solve(G, residual_G)
        #print("Dostal jsem novej graf s number edges: " + str(len(new_G.edges)) )
        string_to_write = ""
        for edge in new_G.edges:
            if (edge.flow > 0):
                string_to_write+=str(edge.to_node-players) + " "

        print(string_to_write)
        f_output.write(string_to_write+"\n")
        prev_frame = curr_frame

    #close the file
    f.close()
    f_output.close()
