# -*- coding: utf-8 -*-

"""
    Shortest Path Fast Algorithm (SPFA)
"""

from queue import Queue
from collections import deque

# typedef ∞
INF = float('Inf')


class SPFA(object):
    """
        SPFA algorithm finds the shortest path from s, to each vertex v, in the graph.
    """

    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal

    def initialization(self):
        """ Initialize distance to each and every vertex in given graph
        """

        # The length of the shortest path from s, to v is stored in d(v)
        dist = {}
        # Predecessor: To find the path from source (the one which update the distance)
        pred = {}

        # Initialize infinite distance from source to v
        # for node, _ in self.graph.get_nodes().items():
        for node in self.graph.get_nodes():
            # d(v)← ∞, forall v ∈ V
            dist[node] = INF
            # π(v)←nil, forall v ∈ V
            pred[node] = None
        # d(s) <- 0
        dist[self.start] = 0

        return dist, pred

    def relax(self, dist, pred, node_u, dist_u, node_v, cost_uv):
        """ Update the distance from vertex u to v

        Parameters
        ----------
        dist   : an array of distance of each node from source
        pred   : an array of predeccesor which points to (previous-hop) vertex of
            the current vertex. it traces the shortest route to the source from the current vertex.
        node_u : vertex u
        dist_u : the weight of path from source to vertex u
        node_v : vertex v
        cost_uv: the weight of edge {u,v}

        Returns
        -------
        dist  : the update distance from source to vertex v passing through vertex u.
            dist is list of float.
        pred  : mark vertex u as the predeccesor of vertex v
            if new distance of vertex v is shorter
        """

        # Use vertex u to relax its adjacent vertice v
        # if d(u) + w(u, v) < d(v)
        # then d(v) <- d(u) + w(u, v)
        if dist_u + cost_uv < dist[node_v]:
            dist[node_v] = dist_u + cost_uv
            pred[node_v] = node_u

        return dist, pred

    def spfa_scan(self, dist, pred):
        """ Scan the graph and Relax vertices

        To avoid blindly relax the adjacent vertices of the candidate vertex,
        SPFA adds a vertex to the queue only if that vertex is relaxed

        Parameters
        ----------
        dist   : an array of distance of each node from source
        pred   : an array of predeccesor which points to (previous-hop) vertex of the current vertex.
            it traces the shortest route to the source from the current vertex.

        Returns
        -------
        dist  : the update distance from source to vertex v passing through vertex u.
            dist is list of float.
        pred  : mark vertex u as the predeccesor of vertex v
            if new distance of vertex v is shorter
        """

        # Maintains a queue of visited candidate vertices
        # open_nodes is a FIFO queue
        open_nodes = Queue()
        # Start finding path from source, thus put vertex s in the queue
        open_nodes.put(self.start)
        self.start.visited = True

        # To avoid infinite loop in case of negative cycle,
        # Counter: to record the number of times a vertex has been relaxed and
        # Exit path search once some vertices got relaxed (|v|) times
        icount = {}
        # Number of vertices v (|v|)
        n_nodes = len(list(self.graph.get_nodes()))

        while not open_nodes.empty():

            # Pop the first vertex from the queue, then
            # Remove it from visited list
            node_u = open_nodes.get()
            node_u.visited = False
            # Neighbors of vertex u
            out_edges = node_u.get_edges()

            # For each successor m:
            for out_edge in out_edges:
                # Adjacent vertex of vertex u
                node_v = out_edge.get_target()
                # Check if there is still available feasible flow from vertex u to v
                if out_edge.get_capacity() > 0:

                    # Keep current distance of vertex before relaxing
                    temp_dist_v = dist[node_v]

                    # Update the distance of v through u
                    dist, pred = self.relax(dist, pred, node_u, dist[node_u], node_v, out_edge.get_weight())
                    # Adds vertex v to the queue only if that vertex is relaxed
                    if dist[node_v] < temp_dist_v:
                        # Put vertex in visited queue if it's not there
                        if (not node_v.visited) and (node_u not in open_nodes.queue):
                            open_nodes.put(node_v)
                            node_v.visited = True

                            # Keep tracking the number of times a vertex has been relaxed
                            if node_v not in icount:
                                icount[node_v] = 1
                            else:
                                icount[node_v] += 1

                            # There exists negative cycle if any vertex has been relaxed (|v|) times
                            if icount[node_v] > n_nodes:
                                return None, None

        return dist, pred

    def spfa(self):
        """ Find a shortest path from source

        The Shortest Path Faster Algorithm (SPFA)
        (SPFA) is an improvement of the Bellman–Ford algorithm which
        computes single-source shortest paths in a weighted directed graph.
        """

        # Initialize the distance to all vertices, and predecessor
        dist, pred = self.initialization()
        # Start shortest path scan
        dist, pred = self.spfa_scan(dist, pred)

        # If shortest found, then return None
        path = None
        if pred:
            path = self.build_path(pred)

        return path

    def build_path(self, pred):
        """ Build Path from predeccesor
        """

        # Path: store nodes of the shortest path in double-ended queue
        shortest_path = deque()

        # Set current node equal goal node
        c_vertex = self.goal

        # First, check if the goal node has been visited
        # and repeat checking if the predecessor node of goal node has been also visited
        # continue until we reach source node
        while pred[c_vertex] is not None:
            # Add c_vertex to the head of queue (the left side of the deque)
            shortest_path.appendleft(c_vertex)
            c_vertex = pred[c_vertex]

        # Add source node to the head of queue
        # The source node is not added to the predecessor list
        # as it has no parent node
        if shortest_path:
            shortest_path.appendleft(c_vertex)

        return shortest_path
