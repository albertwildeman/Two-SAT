from KosarajuLib import kosaraju
import numpy as np


def two_sat(n_variables, clauses):
    # Determines the existence of a solution to a 2-sat problem, using Kosaraju's algorithm
    # to determine the strongly connected components of the equivalent graph.

    n_clauses = clauses.shape[0]

    # Set the number of nodes and vertices of the directed graph (2 for each variable and clause, respectively).
    n_nodes = n_variables * 2
    n_edges = n_clauses * 2

    # Initialize the edge list of the graph o be constructed
    edges = np.zeros((n_edges, 2), dtype = int)

    # Fill the edge list
    for i_clause, clause in enumerate(clauses):
        # Two nodes per variable in the 2-sat problem. One with the same index as the index of the variable,
        # and one with the same index + the number of variables. The first will be for the variable being
        # True, the second for the variable being False. The edges will connect variable values(ie, nodes)
        # that are not allowed together as per a clause.

        # By default, assume the variable has a positive sign, and connect the edge to the
        #  corresponding negative node.
        clause_nodes = abs(clause) + n_variables

        # But, for each of the two variables,
        for i_var_in_clause in [0,1]:
            # If the sign of the variable in the clause is negative,
            if clause[i_var_in_clause] < 0:
                # connect the corresponding edge to the corresponding positive node
                clause_nodes[i_var_in_clause] = abs(clause[i_var_in_clause])

        # Add the edges to the edge list (one for each direction)
        edges[i_clause, :] = clause_nodes
        edges[i_clause + n_clauses, :] = clause_nodes[::-1]

    # Execute Kosaraju's SCC algorithm for the graph
    print("Kosaraju in progress...")
    leaders = kosaraju(edges)
    print("Kosaraju completed.")



    return False