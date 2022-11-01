from selenium import webdriver
from dataclasses import dataclass
from selenium.webdriver.common.by import By
import re


@dataclass
class Course:
    credits: int
    title: str
    catalogTitle: str
    description: str
    inOr: bool  # This is to indicate that the course has options
    required: bool

    def getJSON(self):
        return {
            "credits": self.credits,
            "title": self.title,
            "catalogTitle": self.catalogTitle,
            "description": self.description,
            "inOr": self.inOr,
            "required": self.required,
        }


@dataclass
class Major:
    courses: []
    minCredits: int
    name: str

    def getJSON(self):
        mappedCourses = [c.getJSON() for c in self.courses]
        return {
            "courses": mappedCourses,
            "minCredits": self.minCredits,
            "name": self.name,
        }


def getMajorLinks():
    MAJOR_URL = "https://onestop2.umn.edu/pcas/viewCatalogSearchResults.do?campusId=UMNTC&userDefinedSearch=true&keyworjds=&careerId=UGRD&programType=BACC"

    browser = webdriver.Firefox()
    browser.get(MAJOR_URL)
    browser.maximize_window()

    numberOfMajors = re.match(
        "[0-9]*",
        browser.find_element(By.CLASS_NAME, "requirementshead").get_attribute(
            "textContent"
        ),
    ).group(0)
    majorLinks = (
        browser.find_element(By.ID, "appTable")
        .find_element(By.TAG_NAME, "tbody")
        .find_elements(By.CLASS_NAME, "bold100")
    )
    # Links to different majors

    retLinks = []
    for i in range(int(numberOfMajors)):
        curMajor = majorLinks[i].find_element(By.TAG_NAME, "a").get_attribute("href")
        retLinks.append(curMajor)

    browser.close()
    return retLinks


def scrapeMajors() -> list[Major]:
    browser = webdriver.Firefox()
    browser.maximize_window()
    majorLinks = getMajorLinks()
    majorCatalog = []

    for majorLink in majorLinks:
        browser.get(majorLink)
        majorName = browser.find_elements(By.CLASS_NAME, "programtitle")
        # The above line asks for all class names so we can skip old programs
        if len(majorName) > 1:
            continue  # This is an old program and it's layout is not the same, so we're skipping it
        minCredText = (
            browser.find_element(By.CLASS_NAME, "catalogList").find_elements(
                By.TAG_NAME, "li"
            )
        )[2].get_attribute("textContent")
        minCred = re.search("\d+", minCredText).group(0)

        classes = browser.find_elements(By.XPATH, "//a[@onclick]/..")
        courses = []
        for class_ in classes:
            attr = str(class_.find_element(By.TAG_NAME, "a").get_attribute("onclick"))
            classID = re.search("courseInfo_[0-9]*", attr)[0]
            courseInfo = " ".join(class_.get_attribute("textContent").split())

            courseDesc = (
                browser.find_element(By.ID, classID)
                .find_element(By.CLASS_NAME, "textField")
                .get_attribute("textContent")
            )
            credits = re.search("\d+\.\d+-*\d*\.*\d*", courseInfo).group(0)
            catalogTitle = re.search("\w+ \d+W*H*V*", courseInfo).group(0)
            # Small form catalog name - EE 2301. Sometimes has W, H, or V at end.
            title = re.findall("\w+ \d+W*H*V* - (.*) \(.*", courseInfo)
            # Full descriptive title - Introduction to Microcontrollers
            if title == None or title == []:
                print(catalogTitle)
                raise TypeError("Couldn't find title in regex")
            inOr = re.search("or ", courseInfo) == None
            # Has or at the start - can this class replace another
            required = re.search("· ", courseInfo) == None
            # The bullet point represents electives. If regex finds none, it is required.

            courses.append(  # i think this is what was meant to happen
                Course(credits, title[0], catalogTitle, courseDesc, inOr, required)
            )
        majorCatalog.append(
            Major(courses, minCred, majorName[0].get_attribute("textContent"))
        )

    # mappedCatalog = [m.getJSON() for m in majorCatalog]
    #
    # with open("majorCatalog.json", "w") as majorCatalogFile:
    #     json.dump(mappedCatalog, majorCatalogFile, indent=2)
    # browser.close()

    return majorCatalog
