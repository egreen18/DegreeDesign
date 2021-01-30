import requests
from bs4 import BeautifulSoup
from modelclass import (Class,Catalog)
import re
import json

#Creating RegEx patterns for processing of scraped data
code_find = re.compile(r"([A-Z]*).*(\d{3})")
credit_find = re.compile(r"Credits*:|CEUs*:\s(\d|Var\[.*\])")
course_find = re.compile(r"\(.*\)")
url_find = re.compile(r'href="(.*)"')

#Defining important URLs
urlCSU = 'https://catalog.colostate.edu'
urlBase = 'https://catalog.colostate.edu/general-catalog/courses-az/'
url = 'https://catalog.colostate.edu/general-catalog/courses-az/math/'

#Function which generates a catalog filled with class objects for a given course URL
def get_catalog(url,program):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    classes = soup.find_all('p',class_="courseblocktitle")
    catalog = Catalog()
    for i in classes:
        if not code_find.match(i.string):
            break
        code = code_find.split(i.string)[1]+code_find.split(i.string)[2]
        parent = i.parent.find_all('p',class_="courseblockdesc")[0].contents
        setattr(catalog,code,Class())
        setattr(getattr(catalog,code),'program',program)
        setattr(getattr(catalog,code),'credits',credit_find.split(i.string)[1])
        setattr(getattr(catalog,code),'description',parent[2].string)
        dex = 6
        while parent[dex].string:
            if code_find.match(parent[dex].string):
                match = code_find.match(parent[dex].string)
                getattr(getattr(catalog,code),'prereqs').append(match[1]+match[2])
            dex += 1
        termTrack = 0
        for j in parent:
            if termTrack:
                setattr(getattr(catalog,code),'terms',j.string)
                break
            if j.string:
                if re.match(r'Terms*\sOffered:\s',j.string):
                    termTrack = 1
    return catalog

#Grabbing all courses and initializing list storage
responseBase = requests.get(urlBase)
soupBase = BeautifulSoup(responseBase.text, "html.parser")
courses = soupBase.find_all('li')
Courses = []

#Running get_catalog on every course and saving in the list
for kdx,k in enumerate(courses):
    if k.string:
        if course_find.search(k.string):
            url = urlCSU+url_find.split(str(k))[1]
            print(url)
            catalog = get_catalog(url,course_find.split(courses[kdx].string)[0])
            Courses.append(catalog)
            
#Cleaning up empty courses
while [] in Courses:
    Courses.remove([])

#Translating objects into dictionaries for JSON conversion
dictCourses = Courses.copy()
for idx,i in enumerate(dictCourses):
    for j in list(i.__dict__.keys()):
        setattr(dictCourses[idx],j,getattr(dictCourses[idx],j).__dict__)
    dictCourses[idx] = dictCourses[idx].__dict__
 
#Dumping data as JSON for variable storage    
with open('courseData.json',"w") as outfile:
    def obj_dict(obj):
        return obj.__dict__
    json.dump(dictCourses,outfile)