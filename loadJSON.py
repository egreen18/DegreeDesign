#Function to load Courses from JSON to object list. Returns list
def loadCourses():
    #Importing dependencies
    from modelclass import (Class, Catalog, College)
    import json
    
    #Loading JSON file to dictionary
    with open('courseData.json') as f:
        courseData = json.load(f)
    
    #Transforming dictionary into object list using Class.load method
    # Courses = []
    CSU = College()
    for idx,i in enumerate(courseData):
        catalog = Catalog()
        setattr(CSU,i,catalog)
        for j in courseData[i]:
            classTemp = Class()
            classTemp.load(courseData[i][j])
            setattr(catalog,j,classTemp)
    return CSU
