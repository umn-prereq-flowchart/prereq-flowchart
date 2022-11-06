from typing import Dict, List, Union, cast
import graphviz
import json
from os.path import join, dirname, exists
from os import mkdir

IMAGEDIR = join(
    dirname(dirname(dirname(__file__))), "out"
)  # /../../../out aka prereq-flowchart/out/


def read_data(filename: str) -> List[Dict[str, Union[str, List[str]]]]:
    """Opens a json file and loads the data into a dictionary

    :param filename: a string refering to a filename
    :type filename: str
    :return: A list of dictionaries bound by string keys with values that can be either string lists or string literals.
    :rtype: List[Dict[str, Union[str, List[str]]]]
    """
    with open(filename, "r") as f:
        return cast(List[Dict[str, Union[str, List[str]]]], json.load(f))


def simple_graph() -> graphviz.Digraph:
    """Generates a default simple graph for testing if graphviz software is properly configured.
    The graph is not complex and should consist of 10 nodes all bound to one node with the text 0.

    :return: A graph object that must be rendered to create a pdf.
    :rtype: graphviz.Digraph
    """
    retGraph = graphviz.Digraph(
        "wide",
        node_attr={"color": "darkgoldenrod1", "style": "filled"},
    )
    retGraph.edges(("0", str(i)) for i in range(1, 10))
    return retGraph


def data_graph(data: List[Dict[str, Union[str, List[str]]]]) -> graphviz.Digraph:
    """Reads data and generates a file of classes given

    :param data: _description_
    :type data: List[Dict[str, Union[str, List[str]]]]
    :return: _description_
    :rtype: graphviz.Digraph
    """
    retGraph = graphviz.Digraph(
        "wide",
        edge_attr={"minlen": "2"},
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
    if not exists(IMAGEDIR):
        mkdir(IMAGEDIR)
    data_graph(read_data(join(dirname(__file__), "dummy_data.json"))).render(
        join(IMAGEDIR, "Graph1")
    )
    print("Test Successful")
