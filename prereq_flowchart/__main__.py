import argparse
import sys

from os.path import exists, join

from prereq_flowchart.TEMP_graphviz.test import IMAGEDIR, read_data, data_graph
from prereq_flowchart.scrape.scrape import DATA_FOLDER

"""prereq-flowchart: create graphs representing the prerequisite hierarchy of a set of classes

instructions: don't die

"""

parser = argparse.ArgumentParser(
    description="Generates graphs based on the prerequisites of classes in a major."
)
parser.add_argument(
    "search",
    metavar="query",
    type=str,
    help="Search for classes that roughly match the query string",
)

args = vars(parser.parse_args())

if not exists(join(DATA_FOLDER, "lookup.json")):
    # the main reason why being able to grab exactly what is needed would be cool
    r = input("Gathering data; this will take a while...continue? [Y/n]")
    if r == "n":
        sys.exit(0)
    from prereq_flowchart import compose

    json = compose.make_json_data_for_majors()

query = args["search"]

from prereq_flowchart.search import search_major_names

results = search_major_names(query=query)
print("results:")
# are we programming enough to not index from 1
i = 1
for (r, h, _) in results:
    print(f"{i}.\t{r}")  # ({c})")
    i += 1
c = ""
# ask user to choose from list provided by search
while True:
    c = input("choose a listing (or q[uit] to exit): ")
    if c == "q" or c == "quit":
        sys.exit(0)
    try:
        c = int(c)
        break
    except TypeError:
        print("invalid integer format")
        continue
# get hash from list
(r, h, _) = results[c - 1]
data_graph(read_data(join(DATA_FOLDER, h))).render(join(IMAGEDIR, "Graph1"))
print("complete!")
