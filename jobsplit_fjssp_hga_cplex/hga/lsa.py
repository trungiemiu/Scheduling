import random
from .encoding import convert_matrix_1_to_matrix_2
from .scheduling import calculate_makespan

def _eligible_machines(job, op, num_machine, processing_lookup):
    return [m for m in range(1, num_machine + 1) if (job, op, m) in processing_lookup]

def split_job(chromosome, lot_size, processing_lookup, num_machine, num_operation, j_index, op_index, s):
    m1 = chromosome["Matrix1"]
    alpha = m1[:, j_index * num_operation + op_index]
    total = lot_size[j_index]
    assigned = [i for i, v in enumerate(alpha) if v > 0]
    job = j_index + 1
    op = op_index + 1
    eligible = _eligible_machines(job, op, num_machine, processing_lookup)

    if len(assigned) == 1 and alpha[assigned[0]] == total and total >= s:
        cur = assigned[0]
        candidates = [m - 1 for m in eligible if (m - 1) != cur]
        if not candidates:
            return chromosome
        tgt = random.choice(candidates)
        new_m1 = m1.copy()
        new_alpha = new_m1[:, j_index * num_operation + op_index]
        new_alpha[cur] -= s
        new_alpha[tgt] += s
        new_m1[:, j_index * num_operation + op_index] = new_alpha
        new_m2 = convert_matrix_1_to_matrix_2(new_m1, len(lot_size), num_operation)
        return {"Matrix1": new_m1, "Matrix2": new_m2}
    return chromosome


def decrease_sublot(chromosome, lot_size, processing_lookup, num_machine, num_operation, j, o, s, beta):
    m1 = chromosome["Matrix1"]
    alpha = m1[:, j * num_operation + o].copy()
    total = lot_size[j]
    improved_flag = 0
    base, _ = calculate_makespan(chromosome, lot_size, processing_lookup, num_machine, num_operation)

    for m in range(num_machine):
        while s + beta <= alpha[m] <= total - s:
            new_m1 = m1.copy()
            new_alpha = new_m1[:, j * num_operation + o]
            new_alpha[m] -= beta
            targets = [i for i in range(num_machine) if i != m and alpha[i] > 0]
            moved = False
            for t in targets:
                new_alpha[t] += beta
                new_m1[:, j * num_operation + o] = new_alpha
                new_m2 = convert_matrix_1_to_matrix_2(new_m1, len(lot_size), num_operation)
                cand = {"Matrix1": new_m1, "Matrix2": new_m2}
                mk, _ = calculate_makespan(cand, lot_size, processing_lookup, num_machine, num_operation)
                if mk < base:
                    chromosome = cand
                    base = mk
                    alpha = new_alpha.copy()
                    improved_flag = 1
                    moved = True
                    break
                new_alpha[t] -= beta
            if not moved:
                break
    return chromosome, improved_flag


def increase_sublot(chromosome, lot_size, processing_lookup, num_machine, num_operation, j, o, s, beta, c):
    m1 = chromosome["Matrix1"]
    alpha = m1[:, j * num_operation + o].copy()
    total = lot_size[j]
    base, _ = calculate_makespan(chromosome, lot_size, processing_lookup, num_machine, num_operation)

    for m in range(num_machine):
        while s <= alpha[m] <= total - s - beta:
            new_m1 = m1.copy()
            new_alpha = new_m1[:, j * num_operation + o]
            new_alpha[m] += beta
            targets = [t for t in range(num_machine) if t != m and new_alpha[t] >= beta]
            moved = False
            for t in targets:
                new_alpha[t] -= beta
                new_m1[:, j * num_operation + o] = new_alpha
                new_m2 = convert_matrix_1_to_matrix_2(new_m1, len(lot_size), num_operation)
                cand = {"Matrix1": new_m1, "Matrix2": new_m2}
                mk, _ = calculate_makespan(cand, lot_size, processing_lookup, num_machine, num_operation)
                if mk < base:
                    chromosome = cand
                    base = mk
                    alpha = new_alpha.copy()
                    moved = True
                    break
                new_alpha[t] += beta
            if not moved:
                break
    return chromosome, c


def merge_jobs(chromosome, lot_size, processing_lookup, num_machine, num_operation, j, o):
    m1 = chromosome["Matrix1"]
    total = lot_size[j]
    job = j + 1
    op = o + 1
    eligible = _eligible_machines(job, op, num_machine, processing_lookup)
    best = chromosome
    best_mk, _ = calculate_makespan(best, lot_size, processing_lookup, num_machine, num_operation)
    for m in eligible:
        new_m1 = m1.copy()
        col = j * num_operation + o
        new_m1[:, col] = 0
        new_m1[m - 1, col] = total
        new_m2 = convert_matrix_1_to_matrix_2(new_m1, len(lot_size), num_operation)
        cand = {"Matrix1": new_m1, "Matrix2": new_m2}
        mk, _ = calculate_makespan(cand, lot_size, processing_lookup, num_machine, num_operation)
        if mk < best_mk:
            best, best_mk = cand, mk
    return best


def lsa_chromosome(chromosome, lot_size, processing_lookup, num_machine, num_operation, s, beta):
    current = chromosome
    base, _ = calculate_makespan(current, lot_size, processing_lookup, num_machine, num_operation)
    for j in range(len(lot_size)):
        for o in range(num_operation):
            cand = split_job(current, lot_size, processing_lookup, num_machine, num_operation, j, o, s)
            mk, _ = calculate_makespan(cand, lot_size, processing_lookup, num_machine, num_operation)
            if mk < base:
                current, base = cand, mk

            improved = True
            cflag = 0
            while improved:
                newc, cflag = decrease_sublot(current, lot_size, processing_lookup, num_machine, num_operation, j, o, s, beta)
                mk, _ = calculate_makespan(newc, lot_size, processing_lookup, num_machine, num_operation)
                improved = mk < base
                if improved:
                    current, base = newc, mk

            improved = True
            while improved:
                newc, _ = increase_sublot(current, lot_size, processing_lookup, num_machine, num_operation, j, o, s, beta, cflag)
                mk, _ = calculate_makespan(newc, lot_size, processing_lookup, num_machine, num_operation)
                improved = mk < base
                if improved:
                    current, base = newc, mk

    for j in range(len(lot_size)):
        for o in range(num_operation):
            newc = merge_jobs(current, lot_size, processing_lookup, num_machine, num_operation, j, o)
            mk, _ = calculate_makespan(newc, lot_size, processing_lookup, num_machine, num_operation)
            if mk < base:
                current, base = newc, mk

    return current
