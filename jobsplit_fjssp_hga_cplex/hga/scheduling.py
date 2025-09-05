from typing import Dict, List, Tuple

Lookup = Dict[Tuple[int, int, int], float]

def _col(j: int, o: int, num_ops: int) -> int:
    return (j - 1) * num_ops + (o - 1)

def schedule(chromosome, lot_size: List[int], processing_lookup: Lookup,
             num_machine: int, num_operation: int):
    matrix_1 = chromosome["Matrix1"]
    matrix_2 = chromosome["Matrix2"]

    machine_end_times = [0.0] * num_machine
    job_operation_end_times: Dict[Tuple[int, int], float] = {}
    operation_details: List[dict] = []

    for (job, operation), machine in zip(matrix_2[0], matrix_2[1]):
        col = _col(job, operation, num_operation)
        sublot = float(matrix_1[machine - 1, col])
        if sublot <= 0:
            continue

        p_unit = processing_lookup.get((job, operation, machine))
        if p_unit is None:
            raise KeyError(f"Machine {machine} not eligible for job {job}, op {operation}")
        p_unit = float(p_unit)

        total_p = sublot * p_unit
        prev_end = job_operation_end_times.get((job, operation - 1), 0.0)
        m_avail = machine_end_times[machine - 1]
        start = max(prev_end, m_avail)
        end = start + total_p

        machine_end_times[machine - 1] = end
        job_operation_end_times[(job, operation)] = max(job_operation_end_times.get((job, operation), 0.0), end)

        operation_details.append({
            "J": job, "O": operation, "M": machine,
            "Sublot": sublot, "P": p_unit, "TotalP": total_p,
            "Start": start, "End": end
        })

    return operation_details, machine_end_times, job_operation_end_times


def calculate_makespan(chromosome, lot_size: List[int], processing_lookup: Lookup,
                       num_machine: int, num_operation: int):
    details, m_end, _ = schedule(chromosome, lot_size, processing_lookup, num_machine, num_operation)
    return (float(max(m_end)) if m_end else 0.0), details
