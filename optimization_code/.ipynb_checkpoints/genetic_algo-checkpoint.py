import random

import pygad

function_inputs = [4, 10, 5, 5]  # dummy starting gene


def fitness_func(ga_instance, solution: [int], solution_idx):
    # return sf.score_encoding(solution)
    return random.randint(1, 100)


# Some parameters to set, to be tweaked later
num_generations = 5
num_parents_mating = 4
fitness_function = fitness_func
sol_per_pop = 8
num_genes = len(function_inputs)

init_range_low = 0  # lowest possible duration in seconds
init_range_high = 90  # highest possible duration in seconds

# these are from pygad docs
parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10

ga_instance = pygad.GA(
    num_generations=num_generations,
    num_parents_mating=num_parents_mating,
    fitness_func=fitness_function,
    sol_per_pop=sol_per_pop,
    num_genes=num_genes,
    init_range_low=init_range_low,
    init_range_high=init_range_high,
    parent_selection_type=parent_selection_type,
    keep_parents=keep_parents,
    crossover_type=crossover_type,
    mutation_type=mutation_type,
    mutation_percent_genes=mutation_percent_genes,
)

ga_instance.run()
