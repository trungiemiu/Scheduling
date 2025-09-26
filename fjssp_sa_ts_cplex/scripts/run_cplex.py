import argparse
import matplotlib.pyplot as plt
from src.solvers.cplex_mip import solve_cplex_mip
from src.viz.plotting import plot_gantt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--time-limit", type=float, default=150.0)
    p.add_argument("--gap", type=float, default=0.20)
    p.add_argument("--no-log", action="store_true")
    p.add_argument("--plot", action="store_true")
    args = p.parse_args()

    res = solve_cplex_mip(args.data, timelimit_sec=args.time_limit, mipgap=args.gap, display_log=(not args.no_log))
    print("Cmax = {:.3f}".format(res["Cmax"]))
    for line in res["lines"]:
        print(line)
    if args.plot:
        plot_gantt(res["gantt"], title="Gantt Chart - CPLEX")
        plt.show()

if __name__ == "__main__":
    main()
