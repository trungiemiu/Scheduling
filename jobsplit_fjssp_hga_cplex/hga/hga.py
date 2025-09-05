from __future__ import annotations
from typing import List, Tuple, Dict, Optional
import random
import numpy as np

from .population import create_population
from .selection import binary_selection
from .crossover import crossover
from .mutation import mutation
from .scheduling import calculate_makespan

Lookup = Dict[tuple, float]


def ga(
    pop_size: int,
    max_iteration: int,
    lot_size: List[int],
    processing_lookup: Lookup,
    num_machine: int,
    num_operation: int,
    s: int,
    beta: int,
    elite_k: int = 2,
    seed: Optional[int] = None,
) -> Tuple[dict, float, List[float]]:
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    num_jobs = len(lot_size)
    population = create_population(pop_size, num_jobs, num_operation, lot_size, num_machine, s, processing_lookup)

    def fitness(chrom: dict) -> float:
        mk, _ = calculate_makespan(chrom, lot_size, processing_lookup, num_machine, num_operation)
        return mk

    population.sort(key=fitness)
    best = population[0]
    best_mk = fitness(best)
    history = [best_mk]

    for _ in range(max_iteration):
        k = min(elite_k, len(population))
        elites = population[:k]

        need = pop_size - k
        offspring: List[dict] = []
        while len(offspring) < max(0, need):
            p1, p2 = binary_selection(population, lot_size, processing_lookup, num_machine, num_operation)
            c1, c2 = crossover(p1, p2, num_jobs, num_operation)
            c1 = mutation(c1, lot_size, processing_lookup, num_machine, num_operation, s, beta)
            c2 = mutation(c2, lot_size, processing_lookup, num_machine, num_operation, s, beta)
            offspring.extend([c1, c2])

        offspring.sort(key=fitness)
        offspring = offspring[:need]
        population = elites + offspring
        population.sort(key=fitness)

        cur_best = population[0]
        cur_mk = fitness(cur_best)
        if cur_mk < best_mk:
            best, best_mk = cur_best, cur_mk
        history.append(best_mk)

    return best, best_mk, history


def _main():
    import argparse
    from .io import read_job_scheduling_data
    from .plot import plot_history, plot_gantt_chart

    parser = argparse.ArgumentParser(
        prog="python -m hga.hga",
        description="Run Hybrid GA for Jobsplit-FJSSP."
    )
    parser.add_argument("--data", default="data/2data.xlsx", help="Path to data file (Excel).")
    parser.add_argument("--pop-size", type=int, default=12)
    parser.add_argument("--iters", type=int, default=40)
    parser.add_argument("--s", type=int, default=10, help="minimum sub-lot size (multiple).")
    parser.add_argument("--beta", type=int, default=5, help="beta in mutation (%).")
    parser.add_argument("--elite-k", type=int, default=2)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--save-history", type=str, default=None)
    parser.add_argument("--save-gantt", type=str, default=None)
    parser.add_argument("--no-show", action="store_true")

    args = parser.parse_args()

    num_jobs, num_ops, num_machs, lot_sizes, p_lookup = read_job_scheduling_data(args.data)
    best, best_mk, hist = ga(
        pop_size=args.pop_size,
        max_iteration=args.iters,
        lot_size=lot_sizes,
        processing_lookup=p_lookup,
        num_machine=num_machs,
        num_operation=num_ops,
        s=args.s,
        beta=args.beta,
        elite_k=args.elite_k,
        seed=args.seed,
    )

    mk, details = calculate_makespan(best, lot_sizes, p_lookup, num_machs, num_ops)

    print("========== GA Result ==========")
    print(f"Data file    : {args.data}")
    print(f"Best makespan: {mk}")
    print(f"Population   : {args.pop_size} | Generations: {args.iters} | Elite: {args.elite_k}")
    print(f"s = {args.s} | beta = {args.beta} | seed = {args.seed}")
    print("================================")

    if args.save_history:
        plot_history(hist, args.save_history)
        print(f"Saved history to: {args.save_history}")
    if args.save_gantt:
        plot_gantt_chart(details, args.save_gantt)
        print(f"Saved Gantt to  : {args.save_gantt}")
    if not args.no_show and not (args.save_history or args.save_gantt):
        plot_history(hist)
        plot_gantt_chart(details)


if __name__ == "__main__":
    _main()
