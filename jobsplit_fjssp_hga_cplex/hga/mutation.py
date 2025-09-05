import numpy as np
import random
from .encoding import convert_matrix_1_to_matrix_2
from .lsa import lsa_chromosome

def inversion_chromosome(chromosome):
    job_row = chromosome["Matrix2"][0]
    machine_row = chromosome["Matrix2"][1]
    new_job_row = job_row.copy()
    new_machine_row = machine_row.copy()

    if len(new_job_row) > 1:
        i, j = sorted(np.random.choice(len(new_job_row), 2, replace=False))
        new_job_row[i:j + 1] = reversed(new_job_row[i:j + 1])
        new_machine_row[i:j + 1] = reversed(new_machine_row[i:j + 1])
        changed = True
        while changed:
            changed = False
            for idx in range(len(new_job_row) - 1):
                (j1, o1), (j2, o2) = new_job_row[idx], new_job_row[idx + 1]
                if j1 == j2 and o2 < o1:
                    new_job_row[idx], new_job_row[idx + 1] = new_job_row[idx + 1], new_job_row[idx]
                    new_machine_row[idx], new_machine_row[idx + 1] = new_machine_row[idx + 1], new_machine_row[idx]
                    changed = True

    return {"Matrix1": chromosome["Matrix1"], "Matrix2": [new_job_row, new_machine_row]}


def swap_chromosome(chromosome):
    job_row = chromosome["Matrix2"][0]
    machine_row = chromosome["Matrix2"][1]
    new_job_row = job_row.copy()
    new_machine_row = machine_row.copy()

    if len(new_job_row) > 1:
        i, j = np.random.choice(len(new_job_row), 2, replace=False)
        new_job_row[i], new_job_row[j] = new_job_row[j], new_job_row[i]
        new_machine_row[i], new_machine_row[j] = new_machine_row[j], new_machine_row[i]
        changed = True
        while changed:
            changed = False
            for idx in range(len(new_job_row) - 1):
                (j1, o1), (j2, o2) = new_job_row[idx], new_job_row[idx + 1]
                if j1 == j2 and o2 < o1:
                    new_job_row[idx], new_job_row[idx + 1] = new_job_row[idx + 1], new_job_row[idx]
                    new_machine_row[idx], new_machine_row[idx + 1] = new_machine_row[idx + 1], new_machine_row[idx]
                    changed = True

    return {"Matrix1": chromosome["Matrix1"], "Matrix2": [new_job_row, new_machine_row]}


def mutation1(chromosome, num_job, num_operation, s: int):
    step = max(1, int(s))
    matrix1 = chromosome["Matrix1"]
    new_matrix1 = matrix1.copy()
    j_index = np.random.randint(0, num_job)
    o_index = np.random.randint(0, num_operation)
    col = j_index * num_operation + o_index
    assigned = np.where(new_matrix1[:, col] > 0)[0]
    if len(assigned) > 1:
        m1, m2 = np.random.choice(assigned, 2, replace=False)
        max_transfer = int(new_matrix1[m1, col])
        max_transfer = (max_transfer // step) * step
        if max_transfer > 0:
            k = np.random.randint(1, (max_transfer // step) + 1)
            transfer = k * step
            new_matrix1[m1, col] -= transfer
            new_matrix1[m2, col] += transfer
            new_matrix2 = convert_matrix_1_to_matrix_2(new_matrix1, num_job, num_operation)
            return {"Matrix1": new_matrix1, "Matrix2": new_matrix2}
    return chromosome


def mutation(chromosome, lot_size, processing_lookup, num_machine, num_operation, s, beta):
    if random.random() > 0.5:
        new_c = mutation1(chromosome, len(lot_size), num_operation, s)
        return swap_chromosome(new_c) if random.random() < 0.5 else inversion_chromosome(new_c)
    else:
        return lsa_chromosome(chromosome, lot_size, processing_lookup, num_machine, num_operation, s, beta)
