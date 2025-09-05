import argparse
from cplex_solver.cplex_solver import build_and_solve


def main():
    parser = argparse.ArgumentParser(
        prog="python scripts/run_cplex.py",
        description="Run CPLEX MIP for Job-Splitting FJSSP (Cmax)"
    )
    parser.add_argument("--xlsx", type=str, default="data/2data.xlsx",
                        help="Path to Excel data file.")
    parser.add_argument("--smin", type=int, default=10,
                        help="Minimum sub-lot size s (enforces α_ijk ≥ s when used).")
    parser.add_argument("--timelimit", type=int, default=600,
                        help="Time limit in seconds.")
    parser.add_argument("--mipgap", type=float, default=0.0,
                        help="Relative MIP gap (e.g., 0.01 for 1%).")
    parser.add_argument("--no-log", action="store_true",
                        help="Disable solver log output.")
    args = parser.parse_args()

    build_and_solve(
        xlsx_path=args.xlsx,
        s_min=args.smin,
        timelimit=args.timelimit,
        mipgap=args.mipgap,
        log_output=(not args.no_log),
    )


if __name__ == "__main__":
    main()
