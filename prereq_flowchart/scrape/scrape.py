import json
import os
from pprint import pprint
from classinfo import *  # CourseNumber, Course, get_all_classes_from_classinfo
from majorScrapper import Major, scrapeMajors
import majorScrapper
import pickle
from os.path import join, dirname, exists, abspath

# [project]/prereq_flowchart/scrape/../../data
DATA_FOLDER = join(dirname(abspath(__file__)), "../../data")
FORCE_RECHECK_CLASSINFO = False
FORCE_RECHECK_MAJORINFO = False


def scrape_classinfo() -> dict[CourseNumber, Course]:
    path = join(DATA_FOLDER, "out_classinfo.pickle")
    log_path = join(DATA_FOLDER, "out_classinfo.txt")

    if os.path.exists(path) and not FORCE_RECHECK_CLASSINFO:
        print("reading cached classinfo")
        with open(path, "rb") as f:
            p = pickle.load(f)
            return p

    print("getting classes from classinfo")
    out = get_all_classes_from_classinfo()
    with open(path, "wb") as f:
        pickle.dump(out, f)
    with open(log_path, "w") as f:
        pprint(out, f)
    print("scraping successful")

    return out


def scrape_majors() -> list[Major]:
    path = join(DATA_FOLDER, "majorCatalog.pickle")
    json_path = join(DATA_FOLDER, "majorCatalog.json")

    if os.path.exists(json_path):
        if os.path.exists(path) and not FORCE_RECHECK_MAJORINFO:
            print("reading cached classinfo")
            with open(path, "rb") as f:
                cache = pickle.load(f)
                return cache

    print("getting majors from university catalogs")
    m = scrapeMajors()
    with open(path, "wb") as f:
        pickle.dump(m, f)

    # this is still easier to look at for debugging purposes
    j = [major.getJSON() for major in m]
    with open(json_path, "w") as f:
        json.dump(j, f)

    return m


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

