import argparse
import matplotlib.pyplot as plt
from src.core.io_utils import load_data_from_excel, print_schedule
from src.core.scheduler import objective_makespan
from src.heuristics.tabu import tabu_search
from src.viz.plotting import plot_gantt, plot_history

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--max-iter", type=int, default=300)
    p.add_argument("--tabu", type=int, default=7)
    p.add_argument("--plot", action="store_true")
    args = p.parse_args()

    machines, jobs = load_data_from_excel(args.data)
    best_jobs, best_machines, hist = tabu_search(jobs, machines, args.max_iter, args.tabu)

    print("Best Cmax:", objective_makespan(best_machines))
    print_schedule((best_jobs, best_machines))

    if args.plot:
        plot_gantt((best_jobs, best_machines), title="Gantt Chart - TS")
        plot_history(hist, title="TS – Best Cmax History")
        plt.show()

if __name__ == "__main__":
    main()



