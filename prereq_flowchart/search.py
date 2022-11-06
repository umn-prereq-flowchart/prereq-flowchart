"""search.py - find major to create a graph from

in the future, maybe can sort for department, class number, all sorts of filters

could potentially take on some of the tasks of compose.py
"""
from os import path
import json

from thefuzz import process

from prereq_flowchart.scrape.scrape import DATA_FOLDER

with open(path.join(DATA_FOLDER, "lookup.json"), "r") as f:
    major_table = json.load(f)
    major_names = major_table.keys()


def search_major_names(query: str):
    r = process.extract(query, major_names, limit=10)
    fns = [(name, major_table[name], c) for (name, c) in r]
    return fns

    # how do i make these selectable, where do i cache these results between calls
