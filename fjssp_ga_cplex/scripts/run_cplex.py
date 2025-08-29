import argparse

from cplex_solver.cplex_solver import solve_from_excel
from ga.viz import chromosome_gantt_chart


def main(input_file: str, bigM: float = 1e7, viz: bool = False):
    print(f"[CPLEX] Solving: {input_file}")
    res = solve_from_excel(input_file, bigM=bigM)

    print("==== CPLEX Result ====")
    print("Cmax:", res["Cmax"])
    print(f"|X| active: {len(res['X1'])}, |Z| chosen: {len(res['Z1'])}")

    if viz:
        try:
            chromosome = res["chromosome_ga"]
            machines = res["machines_chosen_ga"]
            processing_times = res["processing_times_ga"]
            chromosome_gantt_chart(chromosome, machines, processing_times,
                       title=args.title or "Gantt Chart")
        except Exception as e:
            print(f"[WARN] Visualization failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run CPLEX solver for FJSSP")
    parser.add_argument("--input", type=str, required=True, help="Path to Excel input file")
    parser.add_argument("--bigM", type=float, default=1e7, help="Big-M value")
    parser.add_argument("--viz", action="store_true", help="Plot Gantt Chart")
    parser.add_argument("--title", type=str, default=None, help="Name of Gantt Chart")
    args = parser.parse_args()

    main(input_file=args.input, bigM=args.bigM, viz=args.viz)
