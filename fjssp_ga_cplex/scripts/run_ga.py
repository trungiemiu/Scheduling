import argparse
from ga.mainga import ga_optimize


def main(input_file=None, pop=10, gen=50, mut=0.1, visualize=False):
    result = ga_optimize(
        data_path=input_file,
        population_size=pop,
        generations=gen,
        mutation_rate=mut,
        visualize=visualize,
    )
    print(f"[Genetic Algorithm] Solving: {input_file}")

    print("==== GA Result ====")
    print("Best makespan:", result["best_makespan"])
    print("Best chromosome:", result["best_chromosome"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Genetic Algorithm for FJSSP")
    parser.add_argument("--input", type=str, default=None, help="Path to Excel input (default: data/Data.xlsx)")
    parser.add_argument("--pop", type=int, default=10, help="Population size")
    parser.add_argument("--gen", type=int, default=50, help="Number of generations")
    parser.add_argument("--mut", type=float, default=0.1, help="Mutation rate")
    parser.add_argument("--viz", action="store_true", help="Enable visualization")
    args = parser.parse_args()
    main(input_file=args.input, pop=args.pop, gen=args.gen, mut=args.mut, visualize=args.viz)
