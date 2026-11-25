import re
import ast

CLASSES_RE = re.compile(r"^\s*(?P<name>\S+)\s*\[(?P<nums>[^\]]*)\]\s*$")
CLASSROOMS_RE = re.compile(r"^\s*(?P<name>\S+)\s*\[(?P<nums>[^\]]*)\]\s*$")
TEACHERS_RE = re.compile(r"^\s*(?P<name>\S+)\s*\[(?P<classes>[^\]]*)\]\s*$")
PREFERENCES_RE = re.compile(r"^\s*(?P<name>\S+)\s+(?P<prefs>\{.*\})\s*$")

def load_classes(path):
    classes = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            m = CLASSES_RE.match(line)
            nums_str = m.group("nums").strip()
            name = m.group("name").strip()
            durations = [int(x) for x in nums_str.split(",")]
            for d in durations:
                classes.append((name, d))
    return classes

def load_classrooms(path):
    classrooms = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            m = CLASSES_RE.match(line)
            nums_str = m.group("nums").strip()
            name = m.group("name").strip()
            startend = [int(x) for x in nums_str.split(",")]
            classrooms.append((name, startend[0], startend[1]))
    return classrooms

def load_teachers(path):
    teachers = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            m = TEACHERS_RE.match(line)
            classes_str = m.group("classes").strip()
            name = m.group("name").strip()
            classes = classes_str.split(",")
            classes = [c.strip() for c in classes]
            teachers.append((name, classes))
    return teachers

def load_preferences(path):
    likes, dislikes = [], []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            m = PREFERENCES_RE.match(line)
            name = m.group("name").strip()
            prefs = ast.literal_eval(m.group("prefs"))
            likes.append((name, prefs['likes']))
            dislikes.append((name, prefs['dislikes']))
    return likes, dislikes

def load(dir="."):
    classes_path = dir + "/Classes.txt"
    classrooms_path = dir + "/Classrooms.txt"
    teachers_path = dir + "/Teachers.txt"
    preferences_path = dir + "/Preferences.txt"

    classes = load_classes(classes_path)
    classrooms = load_classrooms(classrooms_path)
    teachers = load_teachers(teachers_path)
    likes, dislikes = load_preferences(preferences_path)

    return classes, classrooms, teachers, likes, dislikes
