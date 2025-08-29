from .schedule import calculate_makespan, get_operation_details
from .chromosome import generate_population
from .operators import select, divide_into_pairs, pair_crossover, mutate


def genetic_algorithm(machines, processing_times, order, population_size, generations, mutation_rate):
    population = generate_population(machines, order, population_size)
    makespan_history = []
    operation_details_history = []
    for _ in range(generations):
        num_mutated = int(mutation_rate * len(population))
        mutation_population, crossover_population = select(population, machines, processing_times, num_mutated)
        pairs, one = divide_into_pairs(crossover_population)
        if one is not None:
            mutation_population.append(one)

        crossed_population = []
        for pair in pairs:
            children = pair_crossover(pair, machines, processing_times)
            crossed_population.extend(children)

        mutated_population = mutate(mutation_population, machines, processing_times)
        population = crossed_population + mutated_population

        best_child = min(population, key=lambda chrom: calculate_makespan(chrom, machines, processing_times))
        makespan_history.append(calculate_makespan(best_child, machines, processing_times))
        operation_details_history.append(get_operation_details(best_child, machines, processing_times))
    
    best_chromosome = min(population, key=lambda chrom: calculate_makespan(chrom, machines, processing_times))
    best_makespan = calculate_makespan(best_chromosome, machines, processing_times)
    return best_chromosome, best_makespan, makespan_history, operation_details_history
