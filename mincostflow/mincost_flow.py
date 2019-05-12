# -*- coding: utf-8 -*-

"""
    Minimum-cost flow
"""

from spfa import SPFA

# typedef ∞
INF = float('Inf')


class MinCostFlow(SPFA):
    """
        The objective of the minimum-cost flow problem (MCFP) is
        to find the cheapest possible way of sending a certain amount of flow
        through a flow network.
    """

    @staticmethod
    def sendflow():
        """
            Send max flow of a flow network with mininum cost
        """

        # Initial graph
        # g_nodes, start, goal = Graph.init_graph()
        # g_nodes, start, goal = Graph.init_graph_3()
        # g_nodes, start, goal = Graph.init_graph_2()
        # g_nodes, start, goal = Graph.init_graph_td()
        # g_nodes, start, goal = Graph.init_wieighted_graph()

        # graph = Graph(g_nodes)

        # Model
        # from model import Model
        # graph, start, goal = Model.generate()

        # from graph import Graph
        # g_nodes, start, goal = Graph.init_wieighted_graph_5()
        # g_nodes, start, goal = Graph.init_graph_2()
        # graph = Graph(g_nodes)

        # Model
        from model import Model
        graph, start, goal = Model.gen_mincost_flow_graph(start_node='0', goal_node='4')
        # graph, start, goal = Model.gen_maxflow_graph(start_node='0', goal_node='4')

        print("\n*** Graph *** \n")
        graph.__str__()

        # Initialize Mincost Flow
        mincost_flow = MinCostFlow(graph, start, goal)

        # Miximum Feasible Flow from source to sink
        max_flow = 0
        total_weight = 0

        # Find max flow in given graph until no more feasible flow
        while True:

            path = mincost_flow.spfa()

            # There exists a negative cycle
            if path is None:
                print("******************************")
                print("* There is a negative cycle. *")
                print("******************************")
                # Exit the loop
                break
            # No more feasible path to send flow
            elif not path:

                print("\n*** Residual Graph ***\n")
                graph.__str__()

                print("\n************************")
                print("* Max Flow is : ", max_flow, "   *")
                print("************************\n")

                break

            # temp_path = path
            total_weight += graph.calculate_path_weight(path)

            if max_flow == 0:
                print("\n*** Feasible Paths ***\n")

            from utils.info_printer import InfoPrinter
            InfoPrinter.printflow(graph, path)

            # *** How to Update the residual graph *** #
            # 1) Find Bottleneck from given path
            # 2) Build Residual Graph
            #   _ Update the outgoing arc owned by source and end (extremity)
            #   _ Update the incoming arc owned by (extremity) end and source
            # 3) Accumulate max flow from feasbile flow
            max_flow += graph.update_residual_graph(path)

if __name__ == "__main__":
    MinCostFlow.sendflow()