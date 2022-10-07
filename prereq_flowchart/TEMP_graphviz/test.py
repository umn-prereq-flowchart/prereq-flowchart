import graphviz
from os.path import join, dirname, exists
from os import mkdir

IMAGEDIR = join(
    dirname(dirname(dirname(__file__))), "out"
)  # /../../../out aka prereq-flowchart/out/


def simple_graph() -> graphviz.Digraph:
    retGraph = graphviz.Digraph("wide")
    retGraph.edges(("0", str(i)) for i in range(1, 10))
    return retGraph


if __name__ == "__main__":
    print("Test Successful")
    if not exists(IMAGEDIR):
        mkdir(IMAGEDIR)
    simple_graph().render(join(IMAGEDIR, "Graph1"))
