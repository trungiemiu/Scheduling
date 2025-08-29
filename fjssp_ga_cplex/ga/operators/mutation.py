import random
from collections import defaultdict
from ..schedule import calculate_makespan
from ..gene import parse_gene


def _positions_by_machine(chromosome, machines):
    pos_by_machine = defaultdict(list)
    for idx, gene in enumerate(chromosome):
        try:
            j, o = parse_gene(gene)
            m_id = machines[o][j - 1]
            pos_by_machine[m_id].append(idx)
        except Exception:
            continue
    return {m: idxs for m, idxs in pos_by_machine.items() if len(idxs) >= 2}


def individual_mutate(chromosome, machines, processing_times):
    shared = _positions_by_machine(chromosome, machines)
    if not shared:
        return chromosome

    m = random.choice(list(shared.keys()))
    idx1, idx2 = random.sample(shared[m], 2)

    parent = chromosome[:]
    child = parent[:]
    child[idx1], child[idx2] = child[idx2], child[idx1]

    return (
        child
        if calculate_makespan(child, machines, processing_times)
        < calculate_makespan(parent, machines, processing_times)
        else parent
    )


def mutate(mutation_list, machines, processing_times):
    return [
        individual_mutate(ch, machines, processing_times)
        for ch in mutation_list
    ]
