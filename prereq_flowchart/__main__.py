import argparse
import sys

from os.path import exists, join

from prereq_flowchart.graph.graph import IMAGEDIR, read_data, data_graph
from prereq_flowchart.scrape.scrape import DATA_FOLDER

"""prereq-flowchart: create graphs representing the prerequisite hierarchy of a set of classes

Instructions: Use the script or directly run the module with -h to see help
"""

parser = argparse.ArgumentParser(
    description="Generates graphs based on the prerequisites of classes in a major."
)
parser.add_argument(
    "search",
    metavar="query",
    type=str,
    nargs="+",
    help="Search for classes that roughly match the query string",
)
parser.add_argument(
    "--force-recheck-classinfo",
    dest="recheck_classinfo",
    action="store_const",
    const=True,
    default=False,
    help="Forces a recheck of the ClassInfo website for fresh data",
)
parser.add_argument(
    "--force-recheck-majorinfo",
    dest="recheck_majorinfo",
    action="store_const",
    const=True,
    default=False,
    help="Forces a recheck of the University Catalogs website for fresh data",
)
parser.add_argument(
    "--rebuild-major-json",
    dest="rebuild_major_json",
    action="store_const",
    const=True,
    default=False,
    help="Rebuilds major JSON files from scraped data",
)
parser.add_argument(
    "-n",
    dest="num_results",
    type=int,
    default=10,
    # nargs='+',
    help="Number of search results to return",
)

args = vars(parser.parse_args())

if not exists(DATA_FOLDER):
    r = input("Gathering data; this will take a while...continue? [Y/n]: ")
    if r == "n":
        sys.exit(0)
    from prereq_flowchart.scrape.scrape import scrape_classinfo, scrape_majors

    # side-effect-oriented programming
    scrape_classinfo()
    scrape_majors()
else:
    if args["recheck_classinfo"]:
        r = input("Are you sure you would like to recheck ClassInfo? [Y/n]: ")
        from prereq_flowchart.scrape.scrape import scrape_classinfo

        scrape_classinfo()
    if args["recheck_majorinfo"]:
        r = input("Are you sure you would like to recheck University Catalogs? [Y/n]: ")
        from prereq_flowchart.scrape.scrape import scrape_majors

        scrape_majors()

rebuild_json = (
    args["rebuild_major_json"] or args["recheck_classinfo"] or args["recheck_majorinfo"]
)
if not exists(join(DATA_FOLDER, "lookup.json")) or rebuild_json:
    from prereq_flowchart import compose

    json = compose.make_json_data_for_majors()

query = " ".join(args["search"])
from prereq_flowchart.search import search_major_names

results = search_major_names(query=query, num_results=args["num_results"])
print("results:")
# are we programming enough to not index from 1
for i, (r, h, _) in enumerate(results, start=1):
    print(f"{i}.\t{r}")  # ({c})")
c = ""
# ask user to choose from list provided by search
while True:
    c = input("choose a listing (or q[uit] to exit): ")
    if c == "q" or c == "quit":
        sys.exit(0)
    try:
        c = int(c)
        if c > len(results):
            print("Not a valid index")
        else:
            break
    except ValueError:
        print("Invalid integer format")
        continue
# get hash from list
(r, h, _) = results[c - 1]
data_graph(read_data(join(DATA_FOLDER, h))).render(join(IMAGEDIR, "Graph1"))
print("Complete!")
