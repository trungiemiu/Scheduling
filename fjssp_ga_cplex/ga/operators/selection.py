from ..schedule import calculate_makespan


def select(population, machines, processing_times, num_selected):
    evaluated = sorted(
        ((calculate_makespan(ch, machines, processing_times), ch) for ch in population),
        key=lambda x: x[0],
    )
    return (
        [ch for _, ch in evaluated[:num_selected]],
        [ch for _, ch in evaluated[num_selected:]],
    )
