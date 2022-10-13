from typing import Dict, List, Union, cast
import graphviz
import json
from os.path import join, dirname, exists
from os import mkdir

IMAGEDIR = join(
    dirname(dirname(dirname(__file__))), "out"
)  # /../../../out aka prereq-flowchart/out/


def read_data(filename: str) -> List[Dict[str, Union[str, List[str]]]]:
    with open(filename, "r") as f:
        return cast(List[Dict[str, Union[str, List[str]]]], json.load(f))


def simple_graph() -> graphviz.Digraph:
    retGraph = graphviz.Digraph(
        "wide",
        node_attr={"color": "darkgoldenrod1", "style": "filled"},
    )
    retGraph.edges(("0", str(i)) for i in range(1, 10))
    return retGraph


def data_graph(data: List[Dict[str, Union[str, List[str]]]]) -> graphviz.Digraph:
    retGraph = graphviz.Digraph(
        "wide",
        node_attr={
            "color": "darkgoldenrod1",
            "style": "filled",
            "shape": "invhouse",
            "fontname": "Century Gothic Bold",
        },
    )
    for node in data:
        for prereq in node["Prereqs"]:
            retGraph.edge(prereq, node["Classname"])
    return retGraph


if __name__ == "__main__":
    print("Test Successful")
    if not exists(IMAGEDIR):
        mkdir(IMAGEDIR)
    data_graph(read_data(join(dirname(__file__), "dummy_data.json"))).render(
        join(IMAGEDIR, "Graph1")
    )
