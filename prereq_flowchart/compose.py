from os.path import join
import pprint
from hashlib import md5
import scrape.scrape

from scrape.classinfo import *
from scrape.scrape import scrape_classinfo, scrape_majors

'''
recursively searches for prerequisites to a class, then flattens it into a list
of courses and their prerequisites.

this is the memoization test
'''
# def get_prerequisites():


def make_json_data_for_majors():
    c = scrape_classinfo()
    c_names = [course.department+" "+course.number for course in c.keys()]
    m = scrape_majors()
    # print(c.keys())
    for major in m:
        print(f"generating: {major.name}")
        courses = {}
        for course in major.courses:
            num = course.catalogTitle

            # i don't know how to do this better, it's painfully slow
            # creating a CourseNumber and checking for equality does not work
            for c_number in c.keys():
                # duplicate paring (i think due to multiple semesters)
                c_num = c_number.department+" "+c_number.number
                if num == c_num:
                    courses[c_num] = c[c_number]
                    break
                    # courses.append(c[c_number])

        # discard string name (maybe don't do this?)
        courses = courses.values()
        graph_data = []
        # todo: recursively search for prerequisites to prerequisites
        for course in courses:
            number = course.catalog_number.department+" "+course.catalog_number.number
            prereqs = []
            for p in course.prerequisites:
                name = p.catalog_number.department+" "+p.catalog_number.number
                # this algorithm seems to create a lot of duplicate prerequisites
                # cleaner data would help but i think this is safe to apply either way
                if name not in prereqs:
                    prereqs.append(name)

            graph_data.append({
                "Classname": number,
                "Prereqs": prereqs
            })

        # pprint.pprint(graph_data)
        filename = md5(major.name.encode()).hexdigest()+".json"
        print(f"stored at: {filename}")
        with open(join(scrape.scrape.DATA_FOLDER, filename), "w") as f:
            json.dump(graph_data, f)


if __name__ == "__main__":
    make_json_data_for_majors()
