import unittest
import snap


def has_euler_path(graph):
    """
    This method checks whether an undirected SNAP graph has an euler path, and returns the 
    set of vertices that define the start and the end of the Eulerian path.
    :param graph: SNAP object. A precomputed undirected Graph.
    :return: tuple. (boolean, set). Whether the given graph has a Eulerian path and the aforementioned vertices.
    """

    # Gathering the Nodes with odd number of degree
    vertices = set(NI.GetId() for NI in graph.Nodes() if NI.GetDeg() % 2 != 0)

    # if there are more than 2 nodes with odd degree, then there is no Eulerian path.
    if len(vertices) == 2:
        return True, vertices
    else:
        return False, set()


def has_euler_circuit(graph):
    """
    This method checks whether an undirected SNAP graph has an euler circuit.
    
    :param graph: SNAP object. A precomputed undirected Graph.
    :return: Boolean.
    """
    # An undirected Eulerian circuit has no vertices of odd degrees
    for NI in graph.Nodes():
        if NI.GetDeg() % 2 != 0:
            return False

    # Must be connected
    if not snap.IsConnected(graph):
        return False

    return True


class TestEulerMethods(unittest.TestCase):
    """
    
    """

    def test_has_euler_path_but_not_circuit(self):
        """
        Creates and tests if a graph has an euler path without circuit.
        :return: 
        """
        graph = snap.TUNGraph.New()

        for i in range(1, 7):
            graph.AddNode(i)

        for i in range(1, 6):
            graph.AddEdge(i, i + 1)

        result, vertices = has_euler_path(graph)

        self.assertTrue(result)
        self.assertEqual(len(vertices), 2)

    def test_does_not_have_euler_path(self):
        """
        Creates a graph without Eurerian path and tests if a graph has an euler path without circuit.

        :return:
        """
        graph = snap.TUNGraph.New()

        for i in range(1, 8):
            graph.AddNode(i)

        for i in range(1, 6):
            graph.AddEdge(i, i + 1)

        graph.AddEdge(3, 7)

        result, vertices = has_euler_path(graph)

        self.assertFalse(result)
        self.assertEqual(len(vertices), 0)

    def test_has_euler_circuit(self):
        """
        Creates a Circular graph and tests if this graph has a Eurerian Circuit.
        :return:
        """

        graph = snap.GenCircle(snap.PUNGraph, 10000, 1)

        result = has_euler_circuit(graph)
        self.assertTrue(result)
        self.assertTrue(graph.GetNodes() >= 1000)

    def test_does_not_have_euler_circuit(self):
        """
        
        :return: 
        """

        graph = snap.TUNGraph.New()

        for i in range(1, 7):
            graph.AddNode(i)

        for i in range(1, 6):
            graph.AddEdge(i, i + 1)

        result = has_euler_circuit(graph)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()