import numpy as np
from .encoding import convert_matrix_1_to_matrix_2

def crossover(parent1, parent2, num_job, num_operation):
    m1_a = parent1["Matrix1"]
    m1_b = parent2["Matrix1"]
    ncols = m1_a.shape[1]
    cp = np.random.randint(1, ncols)

    c1_m1 = np.hstack([m1_a[:, :cp], m1_b[:, cp:]])
    c2_m1 = np.hstack([m1_b[:, :cp], m1_a[:, cp:]])

    c1_m2 = convert_matrix_1_to_matrix_2(c1_m1, num_job, num_operation)
    c2_m2 = convert_matrix_1_to_matrix_2(c2_m1, num_job, num_operation)

    return {"Matrix1": c1_m1, "Matrix2": c1_m2}, {"Matrix1": c2_m1, "Matrix2": c2_m2}
