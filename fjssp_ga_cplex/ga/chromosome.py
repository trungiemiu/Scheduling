import random
from collections import defaultdict


def create_chromosome(machines, order):
    machine_to_ops = defaultdict(list)
    for op, machines_list in machines.items():
        for job_index, machine_id in enumerate(machines_list):
            machine_to_ops[machine_id].append(f'J{job_index + 1}O{op}')

    chromosome = []
    used_operations = set()
    for machine_id in order:
        available_ops = [op for op in machine_to_ops[machine_id] if op not in used_operations]
        random.shuffle(available_ops)
        chromosome.extend(available_ops)
        used_operations.update(available_ops)
    return chromosome


def generate_population(machines, order, population_size):
    population = set()
    while len(population) < population_size:
        population.add(tuple(create_chromosome(machines, order)))
    return [list(chrom) for chrom in population]
