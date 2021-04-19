#!/usr/bin/env python3
import sys
from collections import deque

import numpy as np

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
    def __init__(self, lower_bound, flow, upper_bound, from_node, to_node):
        self.used = False
        self.lower_bound = lower_bound
        self.flow = flow
        self.upper_bound = upper_bound
        self.from_node = from_node
        self.to_node = to_node

class Graph:

    #graph has nodes and edges
    def __init__(self, nodes, edges):
        #self.adj_matrix = adj_matrix
        #BULLSHIT - make it as classes - no matrixes - no c
        self.nodes = nodes
        self.starting_node = 0
        self.ending_node = len(self.nodes) - 1
        self.edges = edges
        self.max_flow = -1

    #insert edge to the graph - also modify input and output nodes
    def insert_edge(self, lower_bound, flow, upper_bound, from_node, to_node):
        #create edge
        e = Edge(lower_bound, flow, upper_bound, from_node, to_node)
        #put it into list
        self.edges.append(e)
        #modify this node stats
        self.nodes[to_node].input_edges.append(e)
        self.nodes[from_node].output_edges.append(e)

    def bfs_walk(self, G):
        visited = [False] * len(G.nodes)
        queue = deque()
        queue.append(G.nodes[0])
        visited[0] = True
        path_flow = np.inf

        before = [0] * len(G.nodes)
        edges_arr = [None] * len(G.nodes)
        forward_backward = ['None'] * len(G.nodes)
        curr_path = []
        while queue:
            curr_node = queue.popleft()

            for edge in curr_node.input_edges:
                if not visited[edge.from_node] and edge.lower_bound < edge.flow:
                    queue.append(G.nodes[edge.from_node])
                    visited[edge.from_node] = True

                    before[edge.from_node] = edge.to_node
                    edges_arr[edge.from_node] = edge
                    forward_backward[edge.from_node] = 'B'

            for edge in curr_node.output_edges:
                if not visited[edge.to_node] and edge.upper_bound > edge.flow:
                    queue.append(G.nodes[edge.to_node])
                    visited[edge.to_node] = True

                    before[edge.to_node] = edge.from_node
                    edges_arr[edge.to_node] = edge
                    forward_backward[edge.to_node] = 'F'

            if visited[len(G.nodes) - 1]:
                break

        edge = edges_arr[len(G.nodes) - 1]
        f_b = forward_backward[len(G.nodes) - 1]
        bef = before[len(G.nodes) - 1]
        f_b_flow = []
        curr_path = []
        while edge is not None:
            if f_b == 'F':
                cap = edge.upper_bound - edge.flow
                path_flow = min(path_flow, cap)
                curr_path.append(edge)
                f_b_flow.append('F')
            elif f_b == 'B':
                cap = edge.flow - edge.lower_bound
                path_flow = min(path_flow, cap)
                curr_path.append(edge)
                f_b_flow.append('B')

            edge = edges_arr[bef]
            f_b = forward_backward[bef]
            bef = before[bef]

        if curr_path != []:
            for i in range(len(curr_path)):
                if (f_b_flow[i] == 'B'):
                    curr_path[i].flow = curr_path[i].flow - path_flow
                else:
                    curr_path[i].flow = curr_path[i].flow + path_flow

            return True
        return False

"""  
    if not visited[len(G.nodes)-1]:
        return 0, path_to


    path_flow = np.inf
    parent, edge, direction, capacity = path_to[len(G.nodes)-1]
    while edge:
        path_flow = min(path_flow, capacity)
        path.append((edge, direction))
        parent, edge, direction, capacity = path_to[parent]
    """
def edmonds_karp_algorithm(G):
    while True:
        #make walks
        if (not G.bfs_walk(G)):
            break
    return G


def solve_flow(G, extended_G):
    #go through every node in a graph, append starting by 1 cuz we will append it to extended_G (like in video)
    for i in range(len(G.nodes)):
        value = G.nodes[i].count_balance()

        #like in video
        if value < 0:
            # from current node to new t dot end
            extended_G.insert_edge(0, 0, -1 * value, i + 1, len(extended_G.nodes) - 1)
        else:
            # from s dot into current node
            extended_G.insert_edge(0, 0, value, 0, i + 1)

    # check corectness of algorithm
    extended_G = edmonds_karp_algorithm(extended_G)

    #STEP 2) Does it saturate?
    # is the solution correct?
    for edge in extended_G.nodes[0].output_edges:
        if edge.flow != edge.upper_bound:
            return None

    #STEP 3)
    # set flow in the original graph
    for original_graph, extended_graph in zip(G.edges, extended_G.edges):
        original_graph.flow = extended_graph.flow + original_graph.lower_bound

    #last run of FF
    G = edmonds_karp_algorithm(G)
    return G

if  __name__ == '__main__':
    #take 2 arguments (input and output)
    input, output = sys.argv[1], sys.argv[2]

    #INPUT PHASE

    #open file from 1st argument
    f = open(input, "r")

    #read the first line of input file
    temp_data = list(map(int, f.readline().split()))
    C = temp_data[0]
    P = temp_data[1]

    # nodes= C+P +2 (for input and output node), and EDGES - empty
    nodes = []
    edges = []
    edges_ext = []
    nodes_ext = []
    for i in range(C + P + 2):
        nodes.append(Node([],[], i))
        nodes_ext.append(Node([], [], i))

    G = Graph(nodes, edges)
    extended_G = Graph([Node([],[], -1)] + nodes_ext + [Node([],[], len(G.nodes)+2)], edges_ext)
    #starting 1 layer of the graph:
    #we starting with 1, cuz 0 is starting node
    for c in range(1, C + 1):
        #read line with customer
        temp_data = list(map(int, f.readline().split()))
        lower_bound = temp_data[0]
        upper_bound = temp_data[1]

        # source is 0, because it is connected to starting node, c is our number given to a customer
        G.insert_edge(lower_bound, 0, upper_bound, 0, c)
        extended_G.insert_edge(0, 0, upper_bound-lower_bound, 1, c+1)

        # connect customer to 2nd layer where he will connect to every product he does own
        for i in range(2, len(temp_data)):
            # from customer to product, also upper bound is 1, cuz customer can review product only once
            G.insert_edge(0, 0, 1, c, temp_data[i]+C)
            extended_G.insert_edge(0,0,1, c+1, temp_data[i]+C+1)


    temp_data = list(map(int, f.readline().split()))
    #last layer of the GRAPH, products are connected to 1 output node
    #starting with p = C+1
    start = C + 1
    for i in range(len(temp_data)):
        #lb = reviews needed, flow 0, upper bound is INT MAX, from product to output NODE - which is last node = C+P+1
        G.insert_edge(temp_data[i], 0, np.inf, start, C+P+1)
        extended_G.insert_edge(0, 0, np.inf-temp_data[i], start+1, C+P+1+1)
        start+=1

    #close the file
    f.close()
    #from prev last node to to prev input node (that cycle like from video)
    extended_G.insert_edge(0, 0, np.inf, len(extended_G.nodes)-1-1, 1)

    #PROCESSING PHASE
    #now we have graph ready and lets go baby
    G = solve_flow(G, extended_G)

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
