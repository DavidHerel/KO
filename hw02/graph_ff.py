
class Node:

    #input edges - number of input edges to node
    #output edges - number of output edges from node
    #my_id
    def __init__(self, input_edges, output_edges, my_id):
        self.input_edges = input_edges
        self.output_edges = output_edges
        self.my_id = my_id

#class for Edge
class Edge:

    #init lower bound, flow, upper boud, from node, to node
    def __init__(self, lower_bound, flow, upper_bound, from_node, to_node):
        self.lower_bound = lower_bound
        self.flow = flow
        self.upper_bound = upper_bound
        self.from_node = from_node
        self.to_node = to_node

class Graph:

    #graph has nodes and edges
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.starting_node = 0
        self.ending_node = len(self.nodes) - 1

    #insert edge to the graph - also modify input and output nodes
    def insert_edge(self, lower_bound, flow, upper_bound, from_node, to_node):
        #create edge
        e = Edge(lower_bound, flow, upper_bound, from_node, to_node)
        #put it into list
        self.edges.append(e)
        #modify this node stats
        self.nodes[to_node].input_edges.append(e)
        self.nodes[from_node].output_edges.append(e)

