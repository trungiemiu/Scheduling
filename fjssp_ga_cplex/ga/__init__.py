from .io import read_data
from .gene import parse_gene
from .schedule import get_operation_details, calculate_makespan
from .chromosome import create_chromosome, generate_population

from .operators import (
    select,
    divide_into_pairs,
    fix_duplicates,
    pair_crossover,
    individual_mutate,
    mutate,
)

from .ga import genetic_algorithm
from .viz import (
    plot_makespan_history,
    plot_gantt_chart,
    animate_gantt_and_makespan,
    chromosome_gantt_chart,
)
