import numpy as np
from typing import Dict, Tuple, List

Lookup = Dict[Tuple[int,int,int], float]

def convert_matrix_1_to_matrix_2(matrix_1, num_job, num_operation):
    matrix_2 = [[], []]
    for j_index in range(num_job):
        for op_index in range(num_operation):
            col = j_index * num_operation + op_index
            for machine_index in range(matrix_1.shape[0]):
                sub = matrix_1[machine_index, col]
                if sub > 0:
                    matrix_2[0].append((j_index + 1, op_index + 1))
                    matrix_2[1].append(machine_index + 1)
    assert len(matrix_2[0]) == len(matrix_2[1]), "Matrix2 length mismatch"
    return matrix_2


def _eligible_machines_for(job: int, op: int, num_machine: int, processing_lookup: Lookup) -> List[int]:
    eligible = [m for m in range(1, num_machine + 1) if (job, op, m) in processing_lookup]
    return eligible


def create_chromosome(
    num_job: int,
    num_operation: int,
    lot_sizes: List[int],
    num_machine: int,
    s: int = 1,
    processing_lookup: Lookup = None
):
    step = max(1, int(s))
    matrix_1 = np.zeros((num_machine, num_job * num_operation), dtype=float)
    for j_index in range(num_job):
        for op_index in range(num_operation):
            job = j_index + 1
            op = op_index + 1
            lot_size = int(lot_sizes[j_index])
            remaining = lot_size
            if processing_lookup is None:
                eligible = list(range(1, num_machine + 1))
            else:
                eligible = _eligible_machines_for(job, op, num_machine, processing_lookup)
            if not eligible:
                raise ValueError(f"No eligible machine for (J{job}, O{op}). Check ProcessingTime sheet.")
            for idx, m in enumerate(eligible):
                if idx == len(eligible) - 1:
                    assigned = remaining
                else:
                    max_assign = (remaining // step) * step
                    assigned = 0
                    if max_assign > 0:
                        assigned = np.random.randint(0, (max_assign // step) + 1) * step
                matrix_1[m - 1, j_index * num_operation + op_index] += assigned
                remaining -= assigned

            if remaining != 0:
                matrix_1[eligible[-1] - 1, j_index * num_operation + op_index] += remaining
                remaining = 0

    matrix_2 = convert_matrix_1_to_matrix_2(matrix_1, num_job, num_operation)
    for j_index in range(num_job):
        for op_index in range(num_operation):
            col = j_index * num_operation + op_index
            total = float(np.sum(matrix_1[:, col]))
            assert total == lot_sizes[j_index], (
                f"Total sub-lot for J{j_index+1},O{op_index+1} = {total}, expected {lot_sizes[j_index]}"
            )

    return {"Matrix1": matrix_1, "Matrix2": matrix_2}


def is_duplicate_chromosome(new_chromosome, population):
    for c in population:
        if np.array_equal(new_chromosome["Matrix1"], c["Matrix1"]) and new_chromosome["Matrix2"] == c["Matrix2"]:
            return True
    return False
