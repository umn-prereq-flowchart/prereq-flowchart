import graphviz
import os


def simple_graph() -> graphviz.Digraph:
    retGraph = graphviz.Digraph("wide")
    retGraph.edges(("0", str(i)) for i in range(1, 10))
    return retGraph


if __name__ == "__main__":
    print("Test Successful")
    simple_graph().render(os.path.join(os.path.dirname(__file__), "Graph1"))
