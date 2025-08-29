import random


def divide_into_pairs(cross_list):
    cross_list = cross_list[:] 
    random.shuffle(cross_list)
    pairs = []
    odd_individual = None
    if len(cross_list) % 2 != 0:
        odd_individual = cross_list.pop()

    for i in range(0, len(cross_list), 2):
        pairs.append([cross_list[i], cross_list[i + 1]])

    return pairs, odd_individual
