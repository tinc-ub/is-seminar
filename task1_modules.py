import pygad
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt 

#represent schedule
# an array of subject, duration

def initialize_schedule():
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

    return classes, classrooms, teachers, likes, dislikes

#genes are then (classroom, teacher, starHour)
#eg. (P1,Anna, 10) on position 0 which implies programming 2 hours long


#conditions:
#everything being present,
#lectures having a classroom that is availibe and free
#lectures havin their teachr and none of the teacher are teching multiple
#at the same time

#make reading solution easier
def easier(solution, classes, classrooms, teachers):
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

def lexicographic_parent_selection(fitness, num_parents, ga_instance):
    order = np.lexsort((-fitness[:, 1], -fitness[:, 0]))  # hard first, soft as tiebreaker
    parent_indices = order[:num_parents]
    parents = ga_instance.population[parent_indices]
    return parents, parent_indices

def make_fitness(classes, classrooms, teachers, likes, dislikes, which=1):
    def schedule(ga_instance, solution, solution_idx):
        lectures = easier(solution, classes, classrooms, teachers)
        penalty = 0

        for i in lectures:
            roomName, roomStart, roomEnd= i["classroom"]
            if i["start"]<roomStart: penalty+=1
            if (i["start"]+i["duration"]) > roomEnd: penalty+=1

            #teacher, teachesSubject= i["teacher"] # should never happen due to gene space constrains
            #if i["subject"] not in teachesSubject: penalty+=1

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
        lectures = easier(solution, classes, classrooms, teachers)
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

            #if withinLikes: penalty2 = penalty2 - 1/100
            if withinDislikes: penalty2+=1/100

        return [-penalty, -penalty2]

    def schedule3(ga_instance, solution, solution_idx):
        lectures = easier(solution, classes, classrooms, teachers)
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



    fitness_funcs = {1: schedule, 2: schedule2, 3: schedule3}
    if which not in fitness_funcs:
        raise ValueError("which must be 1, 2, or 3")
    return fitness_funcs[which]

def set_gene_space(classes, classrooms, teachers):
    gene_space = []
    starthour = min([h for _,h,_ in classrooms])
    endhour = max([h for _,_,h in classrooms]) - 1
    for name, _ in classes:
        gene_space.append(list(range(len(classrooms))))   # classroom index
        gene_space.append([
            i for i, (_, subjects) in enumerate(teachers) if name in subjects
        ])                                                # teacher index (only valid teachers)
        gene_space.append(list(range(starthour, endhour)))             # start hour
    return gene_space

#####################################################
#AI generated visualisation

def visualize(solution, classes, classrooms, teachers):
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

    starthour = min([h for _,h,_ in classrooms])
    endhour = max([h for _,_,h in classrooms])

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
    ax.set_yticks(range(starthour, endhour+1))
    ax.set_ylabel("Hour")
    ax.set_ylim(starthour, endhour)
    ax.set_title("Best schedule")
    plt.tight_layout()
    plt.show()
#################################################################################






    


# makes it so this code is run only, when run as a script
if __name__ == "__main__":
    classes, classrooms, teachers, likes, dislikes = initialize_schedule()
    gene_space = set_gene_space(classes, classrooms, teachers)

    which = 3


    schedule = make_fitness(classes, classrooms, teachers, likes, dislikes, which) # so that easier() can get args passed to
    ga_instance = pygad.GA(fitness_func=schedule,
                        num_generations=1000,                       # number of generations
                        num_parents_mating=20,                      # number of parents selected for mutation/crossover
                        sol_per_pop=200,                            # population size
                        num_genes=len(gene_space),                  # 3 genes per session
                        gene_space=gene_space,
                        gene_type=int)
    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("best schedule",solution)

    if which == 2:
        print("Fitness (hard constraints)", solution_fitness[0])
        print("Fitness (soft constraints)", solution_fitness[1])
    else:
        print("Fitness", solution_fitness)
        print("Index", solution_idx)
    visualize(solution, classes, classrooms, teachers)