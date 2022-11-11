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
        courses = []
        format_warnings = ""
        not_found_warnings = ""
        for course in major.courses:
            num = course.catalogTitle.split(" ")
            if len(num) != 2:
                not_found_warnings += f"\tinvalid course: {course.catalogTitle}\n"
                continue
            num = CourseNumber(num[0], num[1])
            if num not in c:
                not_found_warnings += f"\tcourse not found: {course.catalogTitle}\n"
                continue
            if c[num] not in courses:
                courses.append(c[num])
        if format_warnings != "" or not_found_warnings != "":
            print(f"{major.name}\n", format_warnings, not_found_warnings, end="")

        graph_data = []
        # todo: recursively search for prerequisites to prerequisites
        for course in courses:
            # number = (
            #     course.catalog_number.department + " " + course.catalog_number.number
            # )
            number = course.catalog_number.to_str()
            prereqs = []
            for p in course.prerequisites:
                # name = p.catalog_number.department + " " + p.catalog_number.number
                name = p.catalog_number.to_str()
                if name not in prereqs:
                    prereqs.append(name)
            graph_data.append({"Classname": number, "Prereqs": prereqs})

        filename = md5(major.name.encode()).hexdigest() + ".json"
        major_table[major.name] = filename
        with open(join(scrape.DATA_FOLDER, filename), "w") as f:
            json.dump(graph_data, f)

    with open(join(scrape.DATA_FOLDER, "lookup.json"), "w") as f:
        json.dump(major_table, f)


if __name__ == "__main__":
    make_json_data_for_majors()
