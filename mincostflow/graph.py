# -*- coding: utf-8 -*-

"""
    Graph
"""

from queue import Queue


class Edge:
    """
        Edge E = (u, v)
    """

    def __init__(self, source, target, weight, flow, capacity):
        """ Initilization

        Parameters
        ----------
        source  : start node
        target  : goal node
        weight  : the weight of the edge from node u to node v
        flow    : the feasible flow from source to sink
            the flow is added while updating the residual graph
        capacity: the initial flow capacity along the edge
            the capacity will be updated once the edge is selected to send the flow
        """

        self.source = source
        self.target = target
        self.weight = weight
        self.flow = flow
        self.capacity = capacity

    def get_source(self):
        """ Get start node

        Return source node
        """

        return self.source

    def get_target(self):
        """ Get goal node

        Return target node
        """

        return self.target

    def get_weight(self):
        """ Get the weight of the edge

        Return weight of edge
        """

        return self.weight

    def get_flow(self):
        """ Get feasible flow of the edge
        At the beginning the flow is zero

        Return flow along the edge
        """

        return self.flow

    def get_capacity(self):
        """ Get the initial flow capacity along the edge

        Return capacity of edge
        """

        return self.capacity


class Node:
    """
        Graph Vertic
    """

    def __init__(self, name, visited=False):
        """ Initilization

        Parameters
        ----------
        name    : the label of the node
        visited : the status to indicate whether the node is already visited
            by default the visited is False
        """

        self.name = name
        self.visited = visited
        self.adjaceny_list = []

    def add_neighbor(self, edge):
        """ Add outgoing edges to the node
        we add the edge instead of adjacency node because the edge contains
        source node and neighbor node along with other neccesary information.

        Parameters
        ----------
        edge    : an outgoing edge
        """

        self.adjaceny_list.append(edge)

    def get_edges(self):
        """ Get all outgoing edges of the current node

        Return outgoing edges
            the outgoing edges is a list of object edges
        """

        return self.adjaceny_list

    def get_name(self):
        """ Get node's name

        Return the label of the node
            the label of the node is string
        """

        return self.name


