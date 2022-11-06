import os
from os import path
import json
from pprint import pprint
import pickle

from prereq_flowchart.scrape import classinfo
from prereq_flowchart.scrape import majorScrapper

"""
functions for collecting information from the web

todo: select for specific info instead of gathering everything and then sorting 
through it

ultimately it would be nice to be able to request data for specific classes and 
construct graphs with minimum viable data, which is why i extracted this logic
out (in order to create an adapted interface to the websites with built-in 
caching)
"""

# prereq_flowchart/prereq_flowchart/scrape/../../data
DATA_FOLDER = path.join(path.dirname(path.abspath(__file__)), "../../data")
if not path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
FORCE_RECHECK_CLASSINFO = False
FORCE_RECHECK_MAJORINFO = False


def scrape_classinfo() -> dict[classinfo.CourseNumber, classinfo.Course]:
    pickle_path = path.join(DATA_FOLDER, "out_classinfo.pickle")
    log_path = path.join(DATA_FOLDER, "out_classinfo.txt")

    if path.exists(pickle_path) and not FORCE_RECHECK_CLASSINFO:
        print("reading cached classinfo")
        with open(pickle_path, "rb") as f:
            p = pickle.load(f)
            return p

    print("getting classes from classinfo")
    out = classinfo.get_all_classes_from_classinfo()
    with open(pickle_path, "wb") as f:
        pickle.dump(out, f)
    with open(log_path, "w") as f:
        pprint(out, f)
    print("scraping successful")

    return out


def scrape_majors() -> list[majorScrapper.Major]:
    pickle_path = path.join(DATA_FOLDER, "majorCatalog.pickle")
    json_path = path.join(DATA_FOLDER, "majorCatalog.json")

    if path.exists(json_path):
        if path.exists(pickle_path) and not FORCE_RECHECK_MAJORINFO:
            print("reading cached major catalogs")
            with open(pickle_path, "rb") as f:
                cache = pickle.load(f)
                return cache

    print("getting majors from university catalogs")
    m = majorScrapper.scrapeMajors()
    with open(pickle_path, "wb") as f:
        pickle.dump(m, f)

    # this is still easier to look at for debugging purposes
    j = [major.getJSON() for major in m]
    with open(json_path, "w") as f:
        json.dump(j, f)

    return m


# note: even though this will read/write cache files in the data folder, they
# will not be valid in usage outside of this package because the location of
# python files has changed, meaning pickle will not be able to deserialize
# the objects.
if __name__ == "__main__":
    # convert cached json back into objects (maybe pickling is a good idea)
    # json_path = join(DATA_FOLDER, "majorCatalog.json")
    # with open(json_path, "r") as f:
    #     major_data = json.load(f)
    #
    # majors = []
    # for major in major_data:
    #     courses = [majorScrapper.Course(credits=course["credits"],
    #                                     title=course["title"],
    #                                     catalogTitle=course["catalogTitle"],
    #                                     description=course["description"],
    #                                     inOr=course["inOr"],
    #                                     required=course["required"])
    #                for course in major["courses"]]
    #     m = Major(courses=courses, minCredits=major["minCredits"], name=major["name"])
    #     majors.append(m)
    #
    # path = join(DATA_FOLDER, "majorCatalog.pickle")
    # print(majors[0].name)
    # with open(path, "wb") as f:
    #     pickle.dump(majors, f)

    print("testing getting everything")

    courses = scrape_classinfo()
    majors = scrape_majors()

    print("retrieval complete")
