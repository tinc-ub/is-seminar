import random
import json
import numpy as np

def get_names(first_path, middle_path, last_path):
    first, middle, last = [], [], []
    with open(first_path) as json_file:
        first = json.load(json_file)
    with open(middle_path) as json_file:
        middle = json.load(json_file)
    with open(last_path) as json_file:
        last = json.load(json_file)
    return first, middle, last

def get_classes(path):
    classes = []
    with open(path) as json_file:
        classes = json.load(json_file)
    return classes


def get_random_name(first, middle, last, middle_name_probability=0.5):
    first_name = random.choice(first)
    m = random.uniform(0, 1)
    middle_name = "_" + random.choice(middle) if (m < middle_name_probability) else ""
    last_name = "_" + random.choice(last)
    return first_name + middle_name + last_name

def get_random_class(classes):
    return random.choice(classes)

def create_classes_file(out_path, in_path, num_classes=20, num_classes_range=(1,10), len_lecture_range=(1,5)):
    classes = get_classes(in_path)
    while(len(classes) < num_classes):
        classes.append("CLx" + str(len(classes)))
    selected_classes = np.random.choice(classes, replace=False, size=num_classes)

    lectures = []
    for _ in range(num_classes):
        num_lectures = random.randrange(num_classes_range[0], num_classes_range[1])
        durations = []
        for _ in range(num_lectures):
            durations.append(random.randrange(len_lecture_range[0], len_lecture_range[1]))
        lectures.append(durations)

    with open(out_path, "w") as f:
        for c, durations in zip(selected_classes, lectures):
            f.write(c + " " + str(durations) + "\n")
    return selected_classes, lectures

def create_classroom_file(out_path, num_classrooms=20, classroom_open_range=(5, 22)):
    first_letter = ["P", "S", "X"]
    classrooms = []
    for i in range(num_classrooms):
        classrooms.append(random.choice(first_letter) + str(i+1))

    open_hours = []
    for _ in range(num_classrooms):
        p = np.random.choice(list(range(classroom_open_range[0], classroom_open_range[1] + 1)), replace=False, size=2)
        p.sort()
        open_hours.append([int(p[0]), int(p[1])])

    with open(out_path, "w") as f:
        for i in range(num_classrooms):
            f.write(classrooms[i] + " " + str(open_hours[i]) + "\n")

def create_teacher_file(out_path, first_path, middle_path, last_path, classes, num_teachers=30, num_classes_range=(1,5)):
    first, middle, last = get_names(first_path, middle_path, last_path)
    teachers = []
    for _ in range(num_teachers):
        teachers.append(get_random_name(first, middle, last))

    teacher_classes = []
    for _ in range(num_teachers):
        num_classes = random.randrange(num_classes_range[0], num_classes_range[1])
        selected_classes = np.random.choice(classes, replace=False, size=num_classes)
        selected_classes = [str(sl) for sl in selected_classes]
        teacher_classes.append(selected_classes)

    with open(out_path, "w") as f:
            for i in range(num_teachers):
                teacher_classes_str = "["
                for tc in teacher_classes[i][:-1]:
                    teacher_classes_str += tc + ", "
                teacher_classes_str += teacher_classes[i][-1] + "]"
                f.write(teachers[i] + " " + teacher_classes_str + "\n")
    return teachers

def create_preferences_file(out_path, teachers, classroom_open_range=(5, 22), probability_likes_first=0.8):
    preferences = []
    for _ in range(len(teachers)):
        p = np.random.choice(list(range(classroom_open_range[0], classroom_open_range[1] + 1)), replace=False, size=4)
        p.sort()
        if random.uniform(0, 1) < probability_likes_first:
            likes = [int(p[0]), int(p[1])]
            dislikes = [int(p[2]), int(p[3])]
        else:
            likes = [int(p[2]), int(p[3])]
            dislikes = [int(p[0]), int(p[1])]
        preferences.append({"likes": likes, "dislikes":dislikes})

    with open(out_path, "w") as f:
        for i in range(len(teachers)):
            f.write(teachers[i] + " " + str(preferences[i]) + "\n")

def generate(in_dir="random-name", out_dir="data"):
    classes,_ = create_classes_file(out_dir + "/Classes.txt", in_dir + "/classes-names.json", num_classes=10, len_lecture_range=(2,4))
    create_classroom_file(out_dir + "/Classrooms.txt", num_classrooms=20)
    teachers = create_teacher_file(out_dir + "/Teachers.txt", in_dir + "/first-names.json", in_dir + "/middle-names.json", in_dir + "/last-names.json", classes, num_teachers=50)
    create_preferences_file(out_dir + "/Preferences.txt", teachers)

generate()