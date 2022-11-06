from os.path import join
from hashlib import md5

from prereq_flowchart.scrape.classinfo import *
from prereq_flowchart.scrape import scrape

"""
recursively searches for prerequisites to a class, then flattens it into a list
of courses and their prerequisites.

this is the memoization test
"""
# def get_prerequisites():


def make_json_data_for_majors():
    c = scrape.scrape_classinfo()
    m = scrape.scrape_majors()
    # associate hashed file name with major title
    major_table = {}

    for major in m:
        print(f"generating: {major.name}")
        courses = {}
        for course in major.courses:
            num = course.catalogTitle

            # i don't know how to do this better, it's painfully slow
            # creating a CourseNumber and checking for equality does not work
            for c_number in c.keys():
                # duplicate paring (i think due to multiple semesters)
                c_num = c_number.department + " " + c_number.number
                if num == c_num:
                    courses[c_num] = c[c_number]
                    break
                    # courses.append(c[c_number])

        # discard string name (maybe don't do this?)
        courses = courses.values()
        graph_data = []
        # todo: recursively search for prerequisites to prerequisites
        for course in courses:
            number = (
                course.catalog_number.department + " " + course.catalog_number.number
            )
            prereqs = []
            for p in course.prerequisites:
                name = p.catalog_number.department + " " + p.catalog_number.number
                # this algorithm seems to create a lot of duplicate prerequisites
                # cleaner data would help but i think this is safe to apply either way
                if name not in prereqs:
                    prereqs.append(name)

            graph_data.append({"Classname": number, "Prereqs": prereqs})

        filename = md5(major.name.encode()).hexdigest() + ".json"
        major_table[major.name] = filename
        print(f"stored at: {filename}")
        with open(join(scrape.DATA_FOLDER, filename), "w") as f:
            json.dump(graph_data, f)

    with open(join(scrape.DATA_FOLDER, "lookup.json"), "w") as f:
        json.dump(major_table, f)


if __name__ == "__main__":
    make_json_data_for_majors()
