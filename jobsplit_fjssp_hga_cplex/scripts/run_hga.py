import argparse
from hga.hga import ga
from hga.io import read_job_scheduling_data
from hga.plot import plot_history, plot_gantt_chart
from hga.scheduling import calculate_makespan


def main():
    parser = argparse.ArgumentParser(
        prog="python scripts/run_hga.py",
        description="Run Hybrid GA for Job-Splitting FJSSP"
    )
    parser.add_argument("--data", default="data/2data.xlsx", help="Path to Excel data file.")
    parser.add_argument("--pop-size", type=int, default=20, help="Population size.")
    parser.add_argument("--iters", type=int, default=50, help="Number of generations.")
    parser.add_argument("--s", type=int, default=10, help="Minimum sub-lot size (HGA uses multiples of s).")
    parser.add_argument("--beta", type=int, default=5, help="Local search step (percent/units depending on your LSA).")
    parser.add_argument("--elite-k", type=int, default=2, help="Number of elites kept each generation.")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility.")
    parser.add_argument("--save-history", type=str, default=None, help="Path to save history plot (PNG).")
    parser.add_argument("--save-gantt", type=str, default=None, help="Path to save Gantt chart (PNG).")
    parser.add_argument("--no-show", action="store_true", help="Do not show plots interactively.")
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
    print("========== HGA Result ==========")
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
    main()
