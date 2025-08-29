# ga/mainga.py
from pathlib import Path
from typing import Optional, Dict, Any

from .io import read_parameters_from_excel
from .ga import genetic_algorithm
from .utils import generate_color_map
from .viz import (
    animate_gantt_and_makespan,
    plot_makespan_history,
    chromosome_gantt_chart,
)

def ga_optimize(
    data_path: Optional[str] = None,
    population_size: int = 10,
    generations: int = 50,
    mutation_rate: float = 0.1,
    visualize: bool = False,
) -> Dict[str, Any]:
    if data_path is None:
        here = Path(__file__).resolve().parent
        data_path = str((here.parent / "data" / "Data.xlsx").resolve())

    machines, processing_times, order = read_parameters_from_excel(data_path)
    best_chrom, best_mk, mk_hist, det_hist = genetic_algorithm(
        machines, processing_times, order, population_size, generations, mutation_rate
    )

    if visualize:
        try:
            import matplotlib.pyplot as plt
            num_jobs = max(len(machine_list) for machine_list in machines.values())
            color_map = generate_color_map(num_jobs)
            animate_gantt_and_makespan(det_hist, mk_hist, color_map, len(det_hist))
            plot_makespan_history(mk_hist)
            chromosome_gantt_chart(best_chrom, machines, processing_times)
        except Exception as e:
            print(f"[WARN] Visualization skipped: {e}")

    return {
        "best_chromosome": best_chrom,
        "best_makespan": best_mk,
        "makespan_history": mk_hist,
        "details_history": det_hist,
        "data_path": data_path,
    }
