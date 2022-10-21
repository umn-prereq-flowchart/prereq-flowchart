from typing import Any
import pickle
import json
import sys
from prereq_flowchart.classinfo import Course, CourseNumber, Prerequisite


def make_json_node(course: Course) -> dict[str, Any]:
    return {
        "Classname": f"{course.catalog_number.department} {course.catalog_number.number}",
        "Pre-Reqs": [
            f"{prereq.catalog_number.department} {prereq.catalog_number.number}"
            for prereq in course.prerequisites
        ],
        "Reccomended": [],
    }


def main() -> None:
    with open(sys.argv[1], "rb") as f:
        courses: dict[CourseNumber, Course] = pickle.load(f)

    json_courses = [
        make_json_node(course)
        for coursenum, course in courses.items()
        if coursenum.department == "CSCI"
    ]

    with open(sys.argv[2], "w") as f:
        json.dump(json_courses, f, indent=4)


if __name__ == "__main__":
    main()
