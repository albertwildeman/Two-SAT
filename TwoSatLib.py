from KosarajuLib import kosaraju
import random as rndm
import numpy as np



def two_sat_papadimitriou(n_variables, clauses, max_searches):

    # Set maximum allowable number of searches
    max_searches = 1
    # Set maximum allowable number of flips in a search
    max_flips = 2 * n_variables**2

    # get number of clauses
    n_clauses = clauses.shape[0]

    # initialize
    i_search = 0
    current_state_feasible = False

    while i_search < max_searches and not current_state_feasible:

        # Initialize state (st) variables to random initial guess
        st = [rndm.random() > 0.5 for x in range(n_variables)]

        n_flips = 0

        # Go over all the clauses, but do it in random order
        iter_range = list(range(n_clauses))
        rndm.shuffle(iter_range)

        while n_flips < max_flips and not current_state_feasible:

            # Check if state satisfies all clauses. Until proven otherwise, consider it correct.
            current_state_feasible = True

            # # Go over all the clauses, but do it in random order
            # iter_range = list(range(n_clauses))
            # rndm.shuffle(iter_range)
            for i_clause in iter_range:

                clause = clauses[i_clause]
                clause_variables = abs(clause)
                clause_signs = np.sign(clause)

                # If neither of the 2 variables match the clause, the current state is not feasible
                if (st[clause_variables[0]]>=0) != clause_signs[0] and (st[clause_variables[1]]>=0) != clause_signs[1]:

                    # Declare the current state not feasible
                    current_state_feasible = False

                    # Change the current state. Randomly pick either of the variables in the clause to flip.
                    variable_to_flip = clause_variables[ 1*(rndm.random()>0.5) ]
                    # flip it
                    st[variable_to_flip] = not st[variable_to_flip]

                    # Increment number of flips
                    n_flips += 1
                    break

        # Increment the number of searches performed
        i_search += 1

    return current_state_feasible

def two_sat_kosaraju(n_variables, clauses):
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