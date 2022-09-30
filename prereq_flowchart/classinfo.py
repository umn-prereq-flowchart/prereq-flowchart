import requests
from dataclasses import dataclass
from typing import Any, TypeAlias, Tuple
import re
from enum import IntEnum

CLASSINFO_URL: str = "http://classinfo.umn.edu/?subject={department}&json=1"


class Semester(IntEnum):
    SPRING = 0
    SUMMER = 1
    FALL = 2


@dataclass(order=True)
class Term:
    year: int
    semester: Semester

    @classmethod
    def from_str(cls, str_repr: str) -> "Term":
        term_str, year_str = str_repr.split(" ")
        year = int(year_str)

        match term_str:
            case "Spring":
                term = Semester.SPRING
            case "Summer":
                term = Semester.SUMMER
            case "Fall":
                term = Semester.FALL
            case _:
                raise ValueError(f"Unknown term: {term!r}")

        return cls(year=year, semester=term)


@dataclass(frozen=True)
class CourseNumber:
    # e.g the CSCI, EE, CEGE part of a course number
    department: str
    # the 1001, 1301W, 1402H part of a course number
    number: str


@dataclass
class Prerequisite:
    catalog_number: CourseNumber
    concurrent_allowed: bool = False


Credits: TypeAlias = (
    None
    | float
    | Tuple[
        float, float
    ]
)


@dataclass
class Course:
    catalog_number: CourseNumber
    course_title: str
    # the number of credits that this class is worth
    credits: Credits
    # other courses that you have to take before you can take this course
    prerequisites: list[Prerequisite]
    is_elective: bool = False


def deduplicate_class_listings(
    class_listings: dict[str, dict[Any, Any]]
) -> list[dict[Any, Any]]:
    course_number_entry_keys: dict[CourseNumber, str] = {}
    last_seen_course_term: dict[CourseNumber, Term] = {}
    for key, course in class_listings.items():
        course_num = CourseNumber(
            department=course["Subject"], number=course["Catalog Number"]
        )
        course_term = Term.from_str(course["Term"])

        if (
            course_num not in last_seen_course_term
            or last_seen_course_term[course_num] < course_term
        ):
            last_seen_course_term[course_num] = course_term
            course_number_entry_keys[course_num] = key

    return [
        class_listings[entry_key] for entry_key in course_number_entry_keys.values()
    ]


def get_prerequisites_string(class_json: dict[Any, Any]) -> str:
    def find_rough_string(class_json: dict[Any, Any]) -> str:
        if "Prerequisites" in class_json:
            return str(class_json["Prerequisites"])
        elif "Course Catalog Description" in class_json:
            desc_str = class_json["Course Catalog Description"]
            matches = re.match(r"^.+[pP]rereq(?:(?:uisites)|(?:s))?:?(.+)$", desc_str)
            if matches is not None:
                return matches.group(1)

        # There is no prerequisites section and we couldn't find it in the catalog description
        try:
            course_desc = class_json["Course Description"]
            matches = re.match(
                r"^.+[pP]rereq(?:(?:uisites)|(?:s))?:?(.+)$", course_desc
            )
            if matches is not None:
                return matches.group(1)
        except (IndexError, KeyError):
            pass
        return ""

    def expand_prereq_string_abbreviations(prereq_string: str) -> str:
        prereq_string = prereq_string.lower()

        prereq_string = prereq_string.replace("dept", "department")
        prereq_string = prereq_string.replace("instr", "instructor")

        # its meaningless that you can get perms from special ppl
        prereq_string = prereq_string.replace("instructor consent", "")
        prereq_string = prereq_string.replace("department consent", "")

        prereq_string = prereq_string.replace(" or ", " | ")
        prereq_string = prereq_string.replace(
            "concurrent registration is required (or allowed) in", "<=>"
        )
        prereq_string = prereq_string.replace(" and ", " , ")

        return prereq_string

    return expand_prereq_string_abbreviations(find_rough_string(class_json))


# Need a mechanism to parse a classinfo listing to find its prerequisites


def extract_prereqs(prereq_string: str, default_subject: str) -> list[Prerequisite]:
    course_number_prereqs = re.findall(
        "(?:\w{1,4} )?\d\d\d\d(?:[HWVhwv]?)", prereq_string
    )
    ret = []

    match: str
    for match in course_number_prereqs:
        if re.fullmatch("\d{4,4}(?:[whv]?)", match):
            subject = default_subject
            number = match.upper()
        else:
            try:
                subject, number = match.upper().strip().split(" ")
            except ValueError:
                print(match)
                raise

        ret.append(
            Prerequisite(
                catalog_number=CourseNumber(department=subject, number=number),
                concurrent_allowed=False,  # TODO
            )
        )

    return ret


def class_json_value_to_course(class_json: dict[Any, Any]) -> Course:
    credits_str = class_json.get("Credits")
    if credits_str is not None:
        re_output = re.match(r"(\d+(?:\.\d+)?(?:-\d+)?) Credits?", credits_str)
        if re_output is None:
            print(credits_str)
            raise TypeError("could not find credits in credits str?? bizarre")

        match = re_output[1]
        if "-" in match:
            lower_bound, upper_bound = match.split("-")
            credits: Credits = (float(lower_bound), float(upper_bound))
        else:
            credits = float(match)
    else:
        credits = None

    prereq_str = get_prerequisites_string(class_json)
    return Course(
        catalog_number=CourseNumber(
            department=class_json["Subject"],
            number=class_json["Catalog Number"],
        ),
        course_title=class_json["Class Title"],
        credits=credits,
        prerequisites=extract_prereqs(
            prereq_str, default_subject=class_json["Subject"]
        ),
    )


def search_dept_on_classinfo(department: str) -> dict[CourseNumber, Course]:
    def get_single_department(department: str) -> dict[CourseNumber, Course]:
        print(f"Fetching the {department} courses")
        response = requests.get(
            f"http://classinfo.umn.edu/?subject={department}&json=1"
        ).json()

        deduped_classes = deduplicate_class_listings(response)
        courses = [class_json_value_to_course(course) for course in deduped_classes]
        return {course.catalog_number: course for course in courses}

    def get_missing_departments(courses: dict[CourseNumber, Course]) -> set[str]:
        fetched_depts = set()
        for course_num in courses:
            fetched_depts.add(course_num.department)

        ret = set()
        for course in courses.values():
            for prereq in course.prerequisites:
                if prereq.catalog_number.department not in fetched_depts:
                    ret.add(prereq.catalog_number.department)
        return ret

    ret = get_single_department(department)
    # while len(missing_depts := get_missing_departments(ret)) > 0:
    #     for dept in missing_depts:
    #         ret |= get_single_department(dept)

    return ret


# Need a mechanism to extract requirements from university catalogs page
