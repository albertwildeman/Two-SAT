import numpy as np

def kosaraju(G):

    # Shift node numbers to start at 0
    G -= G.min()

    # Calculate finishing time for each node, that is, the order in which the second, forward, DFS loop will execute
    f = kosaraju_rev_dfs_loop(G[:, ::-1])

    # Reorder the nodes, in order of decreasing finishing time
    reordering = f.max() - f
    G_reordered = reordering[G]

    # Calculate the leader for each node
    leaders = kosaraju_fwd_dfs_loop(G_reordered)

    return leaders

def kosaraju_rev_dfs_loop(G):
    # Perform the first DFS (depth-first search) loop on the reverse of graph G

    # Buid an array holding the part of the edge list that is relevant for each node
    # To facilitate, first sort the edge list by sending node
    sortOrder = np.argsort(G[:, 0])
    G = G[sortOrder, :]
    # Get start and end indices within G for edges going out from each node
    G_idx = edge_offsets(G)

    # t is a counter that marks number of already-explored nodes.
    # It will be used to determine the processing order of the nodes for the
    # second (forward) DFS loop.
    t = 0

    # Get number of nodes from edge list G
    nNodes = G.max() + 1

    # initialize array that will hold the finishing times of all nodes
    f = np.zeros(nNodes, dtype=np.int32)

    # Initialize an array to keep track of which nodes have been explored
    explored = np.zeros(nNodes, dtype=np.bool)

    for iNode in range(nNodes):
        if not explored[iNode]:
            # call DFS, but with the rows (ie, direction) of the edge list reversed
            if iNode < 10:
                print("DFS_rev exploring node " + str(iNode))
            t = DFS_rev(G, G_idx, iNode, t, f, explored)

    return f


def edge_offsets(G):

    nNodes = G.max() + 1
    nEdges = G.shape[0]

    G_node = np.zeros((nNodes,2), dtype=np.int32)

    iNode = 0;
    for iEdge in range(nEdges):
        if G[iEdge,0] != iNode:
            G_node[iNode, 1] = iEdge
            iNode = G[iEdge,0]
            G_node[iNode,0] = iEdge

    G_node[iNode,1] = nEdges

    return G_node

def DFS_rev(G, G_idx, s, t, f, explored):

    stacksize = 1e7
    stack = np.zeros(stacksize, dtype=np.int32)
    stackexpl = np.zeros(stacksize, dtype=np.bool)

    stack[0] = s
    iStack = 0
    explored[s] = True

    while iStack >= 0:

        iNode = stack[iStack]

        if not stackexpl[iStack]:
            stackexpl[iStack] = True

            for targetNode in G[G_idx[iNode, 0]:G_idx[iNode, 1], 1]:
                if not explored[targetNode]:
                    explored[targetNode] = True

                    iStack += 1
                    if iStack >= stacksize:
                        raise NameError("Ran out of stack space")
                    stack[iStack] = targetNode
                    stackexpl[iStack] = False
        else:
            # stackexpl "true" number in implies need to process finishing time
            # Set finishing time for node just explored to the current "time" t
            f[iNode] = t
            # Increment t
            t += 1

            iStack -= 1

    return t


def kosaraju_fwd_dfs_loop(G):
    # Perform the second DFS (depth-first search) loop on the graph G

    # Buid an array holding the part of the edge list that is relevant for each node
    # To facilitate, first sort the edge list by sending node
    sortOrder = np.argsort(G[:, 0])
    G = G[sortOrder, :]
    # Get start and end indices within G for edges going out from each node
    G_idx = edge_offsets(G)

    # Get number of nodes from edge list G
    nNodes = G.max() + 1

    # initialize array that will hold the leaders of all nodes
    leaders = np.zeros(nNodes, dtype=np.int32)

    # Initialize an array to keep track of which nodes have been explored
    explored = np.zeros(nNodes, dtype=np.bool)

    for iNode in range(nNodes):
        if not explored[iNode]:
            # call DFS
            if iNode%10000==0:
                print("DFS_fwd exploring node " + str(iNode))

            DFS_fwd(G, G_idx, iNode, leaders, explored)

    return leaders


def DFS_fwd(G, G_idx, s, leaders, explored):

    stacksize = 1e7
    stack = np.zeros(stacksize, dtype=np.int32)

    stack[0] = s
    iStack = 0
    explored[s] = True

    while iStack >= 0:

        iNode = stack[iStack]
        leaders[iNode] = s

        iStack -= 1

        for targetNode in G[G_idx[iNode, 0]:G_idx[iNode, 1], 1]:
            if not explored[targetNode]:

                explored[targetNode] = True

                iStack += 1

                if iStack >=stacksize:
                    raise NameError("Ran out of stack space")

                stack[iStack] = targetNode

