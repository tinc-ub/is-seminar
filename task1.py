import pygad
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt 

#represent schedule
# an array of subject, duration

classes = [
    ("Programming", 2),
    ("Programming", 3),
    ("Programming", 2),
    ("Programming", 2),
    ("Math", 2),
    ("Math", 2),
    ("Algorithms", 2),
    ("Algorithms", 3),
    ("OperatingSystems", 2),
    ("OperatingSystems", 2),
]



classrooms = [
    ("P1", 10, 16),
    ("P2", 8, 16),
    ("P3", 10, 16),
    ("P4", 10, 16),
]

teachers = [
    ("Anna", ["Programming", "Math"]),
    ("Brian", ["Programming", "Algorithms", "OperatingSystems"]),
    ("Charles", ["Math"]),
    ("Diana", ["Algorithms", "OperatingSystems"]),
]

likes = [
    ("Anna", [10, 11]),
    ("Brian", [10, 14]),
    ("Charles", [10, 11]),
    ("Diana", [10, 14])
]

dislikes = [
    ("Anna", [12, 14]),
    ("Brian", [15, 16]),
    ("Charles", [12, 16]),
    ("Diana", [15, 16])
]

#genes are then (classroom, teacher, starHour)
#eg. (P1,Anna, 10) on position 0 which implies programming 2 hours long


def lexicographic_parent_selection(fitness, num_parents, ga_instance):
    # fitness shape: (pop_size, 2) -> column 0 = hard, column 1 = soft
    order = np.lexsort((-fitness[:, 1], -fitness[:, 0]))  # primary key last: hard first, soft as tiebreaker
    parent_indices = order[:num_parents]
    parents = ga_instance.population[parent_indices]
    return parents, parent_indices


#conditions:
#everything being present,
#lectures having a classroom that is availibe and free
#lectures havin their teachr and none of the teacher are teching multiple
#at the same time

#make reading solution easier
def easier(solution):
    lectures = []
    for i in range(len(classes)):
        classroom = classrooms[int(solution[i * 3])]
        teacher = teachers[int(solution[i * 3 + 1])]
        start = solution[i * 3 + 2]
        subject = classes[i][0]
        duration = classes[i][1]

        lectures.append({
            "subject": subject,
            "teacher": teacher,
            "start":start,
            "end":start +duration,
            "duration": duration,
            "classroom": classroom
        })
    return lectures

def schedule(ga_instance, solution, solution_idx):
    
    lectures = easier(solution)

    penalty = 0

    for i in lectures:
        roomName, roomStart, roomEnd= i["classroom"]
        if i["start"]<roomStart: penalty+=1
        if (i["start"]+i["duration"]) > roomEnd: penalty+=1

        teacher, teachesSubject= i["teacher"]
        if i["subject"] not in teachesSubject: penalty+=1

    for i in range(len(lectures)):
        for j in range(i+1, len(lectures)):
            a=lectures[i]
            b=lectures[j]

            both = a["start"] < b["end"] and a["end"] > b["start"]

            if both: 
                if a["classroom"] == b["classroom"]: penalty+=1
                if a["teacher"] == b["teacher"]: penalty +=1

    return -penalty

def schedule2(ga_instance, solution, solution_idx):
    
    lectures = easier(solution)

    penalty = 0
    penalty2 = 0

    for i in lectures:
        roomName, roomStart, roomEnd= i["classroom"]
        if i["start"]<roomStart: penalty+=1
        if (i["start"]+i["duration"]) > roomEnd: penalty+=1

        teacher, teachesSubject= i["teacher"]
        if i["subject"] not in teachesSubject: penalty+=1

    for i in range(len(lectures)):
        for j in range(i+1, len(lectures)):
            a=lectures[i]
            b=lectures[j]

            both = a["start"] < b["end"] and a["end"] > b["start"]

            if both: 
                if a["classroom"] == b["classroom"]: penalty+=1
                if a["teacher"] == b["teacher"]: penalty +=1

    
    hours = {}

    for name,sub in teachers:
        hours[name] = 0

    for lecture in lectures:
        name = lecture["teacher"][0]
        hours[name]+= lecture["duration"]

    maxi = max(hours.values())
    mini = min(hours.values())

    penalty2 += (maxi -mini)/100


    for i in range(len(lectures)):
        l = dict(likes)
        d = dict(dislikes)
        
        teach = lectures[i]["teacher"][0]
        hours = [lectures[i]["start"],lectures[i]["end"]]
        like = l[teach]
        dislike = d[teach]

        withinLikes = hours[0] < like[1] and hours[1] > like[0]
        withinDislikes = hours[0] < dislike[1] and hours[1] > dislike[0]

        if withinLikes: penalty2 = penalty2 - 1/100
        if withinDislikes: penalty2+=1/100



    return [-penalty, -penalty2]

