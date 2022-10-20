# import json
import re
from hashlib import md5
import requests
from typing import *
import bs4
from bs4 import BeautifulSoup

import os

cache = "data/cache"
MAJOR_LIST_LINK = "https://onestop2.umn.edu/pcas/viewCatalogSearchResults.do?campusId=UMNTC&userDefinedSearch=true&keywords=&careerId=UGRD&programType=BACC"

def get_web_data(link: str, fresh=False) -> str:
    """
    Retrieves data from the internet and stores it in the hashed file cache

    If the hash of a link already exists on disk, this will instead return
    whatever is stored on disk
    Arguments:
        link: link to website to be scraped
        fresh: force retrieve from website
    """
    if not os.path.exists(cache):
        os.makedirs(cache)
    print(link.encode())
    filename = md5(link.encode()).hexdigest()
    try:
        if fresh:
            raise FileNotFoundError()  # ehehe
        f = open(f"{cache}/{filename}.html", "r", encoding="utf-8")
        s = f.read()
        return s
    except FileNotFoundError:
        f = open(f"{cache}/{filename}.html", "w", encoding="utf-8")
        r = requests.get(link)
        s = r.text
        f.write(s)
        pass
    f.close()
    return s

def get_majors() -> List[str]:
    """
    Uses content at MAJOR_LIST_LINK to gather a list of links to all majors on campus
    """
    s = get_web_data(MAJOR_LIST_LINK)
    soup = BeautifulSoup(s)
    # code that is adapted to the site
    table = soup.find("table", attrs={"id":"appTable"})
    tbody = table.find("tbody")
    rows = tbody.find_all("td", attrs={"class": "bold100"})
    # maps table cell to link within the <a> tag
    return ["https://onestop2.umn.edu/pcas/"+x.find("a")["href"] for x in rows]


def get_major_data(link: str):
    """
    UNDER CONSTRUCTION
    Goes to the major at the link provided to gather every class
    associated with the major in any way

    this is done by:
        1. select for table cell representing main content
        2. find all <a> tags
        3. get containing text
        4. filter to match class code pattern
    Arguments:
        link: link to the major in question
    Returns:
        All classes associated with major
    """
    s = get_web_data(link)

    html = BeautifulSoup(s)

    # get every class listing (and some garbage) indiscriminately
    '''
    div = html.find("div", attrs={"style": "width: 808px;"})

    a = div.find_all("a")

    # split and rejoin with normal spaces (it was on stackoverflow it must be optimal)
    sections: List[str] = [' '.join(x.text.strip().split()) for x in a]

    for i in range(len(sections)):
        while i < len(sections):
            if re.match("[A-Z]+ \d{4}[VW]?", sections[i]):
                break
            else:
                sections.pop(i)
    '''

    # navigate to bold section titles and go up three levels to find
    # all classes in containing div (99% sure this is reliable)
    div = html.find("div", attrs={"style": "width: 808px;"})
    headers: List[bs4.element.Tag] = div.find_all("b")
    shits = []
    for header in headers:
        header_text = ' '.join(header.text.strip().split()).strip()
        if header_text == "Required Courses":
            body = header.parent.parent.parent
            shit = ' '.join(body.text.strip().split())
            shits.append(shit)


    return shits



majors = get_majors()
i = 0
for major in majors:
    data = get_major_data(major)
    for datum in data:
        print(datum)
    i += 1
    if i > 3:
        break
