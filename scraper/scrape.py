import requests
from bs4 import BeautifulSoup

YEARS = [str(i) for i in range(2000, 2021)]
QUARTER_ABREVS = ["WIN", "SPR", "SUM", "AUT"]

TIME_SCH_BASE_URL = "https://www.washington.edu/students/timeschd/"






def parse_link_string(link):
    """
    returns tuple of:
     - the "title" prefix of the course, ex: B CMU (with the space)
     - the "readable name" of the prefix
     For example, given: Health Economic Outcomes Research (HEOR)
     returns: ("HEOR", "Health Economic Outcomes Research")
    """
    # next, get the text, and parse it into the other 2 pieces
    to_split_index = link.rfind("(")
    if to_split_index == -1 or to_split_index == (len(link)-1):
        return (None, None)

    usable_name = link[:to_split_index]
    prefix = link[to_split_index+1:-1].replace("\xa0", " ")

    return (prefix,usable_name)

def get_dept_names(html):
    dept_triples = []
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a")
    for link in links:
        possible_dept_link = str(link.get("href"))
        if "html" in possible_dept_link \
            and len(possible_dept_link) < 15 \
            and link.string is not None:
            
            dept_prefix, dept_readable_name = parse_link_string(link.string)
            
            # couldn't find prefix
            if dept_prefix is None:
                continue

            # otherwise, we're good
            dept_triples.append(
                (dept_prefix, dept_readable_name, possible_dept_link)
            )
    return dept_triples

for year in YEARS:
    for quarter in QUARTER_ABREVS:
        # find all <li> elements that have an <a> in them
        main_page = requests.get(TIME_SCH_BASE_URL + "/" + quarter + year)
        dept_triples = get_dept_names(main_page.content)
        print(quarter + year + ": " + str(len(dept_triples)))




# start with the base URL 
# download the base, parse it into the department names