def schedule3(ga_instance, solution, solution_idx):
    
    lectures = easier(solution)

    penalty = 0
    penalty2 = 0

    for i in lectures:
        roomName, roomStart, roomEnd= i["classroom"]
        if i["start"]<roomStart: penalty+=100
        if (i["start"]+i["duration"]) > roomEnd: penalty+=100

        teacher, teachesSubject= i["teacher"]
        if i["subject"] not in teachesSubject: penalty+=100

    for i in range(len(lectures)):
        for j in range(i+1, len(lectures)):
            a=lectures[i]
            b=lectures[j]

            both = a["start"] < b["end"] and a["end"] > b["start"]

            if both: 
                if a["classroom"] == b["classroom"]: penalty+=100
                if a["teacher"] == b["teacher"]: penalty +=100

    
    hours = {}

    for name,sub in teachers:
        hours[name] = 0

    for lecture in lectures:
        name = lecture["teacher"][0]
        hours[name]+= lecture["duration"]

    maxi = max(hours.values())
    mini = min(hours.values())

    penalty2 += (maxi -mini)/100


    for i in range(len(lectures)):
        l = dict(likes)
        d = dict(dislikes)
        
        teach = lectures[i]["teacher"][0]
        hours = [lectures[i]["start"],lectures[i]["end"]]
        like = l[teach]
        dislike = d[teach]

        withinLikes = hours[0] < like[1] and hours[1] > like[0]
        withinDislikes = hours[0] < dislike[1] and hours[1] > dislike[0]

        if withinLikes: penalty2 = penalty2 - 1/100
        if withinDislikes: penalty2+=1/100



    return -(penalty + penalty2)



gene_space = []
for _ in classes:
    gene_space.append(list(range(len(classrooms))))   # classroom index
    gene_space.append(list(range(len(teachers))))     # teacher index
    gene_space.append(list(range(8, 16)))             # start hour

ga_instance = pygad.GA(fitness_func=schedule3,
                       num_generations=500,                       # number of generations
                       num_parents_mating=30,                     # number of parents selected for mutation/crossover
                       sol_per_pop=200,                            # population size
                       num_genes=len(gene_space),                 # 3 genes per session
                       gene_space=gene_space,
                       gene_type=int)
ga_instance.run()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("best schedule",solution)
print("Fitsness", solution_fitness)

# print("Fitness (hard constraints)", solution_fitness[0])
# print("Fitness (soft constraints)", solution_fitness[1])
print("Index", solution_idx)

#####################################################
#AI generated visualisation

def visualize(solution):
    lectures = []
    for i in range(len(classes)):
        classroom = classrooms[int(solution[i * 3])]
        teacher = teachers[int(solution[i * 3 + 1])]
        start = solution[i * 3 + 2]
        subject = classes[i][0]
        duration = classes[i][1]

        lectures.append({
            "subject": subject,
            "teacher": teacher[0],
            "start": start,
            "duration": duration,
            "classroom": classroom[0],
        })

    room_names = [c[0] for c in classrooms]
    subjects = sorted(set(c[0] for c in classes))
    colors = plt.cm.tab10.colors
    subject_color = {s: colors[i % len(colors)] for i, s in enumerate(subjects)}

    fig, ax = plt.subplots(figsize=(8, 6))

    for lecture in lectures:
        x = room_names.index(lecture["classroom"])
        ax.bar(x, lecture["duration"], bottom=lecture["start"], width=0.6,
               color=subject_color[lecture["subject"]], edgecolor="black")
        ax.text(x, lecture["start"] + lecture["duration"] / 2,
                f"{lecture['subject']}\n{lecture['teacher']}",
                ha="center", va="center", fontsize=8)

    ax.set_xticks(range(len(room_names)))
    ax.set_xticklabels(room_names)
    ax.set_ylabel("Hour")
    ax.set_ylim(16, 8)
    ax.set_title("Best schedule")
    plt.tight_layout()
    plt.show()
#################################################################################

visualize(solution)