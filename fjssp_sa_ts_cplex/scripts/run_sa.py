import argparse
import matplotlib.pyplot as plt
from src.core.io_utils import load_data_from_excel, print_schedule
from src.core.scheduler import objective_makespan
from src.heuristics.sa import simulated_annealing
from src.viz.plotting import plot_gantt, plot_history

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--initial-temp", type=float, default=1000)
    p.add_argument("--cooling-rate", type=float, default=0.85)
    p.add_argument("--max-iter", type=int, default=200)
    p.add_argument("--hints-per-move", type=int, default=2)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--plot", action="store_true")
    args = p.parse_args()

    machines, jobs = load_data_from_excel(args.data)
    best_jobs, best_machines, hist = simulated_annealing(
        jobs, machines,
        initial_temp=args.initial_temp,
        cooling_rate=args.cooling_rate,
        max_iter=args.max_iter,
        n_hints_per_move=args.hints_per_move,
        seed=args.seed
    )

    print("Best Cmax:", objective_makespan(best_machines))
    print_schedule((best_jobs, best_machines))

    if args.plot:
        plot_gantt((best_jobs, best_machines), title="Gantt Chart - SA")
        plot_history(hist, title="SA – Best Cmax History")
        plt.show()

if __name__ == "__main__":
    main()


