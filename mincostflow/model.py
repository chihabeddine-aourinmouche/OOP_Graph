# -*- coding: utf-8 -*-
"""
    Model Builder
"""

from graph import Graph, Node, Edge

# typedef ∞
NA = 'NA'
NA_VALUE = 0


class Model(object):
    """
        Model
    """

    # Problem 2: Min cost flow assignment problem
    @staticmethod
    def get_input_cost_matrix():
        """ Initilize Cost Matrix
        """

        cost_matrix = [[90, 76, 75, 70, 50, 74, 12, 68],\
                        [35, 85, 55, 65, 48, 101, 70, 83],\
                        [125, 95, 90, 105, 59, 120, 36, 73],\
                        [45, 110, 95, 115, 104, 83, 37, 71],\
                        [60, 105, 80, 75, 59, 62, 93, 88],\
                        [45, 65, 110, 95, 47, 31, 81, 34],\
                        [38, 51, 107, 41, 69, 99, 115, 48],\
                        [47, 85, 57, 71, 92, 77, 109, 36],\
                        [39, 63, 97, 49, 118, 56, 92, 61],\
                        [47, 101, 71, 60, 88, 109, 52, 90]]

        return cost_matrix

    @staticmethod
    def gen_task_asgmt_graph(cost_matrix=None, task_capacity=1):
        """ Min cost flow assignment problem
            10 people and 8 tasks
        """

        list_nodes = []
        person_nodes = {}
        task_nodes = {}

        # Add source node and destination node to the list
        node_s = Node("s")
        node_g = Node("t")
        list_nodes.append(node_s)

        #
        n_persons = len(cost_matrix)
        n_tasks = len(cost_matrix[0])

        # Creat nodes
        for i in range(0, n_persons):
            # Create new vertex
            node_name = "p" + str(i)
            node = Node(node_name)

            # Add vertex to queue
            person_nodes[i] = node

            # Add person to the tail of the list
            list_nodes.append(node)

        # Create task nodes
        for j in range(0, n_tasks):
            task_name = "task" + str(j)
            node_task = Node(task_name)
            task_nodes[j] = node_task

            list_nodes.append(node_task)

        # Add adjacency vertices to nodes
        for i, node_p in person_nodes.items():

            # Add outgoing edge from source vertex to new vertex
            edge_src_v = Edge(node_s, node_p, 0, 0, 1)
            node_s.add_neighbor(edge_src_v)

            # Add adjancy vertices to the vertex p
            for j, node_t in task_nodes.items():
                # Edge from vertex p to vertex t
                edge_pt = Edge(node_p, node_t, cost_matrix[i][j], 0, 1)
                node_p.add_neighbor(edge_pt)

        # Add adjancy vertices to the vertex p
        for j, node_t in task_nodes.items():
            # Edge from vertex p to vertex t
            edge_t_g = Edge(node_t, node_g, 0, 0, task_capacity)
            node_t.add_neighbor(edge_t_g)

        # Create graph model from list of nodes
        list_nodes.append(node_g)
        graph = Graph(list_nodes)

        return graph, node_s, node_g, task_nodes, n_persons, n_tasks

    # Problem 1: Max flow problem
    # Problem 3: Min cost flow problem
    @staticmethod
    def __get_input_max_flow():
        """ Input Max Flow problem 1
        """

        # Converting integer list to string list
        start_nodes = [str(x) for x in [0, 0, 0, 1, 1, 2, 2, 3, 3]]
        end_nodes = [str(x) for x in [1, 2, 3, 2, 4, 3, 4, 2, 4]]
        capacities = [20, 30, 10, 40, 30, 10, 20, 5, 20]
        unit_costs = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        return start_nodes, end_nodes, capacities, unit_costs

    @staticmethod
    def __get_input_mincost_flow():
        """ Min cost flow problem 3
        """

        # Converting integer list to string list
        start_nodes = [str(x) for x in [0, 0, 1, 1, 1, 2, 2, 3, 4]]
        end_nodes = [str(x) for x in [1, 2, 2, 3, 4, 3, 4, 4, 2]]
        capacities = [15, 8, 20, 4, 10, 15, 4, 20, 5]
        unit_costs = [4, 4, 2, 2, 6, 1, 3, 2, 3]

        return start_nodes, end_nodes, capacities, unit_costs

    @staticmethod
    def __transform_input_tolist(start_nodes, end_nodes, capacities, unit_costs, extra_info=None):
        """ Transform raw input to match the structure of graph modelling
        """

        # Add a source s links to node 0 with a capacity
        if extra_info:
            start_nodes += extra_info['ext_start_v']
            end_nodes += extra_info['ext_end_v']
            capacities += extra_info['ext_capacities']
            unit_costs += extra_info['ext_unit_costs']

        return zip(start_nodes, end_nodes, capacities, unit_costs), set(start_nodes + end_nodes)

    @staticmethod
    def __gen_graph(matrix_graph=None, label_nodes=None, start_node=None, goal_node=None):
        """ Min cost flow assignment problem
            10 people and 8 tasks
        """

        # Add source node and destination node to the list
        list_nodes = []

        # Creat nodes
        nodes = {}
        for label in label_nodes:
            # Create new vertex
            node_name = str(label)
            node = Node(node_name)

            # Add vertex to queue
            nodes[node_name] = node

            # Add person to the tail of the list
            list_nodes.append(node)

        # Add adjacency vertices to nodes
        for (s_node, e_node, capacity, weight) in matrix_graph:

            # Add outgoing edge from source vertex to new vertex
            # if e_node != NA:
            edge_src_v = Edge(nodes[s_node], nodes[e_node], weight, 0, capacity)
            nodes[s_node].add_neighbor(edge_src_v)

        # Create graph model from list of nodes
        graph = Graph(list_nodes)

        # return object graph, object start_node, object goal_node
        return graph, nodes[start_node], nodes[goal_node]

    @staticmethod
    def gen_maxflow_graph(start_node=None, goal_node=Node):
        """ Min cost flow assignment problem
            10 people and 8 tasks
        """

        # Return graph information
        start_nodes, end_nodes, capacities, unit_costs = Model.__get_input_max_flow()
        matrix_graph, label_nodes = Model.__transform_input_tolist(start_nodes, end_nodes,\
            capacities, unit_costs)
        graph, start_node, goal_node = Model.__gen_graph(matrix_graph, label_nodes, start_node, goal_node)

        # return object graph, object start_node, object goal_node
        return graph, start_node, goal_node

    @staticmethod
    def gen_mincost_flow_graph(start_node=None, goal_node=Node):
        """ Min cost flow assignment problem
            10 people and 8 tasks
        """

        # Add a source s links to node 0 with a capacity 20,
        # and a sink t with arc (3,t) with capacity 5 and arc (4,t) with capacity 15
        # Add an arc (t,s)
        extra_info = {
            'ext_start_v': [str(x) for x in ['s', 3, 4]],
            'ext_end_v': [str(x) for x in [0, 't', 't']],
            'ext_capacities': [20, 5, 15],
            'ext_unit_costs': [0, 0, 0]
        }

        # extra_info = {
        #     'ext_start_v': [str(x) for x in ['s', 3, 4, 't']],
        #     'ext_end_v': [str(x) for x in [0, 't', 't', 's']],
        #     'ext_capacities': [20, 5, 15, NA_VALUE],
        #     'ext_unit_costs': [0, 0, 0, NA_VALUE]
        # }

        # Return graph information
        start_nodes, end_nodes, capacities, unit_costs = Model.__get_input_mincost_flow()
        matrix_graph, label_nodes = Model.__transform_input_tolist(start_nodes, end_nodes,\
            capacities, unit_costs, extra_info)
        graph, start_node, goal_node = Model.__gen_graph(matrix_graph, label_nodes, start_node, goal_node)

        # return object graph, object start_node, object goal_node
        return graph, start_node, goal_node

# if __name__ == "__main__":
#     # model_graph, _, _ = Model.generate()
#     model_graph, _, _ = Model.gen_mincost_flow_graph('s', 't')
#     model_graph, _, _ = Model.gen_maxflow_graph(start_node='0', goal_node='4')

#     print(model_graph.__str__())
