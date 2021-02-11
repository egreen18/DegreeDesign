import requests
from bs4 import BeautifulSoup
from modelclass import (Class,Catalog,College)
from unicodedata import normalize
import re
import json

#Creating RegEx patterns for processing of scraped data
# code_find = re.compile(r"([A-Z]*).*(\d{3})"
credit_find = re.compile(r"(?:Credits*:|CEUs*:)\s(\d|Var\[.*\])")
code_match = re.compile(r"\D{1,5}.\d{1,5}")
code_find = re.compile(r"\xa0")
course_find = re.compile(r"\(.*\)")
url_find = re.compile(r'href="(.*)"')
letter_find = re.compile(r"(\D*)")

#Defining important URLs
urlCSU = 'https://catalog.colostate.edu'
urlBase = 'https://catalog.colostate.edu/general-catalog/courses-az/'

#Function which generates a catalog filled with class objects for a given course URL
def get_catalog(url,program):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    classes = soup.find_all('p',class_="courseblocktitle")
    catalog = Catalog()
    for i in classes:
        code = code_find.split(i.string)[0]+code_find.split(i.string)[1]
        parent = i.parent.find_all('p',class_="courseblockdesc")[0].contents
        setattr(catalog,code,Class())
        setattr(getattr(catalog,code),'program',program)
        setattr(getattr(catalog,code),'title',code_find.split(i.string)[3])
        setattr(getattr(catalog,code),'credits',credit_find.split(i.string)[1])
        setattr(getattr(catalog,code),'description',parent[2].string)
        for j in parent:
            if not j.string:
                pass
            elif code_match.match(j.string):
                getattr(getattr(catalog,code),'prereqs').append(
                    normalize('NFKD',j.string).replace(' ',''))
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
CSU  = College()

#Running get_catalog on every course and saving in the list
for kdx,k in enumerate(courses):
    if k.string:
        if course_find.search(k.string):
            url = urlCSU+url_find.split(str(k))[1]
            print(url)
            catalog = get_catalog(url,course_find.split(courses[kdx].string)[0])
            if catalog.names():
                setattr(CSU,letter_find.split(catalog.names()[0])[1],catalog)
            

# Translating objects into dictionaries for JSON conversion
dictCSU = CSU.__dict__
for i in dictCSU.keys():
    dictCSU[i] = dictCSU[i].__dict__
    for j in dictCSU[i].keys():
        dictCSU[i][j] = dictCSU[i][j].__dict__
 
#Dumping data as JSON for variable storage    
with open('courseData.json',"w") as outfile:
    def obj_dict(obj):
        return obj.__dict__
    json.dump(dictCSU,outfile)