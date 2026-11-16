import pygad
import numpy as np
from task1_modules import initialize_schedule, make_fitness, set_gene_space, visualize
from task2_generate_init_pop import generate_initial_population

# swap all classes up to a random point between 2 consecutive parents
def crossover_classes(parents, offspring_size, ga_instance):
    offspring = []
    idx = 0
    while len(offspring) != offspring_size[0]:
        parent1 = parents[idx % parents.shape[0], :].copy()
        parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

        num_classes = offspring_size[1] // 3
        random_split_point = ga_instance.numpy_random_generator.choice(range(num_classes)) * 3

        parent1[random_split_point:] = parent2[random_split_point:]
        offspring.append(parent1)
        idx += 1
    return np.array(offspring)

# randomly assign one whole class
def mutate_classes(offspring, ga_instance):
    for chromosome_idx in range(offspring.shape[0]):
        num_classes = offspring.shape[1] // 3
        random_gene_idx = ga_instance.numpy_random_generator.choice(range(num_classes)) * 3

        for gene_idx in range(random_gene_idx, random_gene_idx + 3):
            space = ga_instance.gene_space[gene_idx]
            offspring[chromosome_idx, gene_idx] = ga_instance.numpy_random_generator.choice(space)
    return offspring

if __name__ == "__main__":
    classes, classrooms, teachers = initialize_schedule()
    gene_space = set_gene_space(classes, classrooms, teachers)

    sol_per_pop = 100
    initial_population = generate_initial_population(sol_per_pop, classes, classrooms, teachers)
    schedule = make_fitness(classes, classrooms, teachers)
        
    ga_instance = pygad.GA(fitness_func=schedule,
                        num_generations=1000,                       # number of generations
                        num_parents_mating=20,                      # number of parents selected for mutation/crossover
                        sol_per_pop=sol_per_pop,                            # population size
                        num_genes=len(gene_space),                  # 3 genes per session
                        initial_population=initial_population,
                        gene_space=gene_space,
                        crossover_type=crossover_classes,
                        mutation_type=mutate_classes,
                        gene_type=int)
    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("best schedule",solution)

    print("Fitness", solution_fitness)
    print("Index", solution_idx)
    visualize(solution, classes, classrooms, teachers)