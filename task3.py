import pygad
import numpy as np
from task1_modules import initialize_schedule, make_fitness, set_gene_space, visualize, lexicographic_parent_selection
from task2_generate_init_pop import generate_initial_population
from task2_crossover import crossover_classes, mutate_classes
from task4_load_schedule import load


if __name__ == "__main__":
    classes, classrooms, teachers, likes, dislikes = load("data/realistic")

    gene_space = set_gene_space(classes, classrooms, teachers)

    which = 2

    sol_per_pop = 100
    initial_population = generate_initial_population(sol_per_pop, classes, classrooms, teachers)
    schedule = make_fitness(classes, classrooms, teachers, likes, dislikes, which)
    if which == 2:
        ga_instance = pygad.GA(fitness_func=schedule,
                            num_generations=500,                       # number of generations
                            num_parents_mating=20,                      # number of parents selected for mutation/crossover
                            sol_per_pop=sol_per_pop,                            # population size
                            num_genes=len(gene_space),                  # 3 genes per session
                            initial_population=initial_population,
                            gene_space=gene_space,
                            crossover_type=crossover_classes,
                            mutation_type=mutate_classes,
                            gene_type=int,
                            keep_elitism=0,
                            keep_parents=-1,
                            parent_selection_type=lexicographic_parent_selection)
    else:
        ga_instance = pygad.GA(fitness_func=schedule,
                            num_generations=500,                       # number of generations
                            num_parents_mating=20,                      # number of parents selected for mutation/crossover
                            sol_per_pop=sol_per_pop,                     # population size
                            num_genes=len(gene_space),                  # 3 genes per session
                            initial_population=initial_population,
                            gene_space=gene_space,
                            crossover_type=crossover_classes,
                            mutation_type=mutate_classes,
                            gene_type=int)

    ga_instance.run()

    if which == 2:
        fitness = np.array(ga_instance.last_generation_fitness)
        order = np.lexsort((-fitness[:, 1], -fitness[:, 0]))
        solution_idx = order[0]
        solution = ga_instance.population[solution_idx]
        solution_fitness = fitness[solution_idx]
    else:
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
    
    print("best schedule",solution)

    if which == 2:
        print("Fitness (hard constraints)", solution_fitness[0])
        print("Fitness (soft constraints)", solution_fitness[1])
    else:
        print("Fitness", solution_fitness)
        print("Index", solution_idx)
    visualize(solution, classes, classrooms, teachers)