import pandas as pd
from docplex.mp.model import Model
from typing import Dict, Tuple, List


def load_data_from_excel(file_path: str):
    xls = pd.ExcelFile(file_path)
    try:
        df_idx = pd.read_excel(xls, 'indices')
        if 'Unnamed: 0' in df_idx.columns and 'value' in df_idx.columns:
            idx_map = dict(zip(df_idx['Unnamed: 0'].astype(str), df_idx['value']))
            numJ = int(idx_map.get('numJ'))
            numO = int(idx_map.get('numO'))
            numM = int(idx_map.get('numM'))
        else:
            vals = df_idx.iloc[:3, 1].tolist()
            numJ, numO, numM = int(vals[0]), int(vals[1]), int(vals[2])
    except Exception as e:
        raise ValueError("Cannot read 'indices' sheet (numJ,numO,numM)") from e

    df_p = pd.read_excel(xls, 'P')
    required_p = {'j', 'o', 'P'}
    if not required_p.issubset(df_p.columns):
        raise ValueError("'P' sheet must contain columns: j, o, P")
    
    df_m = pd.read_excel(xls, 'M')
    required_m = {'j', 'o'}
    if not required_m.issubset(df_m.columns):
        raise ValueError("'M' sheet must contain columns: j, o, ... machine columns ...")
    
    J = list(range(1, numJ + 1))
    O = list(range(1, numO + 1))
    Mset = list(range(1, numM + 1))
    JOSet = [(j, o) for j in J for o in O]

    P = {}
    for j in J:
        for o in O:
            vals = df_p[(df_p['j'] == j) & (df_p['o'] == o)]['P'].values
            if len(vals) == 0:
                raise ValueError(f"Missing processing time for (j={j}, o={o}) in 'P' sheet")
            P[(j, o)] = float(vals[0])

    machine_cols = [c for c in df_m.columns if c not in ('j', 'o')]
    try:
        machine_ids = [int(str(c)) for c in machine_cols]
    except Exception:
        raise ValueError("Machine column headers in 'M' must be integers 1..numM")

    A = {}
    for _, r in df_m.iterrows():
        j = int(r['j']); o = int(r['o'])
        for col, m in zip(machine_cols, machine_ids):
            A[(j, o, m)] = int(r[col])

    return numJ, numO, numM, J, O, Mset, JOSet, P, A


def build_model(numJ: int, numO: int, numM: int,
                J: List[int], O: List[int], Mset: List[int], JOSet: List[Tuple[int,int]],
                P: Dict[Tuple[int,int], float], A: Dict[Tuple[int,int,int], int],
                bigM: float = 1e7):
    mdl = Model(name='FJSSP_MIP_from_OPL')

    S  = mdl.continuous_var_dict(JOSet, lb=0, name='S')
    C  = mdl.continuous_var_dict(JOSet, lb=0, name='C')
    Co = mdl.continuous_var_dict(J, lb=0, name='Co')
    Cmax = mdl.continuous_var(lb=0, name='Cmax')

    Z = {}
    for j in J:
        for o in O:
            for m in Mset:
                Z[(j,o,m)] = mdl.binary_var(name=f"Z_{j}_{o}_{m}")

    X = {}
    for i in J:
        for j in J:
            if i == j:
                continue
            for o in O:
                for m in Mset:
                    X[(i, j, o, m)] = mdl.binary_var(name=f"X_{i}_{j}_{o}_{m}")

    mdl.minimize(Cmax)

    for (j, o) in JOSet:
        mdl.add_constraint(C[(j, o)] == S[(j, o)] + P[(j, o)], ctname=f"comp_time_{j}_{o}")

    for j in J:
        mdl.add_constraint(Co[j] >= C[(j, numO)], ctname=f"job_completion_{j}")
        mdl.add_constraint(Cmax >= Co[j], ctname=f"makespan_ge_{j}")

    for j in J:
        for o in O:
            if o < numO:
                mdl.add_constraint(C[(j, o)] <= S[(j, o + 1)], ctname=f"precedence_{j}_{o}")

    for (j, o) in JOSet:
        mdl.add_constraint(
            mdl.sum(Z[(j,o,m)] for m in Mset if A[(j,o,m)] == 1) == 1,
            ctname=f"assign_one_{j}_{o}"
        )
        for m in Mset:
            mdl.add_constraint(Z[(j,o,m)] <= A[(j,o,m)], ctname=f"elig_{j}_{o}_{m}")

    for i in J:
        for j in J:
            if i == j:
                continue
            for o in O:
                for m in Mset:
                    mdl.add_constraint(X[(i,j,o,m)] <= Z[(i,o,m)], ctname=f"linkZ1_{i}_{j}_{o}_{m}")
                    mdl.add_constraint(X[(i,j,o,m)] <= Z[(j,o,m)], ctname=f"linkZ2_{i}_{j}_{o}_{m}")
                    mdl.add_constraint(X[(i, j, o, m)] + X[(j, i, o, m)] <= 1, ctname=f"antisym_{i}_{j}_{o}_{m}")
                    mdl.add_constraint(S[(j, o)] >= C[(i, o)] - bigM * (1 - X[(i, j, o, m)]), ctname=f"noovl1_{i}_{j}_{o}_{m}")
                    mdl.add_constraint(S[(i, o)] >= C[(j, o)] - bigM * (1 - X[(j, i, o, m)]), ctname=f"noovl2_{i}_{j}_{o}_{m}")

    return mdl, S, C, Co, Cmax, X, Z


