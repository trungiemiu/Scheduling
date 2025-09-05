from __future__ import annotations
from typing import List, Dict, Tuple
from .encoding import create_chromosome, is_duplicate_chromosome

Lookup = Dict[Tuple[int,int,int], float]

def create_population(
    pop_size: int,
    num_job: int,
    num_operation: int,
    lot_size: List[int],
    num_machine: int,
    s: int,
    processing_lookup: Lookup,
) -> List[dict]:
    population: List[dict] = []
    attempts = 0
    max_attempts = max(pop_size * 50, 100)
    while len(population) < pop_size and attempts < max_attempts:
        chrom = create_chromosome(num_job, num_operation, lot_size, num_machine, s, processing_lookup)
        if not is_duplicate_chromosome(chrom, population):
            population.append(chrom)
        attempts += 1
    if not population:
        raise RuntimeError("Failed to create initial population.")
    return population
