from collections import defaultdict


def fix_duplicates(chromosome, machines):
    required = {f"J{j+1}O{o}" for o, mlist in machines.items() for j in range(len(mlist))}
    cnt = defaultdict(int)
    for g in chromosome:
        cnt[g] += 1

    dup_pos = [i for i, g in enumerate(chromosome) if cnt[g] > 1]
    missing = list(required - set(chromosome))

    for i in dup_pos:
        if not missing:
            break
        g = chromosome[i]
        if cnt[g] > 1:
            chromosome[i] = missing.pop()
            cnt[g] -= 1

    return chromosome