def _to_ga_formats(numJ, numO, J, O, Mset, P, Zvals, Svals):
    machines_chosen = {o: [None]*len(J) for o in O}
    for j in J:
        for o in O:
            chosen_m = None
            for m in Mset:
                if Zvals.get((j,o,m), 0) > 0.5:
                    chosen_m = m
                    break
            if chosen_m is None:
                chosen_m = next((m for m in Mset if Zvals.get((j,o,m), 0) > 0.1), 1)
            machines_chosen[o][j-1] = chosen_m

    processing_times_ga = {o: [P[(j,o)] for j in J] for o in O}

    per_machine = {m: [] for m in Mset}
    for j in J:
        for o in O:
            m = machines_chosen[o][j-1]
            s = Svals[(j,o)]
            per_machine[m].append((s, f"J{j}O{o}"))
    chromosome = []
    for m in sorted(Mset):
        seq = [g for _, g in sorted(per_machine[m], key=lambda x: x[0])]
        chromosome.extend(seq)

    return machines_chosen, processing_times_ga, chromosome


def solve_and_extract(mdl: Model, S, C, Co, Cmax, X, Z):
    sol = mdl.solve(log_output=True)
    if sol is None:
        raise RuntimeError("No feasible solution found.")

    Svals = {k: sol.get_value(v) for k, v in S.items()}
    Cvals = {k: sol.get_value(v) for k, v in C.items()}
    Zvals = {k: sol.get_value(v) for k, v in Z.items()}

    result = {
        'Cmax': sol.get_value(Cmax),
        'Co': {j: sol.get_value(var) for j, var in Co.items()},
        'S': Svals,
        'C': Cvals,
        'X1': {k: sol.get_value(v) for k, v in X.items() if sol.get_value(v) > 0.5},
        'Z1': {k: v for k, v in Zvals.items() if v > 0.5},
    }
    return result


def solve_from_excel(file_path: str, bigM: float = 1e7):
    numJ, numO, numM, J, O, Mset, JOSet, P, A = load_data_from_excel(file_path)
    mdl, S, C, Co, Cmax, X, Z = build_model(numJ, numO, numM, J, O, Mset, JOSet, P, A, bigM=bigM)
    res = solve_and_extract(mdl, S, C, Co, Cmax, X, Z)

    machines_chosen, processing_times_ga, chromosome = _to_ga_formats(
        numJ, numO, J, O, Mset, P, res['Z1'], res['S']
    )
    res['machines_chosen_ga'] = machines_chosen
    res['processing_times_ga'] = processing_times_ga
    res['chromosome_ga'] = chromosome
    return res
