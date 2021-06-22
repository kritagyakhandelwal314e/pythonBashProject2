from pprint import pprint
from os import path
from sys import argv

BASE_DIR = "/data/courses"
MOUNT_BASE_DIR = "/home/trainee/courses"
COURSES_FILE = 'courses.list'
def load_courses(file_name):
  courses_loaded = 0
  courses_not_loaded = 0
  COURSES = []
  try:
    with open(file_name, 'r') as courseList:
      while course := courseList.readline():
        try:
          COURSES.append({
            'path': path.join(BASE_DIR, course[:-1]),
            'name': course[:-1].split('/')[-1]
          })
          courses_loaded += 1
        except:
          print(f"can't process/load the course {course}")
          courses_not_loaded += 1
  except:
    print("can't open file!")
  finally:
    print(f"loaded: {courses_loaded} courses\ncouldn't load: {courses_not_loaded} courses")
  return COURSES

COURSES = load_courses(COURSES_FILE)

pprint(COURSES)



