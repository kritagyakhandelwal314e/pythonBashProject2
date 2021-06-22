from pprint import pprint
from os import path
from sys import argv
import subprocess
from tabulate import tabulate
from exceptions import CourseDoesntExist, BashCommandExecutionError

BASE_DIR = "/data/courses"
MOUNT_BASE_DIR = "/home/trainee/courses"
COURSES_FILE = "courses.list"

def usage(exit_code=0):
  subprocess.run(["cat", "usage"])
  exit(exit_code)

def load_courses(file_name):
  courses_loaded = 0
  courses_not_loaded = 0
  COURSES = []
  try:
    with open(file_name, 'r') as courseList:
      while course := courseList.readline():
        try:
          if not course[:-1]:
            continue
          COURSES.append({
            'path': '/' + course[:-1],
            'name': course[:-1].split('/')[-1]
          })
          courses_loaded += 1
        except:
          print(f"can't process/load the course {course}")
          courses_not_loaded += 1
  except:
    print("can't open file!")
  # finally:
  #   print(f"loaded: {courses_loaded} courses\ncouldn't load: {courses_not_loaded} courses")
  return COURSES

COURSES = load_courses(file_name=COURSES_FILE)

def is_course(course_name):
  for course in COURSES:
    if course["name"] == course_name:
      return True
  return False

def get_course_path(course_name):
  for course in COURSES:
    if course["name"] == course_name:
      return course["path"]
  raise CourseDoesntExist

def is_mounted(course_name):
  source_path = BASE_DIR +  get_course_path(course_name)
  destination_path = MOUNT_BASE_DIR  + get_course_path(course_name)
  mount_string = source_path + ' on ' + destination_path + ' '
  return_values = subprocess.run(["mount"], capture_output=True)
  if return_values.returncode != 0:
    raise BashCommandExecutionError
  mnt_pts = str(return_values.stdout).split('\\n')
  for mnt_pt in mnt_pts:
    # print(mnt_pt, mount_string)
    if mount_string in mnt_pt:
      return True
  return False


def list_courses():
  table_rows = []
  table_header = ['SNo.', 'Course', 'Mount']
  for i, course  in enumerate(COURSES):
    table_rows.append([i+1, course['name'], is_mounted(course['name'])])
  print(tabulate(tabular_data=table_rows, headers=table_header, tablefmt='orgtbl'))
  # pprint(table_rows)

def mount_all():
  for course in COURSES:
    if not is_mounted(course['name']):
      mount(course['name'])

def unmount_all():
  for course in COURSES:
    if is_mounted(course['name']):
      unmount(course['name'])

def mount(course_name):
  # bindfs -p a-w -u trainee -g ftpaccess ${COURSE_PATH} ${TARGET_PATH}
  source_path = BASE_DIR + get_course_path(course_name)
  destination_path = MOUNT_BASE_DIR + get_course_path(course_name)
  return_values = subprocess.run(['bindfs', '-p', '550', '-u', 'trainee', '-g', 'ftpaccess', source_path, destination_path])
  if return_values.returncode != 0:
    raise BashCommandExecutionError
  print(f"successfully mounted {course_name}")

def unmount(course_name):
  destination_path = MOUNT_BASE_DIR + get_course_path(course_name)
  return_values = subprocess.run(['umount', destination_path])
  if return_values.returncode != 0:
    raise BashCommandExecutionError
  print(f"successfully unmounted {course_name}")

args = argv[1:]
if len(args) == 1:
  if args[0] == "-h":
    usage()
  elif args[0] == "-l":
    list_courses()
  elif args[0] == "-m":
    mount_all()
  elif args[0] == "-u":
    unmount_all()
  else:
    usage(1)
elif len(args) == 3:
  course = args[2]
  if not is_course(course):
    print("Invalid course name\nplease see the list of courses:")
    list_courses()
    exit(1)
  if args[1] == '-c':
    if args[0] == '-m':
      if is_mounted(course):
        print(f"Course: {course} is already mounted!")
      else:
        mount(course)
    elif args[0] == '-u':
      if is_mounted(course):
        unmount(course)
      else:
        print(f"Course: {course} is not mounted!")
    else:
      usage(1)
  else:
    usage(1)
else:
  usage(1)


