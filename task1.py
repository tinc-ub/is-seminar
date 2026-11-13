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

#genes are then (classroom, teacher, starHour)
#eg. (P1,Anna, 10) on position 0 which implies programming 2 hours long





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


gene_space = []
for _ in classes:
    gene_space.append(list(range(len(classrooms))))   # classroom index
    gene_space.append(list(range(len(teachers))))     # teacher index
    gene_space.append(list(range(8, 16)))             # start hour

ga_instance = pygad.GA(fitness_func=schedule,
                       num_generations=1000,                       # number of generations
                       num_parents_mating=20,                     # number of parents selected for mutation/crossover
                       sol_per_pop=200,                            # population size
                       num_genes=len(gene_space),                 # 3 genes per session
                       gene_space=gene_space,
                       gene_type=int)
ga_instance.run()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("best schedule",solution)


print("Fitness", solution_fitness)
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