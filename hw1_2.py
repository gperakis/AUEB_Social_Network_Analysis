import snap
import random
import time


def generate_graph(n_nodes=50, out_degree=None, seed=1):
    """
    This method generates a Graph based on the Barabasi Algorithm and computes several metrics:
    1) It finds the Node with the maximum Degree.
    2) It finds the Node with the maximum PageRank Score.
    3) Calculates communities within the graph by using two different algorithms:
        a) Girvan - Newman community Detection
        b) Clauset-Newman-Moore community Detection.
        
    :param n_nodes: int. Specifies the number of nodes for the graph to be created.
    :param out_degree: int. Specifies the outer degree for each node. If None, then a random integer is generated
                            between 5 and 20.
    :param seed: Int. An integer that is used to generate the same 'random' integer for the out degree.
    :return: Boolean. Whether the execution time of the specific community detection algorithms is over 10 minutes.
    """

    if out_degree is None:
        random.seed(seed)
        out_degree = random.randint(5, 20)

    print
    print "Generating Graph with %s Nodes of Out Degree: %s " % (n_nodes, out_degree)

    # Generating a random graph based on the Barabasi Algorithm.
    barabasi_graph = snap.GenPrefAttach(n_nodes, out_degree)

    # Finding the node ID with the maximoun Degree.
    maximum_degree_node = snap.GetMxDegNId(barabasi_graph)

    # Iterating in the graph nodes in order to find the Maximum degree for this particular node.
    for NI in barabasi_graph.Nodes():
        if NI.GetId() == maximum_degree_node:
            print "Node: %d, Maximum Degree %d" % (NI.GetId(), NI.GetDeg())

    # Computing the PageRank score of every node in Graph

    # Setting the ID and the PageRank score to -1. (minimum of both of these is 0)
    page_rank_id, page_rank_score = -1, -1

    # Creating the iterator for the PageRank algorithm.
    PRankH = snap.TIntFltH()
    # Calculating the PageRank for every Node.
    snap.GetPageRank(barabasi_graph, PRankH)

    # By iterating on each node we find the Node with the maximum PageRank Score.
    for node in PRankH:
        if PRankH[node] > page_rank_score:
            page_rank_score = PRankH[node]
            page_rank_id = node

    print
    print "Node with the Highest PageRank value: "
    print "Node: %s, PageRank value %s " % (page_rank_id, page_rank_score)
    print

    try:
        start_Girvan_Newman = time.time()  # setting the timer for the first community detection algorithm.

        # Calculating Girvan - Newman community Detection Algorithm
        CmtyV = snap.TCnComV()
        snap.CommunityGirvanNewman(barabasi_graph, CmtyV)
        print 'Girvan-Newman community Detection Algorithm: Execution Time: ', time.time() - start_Girvan_Newman

        # Calculating Girvan-Newman community Detection Algorithm
        start_Clauset_Newman_Moore = time.time()  # setting the timer for the second community detection algorithm.
        CmtyV = snap.TCnComV()
        snap.CommunityCNM(barabasi_graph, CmtyV)
        print 'Clauset-Newman-Moore community Detection Algorithm: Execution Time: ', time.time() - start_Clauset_Newman_Moore

        print '-' * 100
        print '-' * 100

        if time.time() - start_Girvan_Newman > 10 * 60:  # if the total execution time for both algorithms is over 10
            # minutes then return False in order to quit the loop that this method will be used in.
            return False

        return True

    except MemoryError:  # if we get a memory error during the Community Detection algorithms we set to False in order
        # to avoid adding more Nodes when running this method in a while loop.
        return False


if __name__ == '__main__':

    # Instantiating the nodes.
    n_graph_nodes = 50
    run_graph = True

    while run_graph:
        # The output of this method is Boolean. This output defines whether we will continue to add Nodes in the
        # graph, or we reached the limit that we wanted for the exercise.
        run_graph = generate_graph(n_nodes=n_graph_nodes, out_degree=None, seed=1)
        n_graph_nodes += 25
