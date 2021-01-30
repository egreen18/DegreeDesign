import requests
from bs4 import BeautifulSoup
from modelclass import Class
import re

code_find = re.compile(r"([A-Z]*).*(\d{3})")
credit_find = re.compile(r"Credits*:\s(\d|Var\[.*\])")

url = 'https://catalog.colostate.edu/general-catalog/courses-az/math/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
courses = soup.find_all('p',class_="courseblocktitle")
catalog = ['']*len(courses)
for idx,i in enumerate(courses):
    parent = i.parent.find_all('p',class_="courseblockdesc")[0].contents
    catalog[idx] = Class()
    catalog[idx].code = code_find.split(i.string)[1]+code_find.split(i.string)[2]
    catalog[idx].credits = credit_find.split(i.string)[1]
    catalog[idx].description = parent[2].string
    dex = 6
    while parent[dex].string:
        if code_find.match(parent[dex].string):
            match = code_find.match(parent[dex].string)
            catalog[idx].prereqs.append(match[1]+match[2])
        dex += 1
    termTrack = 0
    for j in parent:
        if termTrack:
            catalog[idx].terms = j.string
            break
        if j.string:
            if re.match(r'Terms*\sOffered:\s',j.string):
                termTrack = 1
    print(catalog[idx].terms)
    