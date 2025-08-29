from collections import defaultdict
from .gene import parse_gene

def get_operation_details(chromosome, machines, processing_times):
    job_times, machine_times = defaultdict(float), defaultdict(float)
    operation_details = []
    for gene in chromosome:
        try:
            j, o = parse_gene(gene)
            machine_id = machines[o][j - 1]
            start_time = max(job_times[f'J{j}'], machine_times[machine_id])
            duration = processing_times[o][j - 1]
            end_time = start_time + duration
            job_times[f'J{j}'] = end_time
            machine_times[machine_id] = end_time
            operation_details.append((gene, machine_id, start_time, end_time, duration))
        except Exception:
            continue
    return operation_details

def calculate_makespan(chromosome, machines, processing_times):
    operation_details = get_operation_details(chromosome, machines, processing_times)
    if not operation_details:
        return float('inf')
    return max(end for _, _, _, end, _ in operation_details)
