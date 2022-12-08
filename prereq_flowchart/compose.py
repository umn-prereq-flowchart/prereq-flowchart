from os.path import join
from hashlib import md5

from prereq_flowchart.scrape.classinfo import *
from prereq_flowchart.scrape import scrape

c = scrape.scrape_classinfo()
non_existent = []
buf = []


def get_courses(course: CourseNumber, n=0) -> [CourseNumber]:
    """
    returns a list of classes (not a hierarchy!) that are a prerequisite to the course provided.
    Args:
        course: 
        n: 

    Returns:

    """
    # print(course)
    global buf
    if n > 5:
        # print(f"bottomed out: {course}")
        return []

    if course not in c:
        return []
    # this is an issue
    # if course == CourseNumber("CHEM", "1061"):
    #     print(f'chem prereqs: {c[course].prerequisites}')
    prereqs = []
    for prereq in c[course].prerequisites:
        if prereq in buf:
            continue
        if prereq.catalog_number in c:
            prereqs.append(prereq.catalog_number)
            prereqs.extend(get_courses(course=prereq.catalog_number, n=n+1))
        else:
            if prereq.catalog_number not in non_existent:
                print(f"warning: prereq does not exist: {prereq.catalog_number}")
                non_existent.append(prereq.catalog_number)

    for prereq in prereqs:
        if prereq not in buf:
            buf.append(prereq)
    if n == 0:
        # print(len(buf))
        buf = []
    return prereqs


def make_json_data_for_majors():
    c = scrape.scrape_classinfo()
    m = scrape.scrape_majors()
    # associate hashed file name with major title
    major_table = {}

    for major in m:
        # print(major.name)
        courses = []
        warnings = ""
        for course in major.courses:
            # print(course.catalogTitle)
            num = course.catalogTitle.split(" ")
            if len(num) != 2:
                warnings += f"\tinvalid course: {course.catalogTitle}\n"
                continue
            num = CourseNumber(num[0], num[1])
            if num not in c:
                warnings += f"\tcourse not found: {course.catalogTitle}\n"
                continue
            if c[num] not in courses:
                courses.append(c[num])
                for pr in get_courses(num):
                    if c[pr] not in courses:
                        courses.append(c[pr])
            # courses.extend(get_courses(c[num]))
        if warnings != "":
            print(f"{major.name}\n", warnings, end="")

        # i = 0
        # while i in range(0, len(courses)):
        #     if "H" in courses[i].catalog_number.number:
        #         courses.pop(i)
        #     else:
        #         i += 1

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
