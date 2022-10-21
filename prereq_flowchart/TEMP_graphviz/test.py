from typing import Dict, List, Union, cast
import graphviz
import json
from os.path import join, dirname, exists
from os import mkdir

IMAGEDIR = join(
    dirname(dirname(dirname(__file__))), "out"
)  # /../../../out aka prereq-flowchart/out/

COLORS: List[str] = ["green4", "lightskyblue", "crimson"]
CREATED_NODES: Dict[str, str] = dict()


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


def mock_graph() -> graphviz.Digraph:
    """Creates a demonstration graph designed to show a theoretical interpretation of our end goal.

    :return: The graph object to be rendered.
    :rtype: graphviz.Digraph
    """
    retGraph = graphviz.Digraph(
        "wide",
        node_attr={
            "color": "darkgoldenrod1",
            "style": "filled",
            "shape": "invhouse",
            "fontname": "Century Gothic Bold",
        },
    )
    retGraph.edge("CSCI 4XXX", "CSCI 8XXX")
    retGraph.edge("RECC 2XXX", "CSCI 8XXX", style="dashed")
    retGraph.node(
        "COREC1 3XXX/COREC1 2XXX",
        shape="point",
        height="0.01",
        width="0.01",
        color="green4",
    )
    retGraph.edge("COREC1 3XXX", "COREC1 3XXX/COREC1 2XXX", color="green4", dir="none")
    retGraph.edge("COREC1 2XXX", "COREC1 3XXX/COREC1 2XXX", color="green4", dir="none")
    retGraph.edge("COREC1 3XXX/COREC1 2XXX", "CSCI 4XXX", color="green4")
    retGraph.node(
        "COREC2 3XXX/COREC2 2XXX",
        shape="point",
        height="0.01",
        width="0.01",
        color="lightskyblue",
    )
    retGraph.edge(
        "COREC2 3XXX", "COREC2 3XXX/COREC2 2XXX", color="lightskyblue", dir="none"
    )
    retGraph.edge(
        "COREC2 2XXX", "COREC2 3XXX/COREC2 2XXX", color="lightskyblue", dir="none"
    )
    retGraph.edge("COREC2 3XXX/COREC2 2XXX", "CSCI 4XXX", color="lightskyblue")
    return retGraph


def join_recs(
    graph: graphviz.Digraph,
    nodeName: str,
    prereq: Union[str, List[str]],
    reccomended: bool = False,
) -> None:
    """Creates paths and subnodes for pre-req and reccomended pre-req structures.

    :param graph: The graph that we need to modify
    :type graph: graphviz.Digraph
    :param nodeName: The name of the node we want to connect our points to
    :type nodeName: str
    :param prereq: If given a string it will create one edge between the two nodes. If given a list it
    will appropriately distinguish it by color and create a psuedo-node where the arrows will converge.
    :type prereq: Union[str, List[str]]
    :param reccomended: Makes the arrow dashed if it should be optional otherwise solid, defaults to False
    :type reccomended: bool, optional
    """
    style = "dashed" if reccomended else ""
    if type(prereq) == str:
        graph.edge(prereq, nodeName, style=style)
    else:
        mid_name = "/".join(prereq)
        if mid_name in CREATED_NODES:
            color = CREATED_NODES[mid_name]
        else:
            color = COLORS.pop(0)
            COLORS.append(color)
            CREATED_NODES[mid_name] = color
        graph.node(
            mid_name,
            shape="point",
            height="0.01",
            width="0.01",
            color=color,
        )
        graph.edge(
            mid_name,
            nodeName,
            color=color,
            style=style,
        )
        for coreq in prereq:
            graph.edge(
                coreq,
                mid_name,
                color=color,
                style=style,
                dir="none",
            )


def data_graph(data: List[Dict[str, Union[str, List[str]]]]) -> graphviz.Digraph:
    """Reads data and generates a file of classes given

    :param data: _description_
    :type data: List[Dict[str, Union[str, List[str]]]]
    :return: _description_
    :rtype: graphviz.Digraph
    """
    retGraph = graphviz.Digraph(
        "wide",
        strict=True,
        node_attr={
            "color": "darkgoldenrod1",
            "style": "filled",
            "shape": "invhouse",
            "fontname": "Century Gothic Bold",
        },
    )
    for node in data:
        for prereq in node["Pre-Reqs"]:
            join_recs(retGraph, cast(str, node["Classname"]), prereq)
        for reccomend in node["Reccomended"]:
            join_recs(
                retGraph, cast(str, node["Classname"]), reccomend, reccomended=True
            )

    return retGraph


if __name__ == "__main__":
    if not exists(IMAGEDIR):
        mkdir(IMAGEDIR)
    data_graph(read_data(join(dirname(__file__), "advanced_data.json"))).render(
        join(IMAGEDIR, "MockGraph")
    )
    print("Test Successful")
