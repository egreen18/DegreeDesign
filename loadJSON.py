#Function to load Courses from JSON to object list. Returns list
def loadCourses():
    #Importing dependencies
    from modelclass import (Class, Catalog)
    import json
    
    #Loading JSON file to dictionary
    with open('courseData.json') as f:
        courseData = json.load(f)
    
    #Transforming dictionary into object list using Class.load method
    Courses = []
    for idx,i in enumerate(courseData):
        catalog = Catalog()
        for j in list(i.keys()):
            setattr(catalog,j,Class().load(i[j]))
        Courses.append(catalog)
    return Courses