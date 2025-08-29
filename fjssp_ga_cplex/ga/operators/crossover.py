import random
from ..schedule import calculate_makespan
from .repair import fix_duplicates


def pair_crossover(cross_pair, machines, processing_times):
    p1, p2 = cross_pair
    n = len(p1)
    if n <= 2:
        point = 1
    else:
        point = random.randint(1, n - 1)

    c1 = fix_duplicates(p1[:point] + p2[point:], machines)
    c2 = fix_duplicates(p2[:point] + p1[point:], machines)

    candidates = [p1, p2, c1, c2]
    scored = sorted(
        ((calculate_makespan(ch, machines, processing_times), tuple(ch)) for ch in candidates),
        key=lambda x: x[0]
    )
    best = [list(scored[0][1])]
    for _, chrom in scored[1:]:
        if tuple(chrom) != tuple(best[0]):
            best.append(list(chrom))
            break
    if len(best) == 1: 
        best.append(list(best[0]))

    return best