class Graph:
    """
        Weighted graph G = (V)
    """

    def __init__(self, nodes):
        """ Initilization

        Parameters
        ----------
        nodes   : a list of nodes
            the node is list of nodes. The edge of the graph is not used since\
                each node has outgoing edges as adjancy list.
        """

        self.nodes = nodes

    def get_nodes(self):
        """ Get the list of all nodes

        Return Get list of nodes
        """

        return self.nodes

    def bfs_scan(self, start):
        """ Scan the vertices reachable from source in residual graph

            The objective is to find the subset A. Set A contains any vertices reachable from source.
            But it's disjoint from Set B which contains sink t.

            Paramaters
            ----------
                start : source vertex

            Returns
            -------
                visited : all visited vertices reachable from source vertex.
        """

        # Maintains a queue of visited candidate vertices
        # open_nodes is a FIFO queue
        open_nodes = Queue()

        # Keep tracking of visited nodes
        visited = set()
        # Mark the source node as visited and enqueue it
        # Start finding path from source, thus put vertex s in the queue
        open_nodes.put(start)

        # Add vertex u in visited listed
        start.visited = True
        visited.add(start)

        while not open_nodes.empty():

            # Pop vertex u from the queue
            node_u = open_nodes.get()
            # Get the outgoing edges (forward edges) of vertex u
            out_edges = node_u.get_edges()

            # Visit all neighbor vertices of vertex u
            for out_edge in out_edges:
                node_v = out_edge.get_target()
                # Check if there is still available feasible flow from vertex u to v
                # And node v is not the path yet
                if (not node_v.visited) and (out_edge.get_capacity() > 0):
                    # Mark node v as visited, and
                    # Add it to the tail of the queue
                    node_v.visited = True
                    open_nodes.put(node_v)

                    # Add vertex u in visited listed
                    visited.add(node_v)

        return visited

    def bfs(self, start, goal):
        """
            Returns path if there is a path from source 's' to sink 't' in
            residual graph.
        """

        # Maintains a queue of visited candidate vertices
        # open_nodes is a FIFO queue
        open_nodes = Queue()

        # Keep tracking of shortest path
        path = [start]
        # Mark the source node as visited and enqueue it
        # Start finding path from source, thus put vertex s in the queue
        open_nodes.put((start, path))

        while not open_nodes.empty():

            # Dequeue a vertice
            node_u, path = open_nodes.get()

            # Sort edges in non decreasing order
            out_edges = node_u.get_edges()

            # for edge in outgoing edges:
            for out_edge in out_edges:
                node_v = out_edge.get_target()
                # Check if there is still available feasible flow from vertex u to v
                # And node v is not the path yet
                if (node_v not in path) and (out_edge.get_capacity() > 0):

                    if node_v.get_name() == goal.get_name():
                        return path + [node_v]
                    else:
                        # Stores w in Q to further visit its neighbour
                        open_nodes.put((node_v, path + [node_v]))
        return None

    def find_bottleneck(self, path):
        """ Search for the minimum feasible flow in given Path

        Parameters
        ----------
        path   : an array of nodes from source to sink
            the node is list of nodes.

        Returns
        -------
        min_flow : the smallest feasible of any edges in the path
            min_float is float
        """

        min_flow = 0
        # Start from the second node since first node is the source node
        for i in range(1, len(path), 1):
            node_u = path[i - 1]
            node_v = path[i]

            # Outgoing edges from source node
            edges = node_u.get_edges()
            for edge in edges:
                if edge.get_target().get_name() == node_v.get_name():
                    flow = edge.get_capacity()
                    # Find the minimum between previous flow and current flow
                    if min_flow > 0:
                        min_flow = min(flow, min_flow)
                    else:
                        min_flow = flow

        # Return feasible flow of given path
        return min_flow

    def update_residual_graph(self, path):
        """ Update the Residual Graph

        Steps to update the residual graph
        1) Find Bottleneck from given path
        2) Build Residual Graph
            _ Update the outgoing arc owned by source and end (extremity)
            _ Update the incoming arc owned by (extremity) end and source

        Parameters
        ----------
        path   : an array of nodes from source to sink
            the path is the shortest path from source to sink. the path is a list.

        Returns
        -------
        feasible_flow : the smallest feasible flow can be sent along the path.
            feasible_flow is float. To gain the computing time, we return the feasible flow\
                after updating the residual graph.

        """

        # Determine the feasible flow along the path (bottleneck)
        feasible_flow = self.find_bottleneck(path)

        # Update the flow and capacity of graph
        # Start from the second node since first node is the source node
        for i in range(1, len(path), 1):
            node_u = path[i - 1]
            node_v = path[i]

            # Outgoing edges from source node
            out_edges = node_u.get_edges()
            for edge in out_edges:
                # Update flow and capacity of outgoing edge
                if edge.get_target().get_name() == node_v.get_name():
                    # Increase the flow of outgoing edge
                    edge.flow += feasible_flow
                    # Decrease the capacity of outgoing edge
                    edge.capacity -= feasible_flow

                    # Update flow and capacity of incoming edge
                    in_edges = edge.get_target().get_edges()
                    for in_edge in in_edges:
                        if in_edge.get_target().get_name() == node_u.get_name():
                            # Increase the capacity of incoming edge
                            in_edge.capacity += feasible_flow

        # Output feasbile flow
        return feasible_flow

    def calculate_path_weight(self, path):
        """
            Calculate the weight of given Path
        """

        graph_weight = 0
        # Start from the second node since first node is the source node
        for i in range(1, len(path), 1):
            source = path[i - 1]
            dest = path[i]

            # Get edges from source to dest
            edges = source.get_edges()
            for edge in edges:
                if edge.get_target().get_name() == dest.get_name():
                    graph_weight += edge.get_weight()

        return graph_weight

    def __str__(self):
        """
            Print out Graph
        """

        for _, node in enumerate(self.nodes):
            # print('%s: adjacent %d' % (node.get_name(), len(node.get_edges())))
            out_edges = node.get_edges()
            # if (out_edges is not None) or (len(out_edges) > 0):
            if out_edges:
                for _, edge in enumerate(out_edges):
                    # print('Node%s -> Node%s | weight: %4.2f | capacity: %4.2f | flow: %4.2f' %\
                    print('%s -> %s | weight: %4.2f | capacity: %4.2f | flow: %4.2f' %\
                                (edge.get_source().get_name(),\
                                    edge.get_target().get_name(),\
                                    edge.get_weight(),\
                                    edge.get_capacity(),\
                                    edge.get_flow()))
                    print("------------------------------------------------------------")
        return ""

    def show_saturated_edges(self):
        """
            Print out Graph
        """

        for _, node in enumerate(self.nodes):
            # print('%s: adjacent %d' % (node.get_name(), len(node.get_edges())))
            out_edges = node.get_edges()
            # if (out_edges is not None) or (len(out_edges) > 0):
            if out_edges:
                for _, edge in enumerate(out_edges):
                    if edge.get_capacity() == 0:
                        print('%s -> %s | weight: %4.2f | capacity: %4.2f | flow: %4.2f' %\
                                    (edge.get_source().get_name(),\
                                        edge.get_target().get_name(),\
                                        edge.get_weight(),\
                                        edge.get_capacity(),\
                                        edge.get_flow()))
                        print("------------------------------------------------------------")
        return ""

    def get_cutedges(self, setA):
        """ Get all the cut edges between vertices of the two sets
        """

        cut_edges = {
            'weights': [],
            'edges': []
        }

        for node in setA:
            # print('%s: adjacent %d' % (node.get_name(), len(node.get_edges())))
            out_edges = node.get_edges()
            if out_edges:
                for edge in out_edges:
                    if (edge.get_target() not in setA) and (edge.get_capacity() == 0):

                        # Add edge to list
                        cut_edges['weights'].append(edge.get_flow())
                        cut_edges['edges'].append(edge)

                        print('%s -> %s | weight: %4.2f | capacity: %4.2f | flow: %4.2f' %\
                                    (edge.get_source().get_name(),\
                                        edge.get_target().get_name(),\
                                        edge.get_weight(),\
                                        edge.get_capacity(),\
                                        edge.get_flow()))
                        print("------------------------------------------------------------")
        return cut_edges

    @staticmethod
    def init_graph():
        """
            Initialize Vertices and Edges of Graph
        """

        # Inititialze nodes
        node_1 = Node("1")
        node_2 = Node("2")
        node_3 = Node("3")
        node_4 = Node("4")
        node_5 = Node("5")
        node_6 = Node("6")

        # Initializes edges
        edge_01 = Edge(node_1, node_2, 1, 0, 16)
        edge_02 = Edge(node_1, node_3, 1, 0, 13)

        edge_12 = Edge(node_2, node_3, -1, 0, 10)
        edge_13 = Edge(node_2, node_4, 1, 0, 12)

        edge_21 = Edge(node_3, node_2, 1, 0, 4)
        edge_24 = Edge(node_3, node_5, 1, 0, 14)

        edge_32 = Edge(node_4, node_3, -2, 0, 9)
        edge_35 = Edge(node_4, node_6, 3, 0, 20)

        edge_43 = Edge(node_5, node_4, 1, 0, 7)
        edge_45 = Edge(node_5, node_6, 1, 0, 4)

        # Add the outgoing edges to each node
        node_1.add_neighbor(edge_01)
        node_1.add_neighbor(edge_02)

        node_2.add_neighbor(edge_13)
        node_2.add_neighbor(edge_12)

        node_3.add_neighbor(edge_21)
        node_3.add_neighbor(edge_24)

        node_4.add_neighbor(edge_32)
        node_4.add_neighbor(edge_35)

        node_5.add_neighbor(edge_43)
        node_5.add_neighbor(edge_45)

        # Prepare a list of nodes and pass to graph
        nodes = [node_1, node_2, node_3, node_4, node_5, node_6]

        # Set source node and goal node
        start = node_1
        goal = node_6

        return nodes, start, goal

    @staticmethod
    def init_graph_2():
        """
            Initialize Vertices and Edges of Graph
        """

        node_0 = Node("0")
        node_1 = Node("1")
        node_2 = Node("2")
        node_3 = Node("3")
        node_4 = Node("4")
        node_5 = Node("5")
        node_6 = Node("6")
        node_7 = Node("7")

        # Initializes edges
        edge_01 = Edge(node_0, node_1, 1, 0, 15)
        edge_02 = Edge(node_0, node_2, 1, 0, 10)

        edge_12 = Edge(node_1, node_2, 1, 0, 3)
        edge_13 = Edge(node_1, node_3, 1, 0, 6)

        edge_24 = Edge(node_2, node_4, 1, 0, 12)

        edge_35 = Edge(node_3, node_5, 1, 0, 4)
        edge_36 = Edge(node_3, node_6, 1, 0, 6)

        edge_46 = Edge(node_4, node_6, 1, 0, 6)

        edge_54 = Edge(node_5, node_4, 1, 0, 3)
        edge_57 = Edge(node_5, node_7, 1, 0, 10)

        edge_65 = Edge(node_6, node_5, 1, 0, 1)
        edge_67 = Edge(node_6, node_7, 1, 0, 5)

        # Add the outgoing edges to each node
        node_0.add_neighbor(edge_01)
        node_0.add_neighbor(edge_02)

        node_1.add_neighbor(edge_12)
        node_1.add_neighbor(edge_13)

        node_2.add_neighbor(edge_24)

        node_3.add_neighbor(edge_35)
        node_3.add_neighbor(edge_36)

        node_4.add_neighbor(edge_46)

        node_5.add_neighbor(edge_54)
        node_5.add_neighbor(edge_57)

        node_6.add_neighbor(edge_65)
        node_6.add_neighbor(edge_67)

        # Prepare a list of nodes and pass to graph
        nodes = [node_0, node_1, node_2, node_3, node_4, node_5, node_6, node_7]

        # Set source node and goal node
        start = node_0
        goal = node_7

        return nodes, start, goal

    @staticmethod
    def init_graph_td():
        """
            Initialize Vertices and Edges of Graph
        """

        node_0 = Node("0")
        node_1 = Node("1")
        node_2 = Node("2")
        node_3 = Node("3")
        node_4 = Node("4")
        node_5 = Node("5")
        node_6 = Node("6")

        # Initializes edges
        edge_01 = Edge(node_0, node_1, 5.8, 0, 16)
        edge_03 = Edge(node_0, node_3, 4.0, 0, 13)

        edge_12 = Edge(node_1, node_2, 4.6, 0, 5)
        edge_14 = Edge(node_1, node_4, 4.5, 0, 10)

        edge_23 = Edge(node_2, node_3, 5.8, 0, 5)
        edge_24 = Edge(node_2, node_4, 3.3, 0, 8)

        edge_32 = Edge(node_3, node_2, 6.0, 0, 10)
        edge_35 = Edge(node_3, node_5, 4.6, 0, 15)

        # edge_43 = Edge(node_4, node_3, 3.3, 0, 8)
        edge_46 = Edge(node_4, node_6, 7.2, 0, 25)

        edge_56 = Edge(node_5, node_6, 6.8, 0, 6)

        # Add the outgoing edges to each node
        node_0.add_neighbor(edge_01)
        node_0.add_neighbor(edge_03)

        node_1.add_neighbor(edge_12)
        node_1.add_neighbor(edge_14)

        node_2.add_neighbor(edge_23)
        node_2.add_neighbor(edge_24)

        node_3.add_neighbor(edge_32)
        node_3.add_neighbor(edge_35)

        node_4.add_neighbor(edge_46)

        node_5.add_neighbor(edge_56)

        # Prepare a list of nodes and pass to graph
        nodes = [node_0, node_1, node_2, node_3, node_4, node_5, node_6]

        # Set source node and goal node
        start = node_0
        goal = node_6

        return nodes, start, goal

    @staticmethod
    def init_graph_3():
        """
            Initialize Vertices and Edges of Graph
        """

        # Inititialze nodes
        node_0 = Node("0")
        node_1 = Node("1")
        node_2 = Node("2")
        node_3 = Node("3")
        node_4 = Node("4")

        # Initializes edges
        edge_01 = Edge(node_0, node_1, 1, 0, 20)
        edge_02 = Edge(node_0, node_2, 1, 0, 30)
        edge_03 = Edge(node_0, node_3, 1, 0, 10)

        edge_12 = Edge(node_1, node_2, 1, 0, 40)
        edge_14 = Edge(node_1, node_4, 1, 0, 30)

        edge_23 = Edge(node_2, node_3, 1, 0, 10)
        edge_24 = Edge(node_2, node_4, 1, 0, 20)

        edge_32 = Edge(node_3, node_2, 1, 0, 5)
        edge_34 = Edge(node_3, node_4, 1, 0, 20)

        # Add the outgoing edges to each node
        node_0.add_neighbor(edge_01)
        node_0.add_neighbor(edge_02)
        node_0.add_neighbor(edge_03)

        node_1.add_neighbor(edge_14)
        node_1.add_neighbor(edge_12)

        node_2.add_neighbor(edge_23)
        node_2.add_neighbor(edge_24)

        node_3.add_neighbor(edge_32)
        node_3.add_neighbor(edge_34)

        # Prepare a list of nodes and pass to graph
        nodes = [node_0, node_1, node_2, node_3, node_4]

        # Set source node and goal node
        start = node_0
        goal = node_4

        return nodes, start, goal

    @staticmethod
    def init_wieighted_graph():
        """
            Initialize Vertices and Edges of Graph
        """

        # Inititialze nodes
        node_0 = Node("0")
        node_1 = Node("1")
        node_2 = Node("2")
        node_3 = Node("3")
        node_4 = Node("4")

        node_s = Node("s")
        node_t = Node("t")

        # Initializes edges
        edge_s0 = Edge(node_s, node_0, 0, 0, 20)

        edge_01 = Edge(node_0, node_1, 4, 0, 15)
        edge_02 = Edge(node_0, node_2, 4, 0, 8)

        edge_12 = Edge(node_1, node_2, 2, 0, 20)
        edge_13 = Edge(node_1, node_3, 2, 0, 4)
        edge_14 = Edge(node_1, node_4, 6, 0, 10)

        edge_23 = Edge(node_2, node_3, 1, 0, 15)
        edge_24 = Edge(node_2, node_4, 3, 0, 4)

        edge_32 = Edge(node_3, node_4, 2, 0, 20)
        edge_42 = Edge(node_4, node_2, 3, 0, 5)

        edge_3t = Edge(node_3, node_t, 0, 0, 5)
        edge_4t = Edge(node_4, node_t, 0, 0, 15)

        # Add the outgoing edges to each node
        node_s.add_neighbor(edge_s0)

        node_0.add_neighbor(edge_01)
        node_0.add_neighbor(edge_02)

        node_1.add_neighbor(edge_13)
        node_1.add_neighbor(edge_12)
        node_1.add_neighbor(edge_14)

        node_2.add_neighbor(edge_23)
        node_2.add_neighbor(edge_24)

        node_3.add_neighbor(edge_32)
        node_3.add_neighbor(edge_3t)

        node_4.add_neighbor(edge_42)

        node_s.add_neighbor(edge_4t)

        # Prepare a list of nodes and pass to graph
        nodes = [node_s, node_0, node_1, node_2, node_3, node_4, node_t]

        # Set source node and goal node
        start = node_0
        goal = node_4

        return nodes, start, goal
