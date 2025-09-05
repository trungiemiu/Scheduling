import numpy as np
from .scheduling import calculate_makespan

def binary_selection(population, lot_size, processing_lookup, num_machine, num_operation):
    selected = []
    while len(selected) < 2:
        if len(population) > 2:
            i1, i2 = np.random.choice(len(population), 2, replace=False)
            c1, c2 = population[i1], population[i2]
            mk1, _ = calculate_makespan(c1, lot_size, processing_lookup, num_machine, num_operation)
            mk2, _ = calculate_makespan(c2, lot_size, processing_lookup, num_machine, num_operation)
            selected.append(c1 if mk1 < mk2 else c2)
        else:
            selected.append(population[np.random.randint(0, len(population))])
    return selected
