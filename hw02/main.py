#!/usr/bin/env python3
import sys
from collections import deque

from copy import deepcopy

from typing import *

#class for Edge
class Edge:

    #init lower bound, flow, upper boud, from node, to node
    def __init__(self, lower_bound, flow, upper_bound, from_node, to_node):
        self.lower_bound = lower_bound
        self.flow = flow
        self.upper_bound = upper_bound
        self.from_node = from_node
        self.to_node = to_node


class Node:

    #input edges - number of input edges to node
    #output edges - number of output edges from node
    def __init__(self, input_edges, output_edges):
        self.input_edges = input_edges
        self.output_edges = output_edges


class Graph:

    #graph has nodes and edges
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    #insert edge to the graph - also modify input and output nodes
    def insert_edge(self, lower_bound, flow, upper_bound, from_node, to_node):
        #create edge
        e = Edge(lower_bound, flow, upper_bound, from_node, to_node)
        #put it into list
        self.edges.append(e)
        #modify this node stats
        self.nodes[to_node].input_edges.append(e)
        self.nodes[from_node].output_edges.append(e)

    def get_first_and_last_node(self):
        return 0, len(self.nodes)-1

def ff_labeling(G):
    s, t = G.get_first_and_last_node()
    path_to = [(0, None, 0, 0)] * len(G.nodes)

    visited = {s}
    queue = deque([s])

    min_capacity = sys.maxsize
    path = []

    while queue:
        v = G.nodes[queue.popleft()]

        for edge in v.output_edges:
            target = edge.to_node
            if target not in visited and edge.flow < edge.upper_bound:
                path_to[target] = edge.from_node, edge, 1, edge.upper_bound - edge.flow
                queue.append(target)
                visited.add(target)

        for edge in v.input_edges:
            source = edge.from_node
            if source not in visited and edge.flow > edge.lower_bound:
                path_to[source] = edge.to_node, edge, -1, edge.flow - edge.lower_bound
                queue.append(source)
                visited.add(source)

        if t in visited:
            parent, edge, direction, capacity = path_to[t]
            while edge:
                min_capacity = min(min_capacity, capacity)
                path.append((edge, direction))
                parent, edge, direction, capacity = path_to[parent]

            break

    return min_capacity, path

def ff_algorithm(G):
    bottleneck, augmenting_path = ff_labeling(G)
    while augmenting_path:
        for e, direction in augmenting_path:
            e.flow += direction * bottleneck
        bottleneck, augmenting_path = ff_labeling(G)
    return G


def build_g_dot(G):
    G_dot = deepcopy(G)

    # add starting intput node and new ending input node
    G_dot.nodes = ([Node([],[])] + G_dot.nodes + [Node([],[])])

    # shift all existing edges
    for e in G_dot.edges:
        # shift indices - new source and target added
        e.to_node += 1
        e.from_node += 1

        # normalize bounds
        e.upper_bound -= e.lower_bound
        e.lower_bound, e.flow = 0, 0

    return G_dot

def solve_flow(G):
    # build another graph to have feasible flow
    G_dot = build_g_dot(G)
    first, last = G_dot.get_first_and_last_node()

    #from prev last node to to prev input node (that cycle like from video)
    G_dot.insert_edge(0, 0, sys.maxsize, last-1, first+1)

    #go through every node in a graph, append starting by 1 cuz we will append it to G_dot (like in video)
    for idx, v in enumerate(G.nodes, start=1):
        balance = sum(e.lower_bound for e in v.input_edges) - sum(e.lower_bound for e in v.output_edges)

        #like in video
        if balance >= 0:
            #from s dot into current node
            G_dot.insert_edge(0, 0, balance, first, idx)
        else:
            #from current node to new t dot end
            G_dot.insert_edge(0, 0, -1*balance, idx, last)

    # sanity check
    G_dot = ff_algorithm(G_dot)

    #STEP 2) Does it saturate?
    # is the solution correct?
    banned = [e for e in G_dot.nodes[first].output_edges if e.flow != e.upper_bound]
    if banned:
        return None

    #STEP 3)
    # set flow in the original graph
    for original, extended in zip(G.edges, G_dot.edges):
        original.flow = original.lower_bound + extended.flow

    #last run of FF
    return ff_algorithm(G)

if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #INPUT PHASE

    #open file from 1st argument
    f = open(input, "r")

    #read the first line of input file
    C, P = [int(x) for x in f.readline().split()]

    # nodes= C+P +2 (for input and output node), and EDGES - empty
    nodes = []
    edges = []
    for i in range(C + P + 2):
        nodes.append(Node([],[]))

    G = Graph(nodes, edges)

    #starting 1 layer of the graph:
    #we starting with 1, cuz 0 is starting node
    for c in range(1, C + 1):
        #read line with customer
        lower_bound, upper_bound, *products = [int(x) for x in f.readline().split()]

        # source is 0, because it is connected to starting node, c is our number given to a customer
        G.insert_edge(lower_bound, 0, upper_bound, 0, c)

        #connect customer to 2nd layer where he will connect to every product he does own
        for p in products:
            # increase product number
            p += C
            # from customer to product, also upper bound is 1, cuz customer can review product only once
            G.insert_edge(0, 0, 1, c, p)

    reviews_needed = [int(x) for x in f.readline().split()]
    #last layer of the GRAPH, products are connected to 1 output node
    #starting with p = C+1
    for p, reviews_needed in enumerate(reviews_needed, start=C + 1):
        #lb = reviews needed, flow 0, upper bound is INT MAX, from product to output NODE - which is last node = C+P+1
        G.insert_edge(reviews_needed, 0, sys.maxsize, p, C+P+1)

    #close the file
    f.close()

    #PROCESSING PHASE
    #now we have graph ready and lets go baby
    G = solve_flow(G)

    result=[]
    #if there exist solution
    if G:
        for v in G.nodes[1:C + 1]:
            reviews = sorted([e.to_node for e in v.output_edges if e.flow])
            result.append(' '.join([str(r - C) for r in reviews]))
    #if not
    else:
        result = ['-1']

    f = open(output, "w")
    f.writelines([f'{line}\n' for line in result if line])
    f.close()