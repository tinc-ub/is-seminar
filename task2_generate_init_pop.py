import pygad
from task1_modules import initialize_schedule, make_fitness, set_gene_space, visualize

# We greedily go in order of classes and find the first slot we can assign the class to.
# The time slots are ordered by ["classroom", "time"] so we first try to assign
# the class to classroom 0, then classroom 1, ...
# If we can't assign the class to the current classroom, we move on and do not to try to
# fill the empty class in later attempts.
# We assign the first teachr that fits.
def generate_initial_population(sol_per_pop, classes, classrooms, teachers):
    cur_time = classrooms[0][1] # the time up to which we have greedily filled classes
    open_until_time = classrooms[0][2]
    classroom = 0

    population = []
    for _ in range(sol_per_pop):
        gene = []
        for subject, duration in classes:
            while open_until_time - cur_time < duration: # We assume there is a room that can fit the class duration.
                classroom = (classroom + 1) % len(classrooms) # We loop classrooms and "clear" the classrooms
                cur_time = classrooms[classroom][1]
                open_until_time = classrooms[classroom][2]

            for i, (_, subjects) in enumerate(teachers):
                if subject in subjects:
                    gene.append(classroom)
                    gene.append(i)
                    gene.append(cur_time)
                    cur_time += duration
                    break
        population.append(gene)
    return population

if __name__ == "__main__":
    classes, classrooms, teachers, likes, dislikes = initialize_schedule()
    gene_space = set_gene_space(classes, classrooms, teachers)

    which = 2

    sol_per_pop = 100
    initial_population = generate_initial_population(sol_per_pop, classes, classrooms, teachers)
    print("The initial population generated using greedy algorithm.")
    visualize(initial_population[0], classes, classrooms, teachers)
    visualize(initial_population[1], classes, classrooms, teachers)
    visualize(initial_population[2], classes, classrooms, teachers)

    schedule = make_fitness(classes, classrooms, teachers, likes, dislikes, which)
    ga_instance = pygad.GA(fitness_func=schedule,
                        num_generations=1000,                       # number of generations
                        num_parents_mating=20,                      # number of parents selected for mutation/crossover
                        sol_per_pop=sol_per_pop,                            # population size
                        num_genes=len(gene_space),                  # 3 genes per session
                        initial_population=initial_population,
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