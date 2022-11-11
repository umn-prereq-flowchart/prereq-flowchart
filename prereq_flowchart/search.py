"""search.py - find major to create a graph from

in the future, maybe can sort for department, class number, all sorts of filters

could potentially take on some of the tasks of compose.py
"""
from os import path
import json

from thefuzz import process

from prereq_flowchart.scrape.scrape import DATA_FOLDER
from prereq_flowchart import compose


lookup_file = path.join(DATA_FOLDER, "lookup.json")
if path.exists(lookup_file):
    with open(path.join(DATA_FOLDER, "lookup.json"), "r") as f:
        major_table = json.load(f)
else:
    major_table = compose.make_json_data_for_majors()
major_names = major_table.keys()


def search_major_names(query: str, num_results=10):
    r = process.extract(query, major_names, limit=num_results)
    fns = [(name, major_table[name], c) for (name, c) in r]
    return fns
