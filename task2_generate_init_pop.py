import pygad
import random
from task1_modules import initialize_schedule, make_fitness, set_gene_space, visualize
from task4_load_schedule import load

# We start with a random classrom, then we greedily go in order of classes and find the first slot we can assign the class to.
# If we can't assign the class to the current classroom, we move on.
# We assign a random first teacher that fits.
# If we 'filler' every classroom we simple go on and treet each classroom as empty
def generate_initial_population(sol_per_pop, classes, classrooms, teachers):
    population = []
    shuffled_classes = list(enumerate(classes))
    for _ in range(sol_per_pop):
        classroom = random.choice(list(range(len(classrooms)))) # Randomly start with one classroom
        cur_time = classrooms[classroom][1] # the time up to which we have greedily filled classes
        open_until_time = classrooms[classroom][2]
        
        gene = [0] * (3 * len(classes))

        random.shuffle(shuffled_classes)
        for idx, (subject, duration) in shuffled_classes:
            while open_until_time - cur_time + 1 < duration: # We assume there is a room that can fit the class duration.
                classroom = (classroom + 1) % len(classrooms) # We loop classrooms and "clear" the classrooms
                cur_time = classrooms[classroom][1]
                open_until_time = classrooms[classroom][2]

            elegible_teachers = [i for i, (_, subjects) in enumerate(teachers) if subject in subjects]
            selected_teacher = random.choice(elegible_teachers)

            gene[3*idx] = classroom
            gene[3*idx + 1] = selected_teacher
            gene[3*idx + 2] = cur_time
            cur_time += duration

        population.append(gene)
    return population

if __name__ == "__main__":
    classes, classrooms, teachers, likes, dislikes = load("data/realistic")
    gene_space = set_gene_space(classes, classrooms, teachers)

    sol_per_pop = 50
    initial_population = generate_initial_population(sol_per_pop, classes, classrooms, teachers)
    print("The initial population generated using greedy algorithm.")
    visualize(initial_population[0], classes, classrooms, teachers)
    visualize(initial_population[1], classes, classrooms, teachers)
    visualize(initial_population[2], classes, classrooms, teachers)

    schedule = make_fitness(classes, classrooms, teachers, likes, dislikes)
    ga_instance = pygad.GA(fitness_func=schedule,
                        num_generations=100,                        # number of generations
                        num_parents_mating=20,                      # number of parents selected for mutation/crossover
                        sol_per_pop=sol_per_pop,                            # population size
                        num_genes=len(gene_space),                  # 3 genes per session
                        initial_population=initial_population,
                        gene_space=gene_space,
                        gene_type=int)
    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("best schedule",solution)

    print("Fitness", solution_fitness)
    print("Index", solution_idx)
    visualize(solution, classes, classrooms, teachers)