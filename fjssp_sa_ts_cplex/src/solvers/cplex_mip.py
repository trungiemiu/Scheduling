from __future__ import annotations
from typing import Dict, Tuple, List
from docplex.mp.model import Model
from src.core.io_utils import load_data_from_excel


def _build_sets_like_opl(data_path: str):
    machines, jobs = load_data_from_excel(data_path)
    J_names = [j.job_name for j in sorted(jobs, key=lambda x: x.job_name)]
    M_names = [m.name for m in sorted(machines, key=lambda x: x.name)]
    mapJ = {jn: i + 1 for i, jn in enumerate(J_names)}
    mapM = {mn: i + 1 for i, mn in enumerate(M_names)}
    WF: Dict[int, int] = {mapM[m.name]: int(m.capacity) for m in machines}
    job_to_opids: Dict[int, List[int]] = {}
    for j in jobs:
        jidx = mapJ[j.job_name]
        job_to_opids[jidx] = sorted(int(op.operation_id) for op in j.operations)

    JO: List[Tuple[int, int]] = []
    for jidx, op_ids in sorted(job_to_opids.items()):
        for o in range(1, len(op_ids) + 1):
            JO.append((jidx, o))

    op_by_jo: Dict[Tuple[int, int], object] = {}
    for j in jobs:
        jidx = mapJ[j.job_name]
        pos_to_id = {pos + 1: oid for pos, oid in enumerate(job_to_opids[jidx])}
        for op in j.operations:
            for pos, oid in pos_to_id.items():
                if int(op.operation_id) == oid:
                    op_by_jo[(jidx, pos)] = op
                    break

    p: Dict[Tuple[int, int], float] = {}
    setup: Dict[Tuple[int, int], float] = {}
    w: Dict[Tuple[int, int], Dict[int, int]] = {i: {} for i in JO}
    for i in JO:
        op = op_by_jo[i]
        p[i] = float(op.time_required)
        setup[i] = float(op.setup_time)
        for mn, tools in op.tool_requirements.items():
            w[i][mapM[mn]] = int(tools)

    numO: Dict[int, int] = {j: len(ids) for j, ids in job_to_opids.items()}
    return J_names, M_names, JO, numO, p, setup, w, WF, mapJ, mapM


def solve_cplex_mip(
    data_path: str,
    timelimit_sec: float = 150.0,
    mipgap: float = 0.2,
    display_log: bool = True,
):
    J_names, M_names, JO, numO, p, setup, w, WF, mapJ, mapM = _build_sets_like_opl(data_path)
    mdl = Model(name="fjssp_opl_style", log_output=display_log)
    begin = mdl.continuous_var_dict(JO, lb=0, name="begin")
    end   = mdl.continuous_var_dict(JO, lb=0, name="end")
    Cmax  = mdl.continuous_var(lb=0, name="Cmax")

    X = {}
    for i in JO:
        for m in mapM.values():
            if m in w[i]: 
                X[(i, m)] = mdl.binary_var(name=f"X_{i[0]}_{i[1]}_{m}")

    Z = {}
    for m in mapM.values():
        elig = [i for i in JO if m in w[i]]
        for idx1 in range(len(elig)):
            for idx2 in range(idx1 + 1, len(elig)):
                i1 = elig[idx1]; i2 = elig[idx2]
                Z[(i1, i2, m)] = mdl.binary_var(name=f"Z_{i1[0]}_{i1[1]}_{i2[0]}_{i2[1]}_{m}")

    A    = mdl.integer_var_dict(mapM.values(), lb=0, name="A")
    ptm  = mdl.continuous_var_dict(mapM.values(), lb=0, name="ptm")
    numP = mdl.integer_var_dict(mapM.values(), lb=0, name="numP")

    mdl.minimize(Cmax)
    for i in JO:
        mdl.add(mdl.sum(X[(i, m)] for m in mapM.values() if (i, m) in X) == 1)
    for i in JO:
        mdl.add(Cmax >= end[i])
    for i in JO:
        mdl.add(end[i] == begin[i] + setup[i] + mdl.sum(X[(i, m)] * p[i] for m in mapM.values() if (i, m) in X))

    for j in sorted(numO.keys()):
        k = numO[j]
        for o1 in range(1, k):
            for o2 in range(o1 + 1, k + 1):
                mdl.add(begin[(j, o2)] >= end[(j, o1)])

    for m in mapM.values():
        mdl.add(ptm[m]  == mdl.sum(X[(i, m)] * p[i] for i in JO if (i, m) in X))
        mdl.add(numP[m] == mdl.sum(X[(i, m)] for i in JO if (i, m) in X))
        mdl.add(A[m]    == mdl.sum(X[(i, m)] * w[i][m] for i in JO if (i, m) in X))
        mdl.add(A[m]    <= WF[m])

    BIGM = 10**6
    for m in mapM.values():
        elig = [i for i in JO if (i, m) in X]
        for idx1 in range(len(elig)):
            for idx2 in range(idx1 + 1, len(elig)):
                i1 = elig[idx1]; i2 = elig[idx2]
                z = Z[(i1, i2, m)]
                mdl.add(end[i1] <= begin[i2] + BIGM * (3 - X[(i1, m)] - X[(i2, m)] - z))
                mdl.add(end[i2] <= begin[i1] + BIGM * (2 - X[(i1, m)] - X[(i2, m)] + z))
                mdl.add(z <= X[(i1, m)])
                mdl.add(z <= X[(i2, m)])

    if timelimit_sec is not None:
        mdl.parameters.timelimit = float(timelimit_sec)
    if mipgap is not None:
        mdl.parameters.mip.tolerances.mipgap = float(mipgap)

    sol = mdl.solve(log_output=display_log)
    if not sol:
        raise RuntimeError("No feasible solution found by CPLEX.")

    chosen_m: Dict[Tuple[int, int], int] = {}
    for i in JO:
        for m in mapM.values():
            if (i, m) in X and sol.get_value(X[(i, m)]) > 0.5:
                chosen_m[i] = m
                break

    sched_per_m: Dict[int, List[Tuple[Tuple[int, int], float, float]]] = {m: [] for m in mapM.values()}
    for i in JO:
        bi = sol.get_value(begin[i]); ei = sol.get_value(end[i])
        m = chosen_m[i]
        sched_per_m[m].append((i, bi, ei))
    for m in sched_per_m:
        sched_per_m[m].sort(key=lambda t: t[1])

    lines: List[str] = []
    gantt: List[Tuple[str, str, int, float, float, float]] = []
    for m in sorted(sched_per_m.keys()):
        mname = M_names[m - 1]
        lines.append(f"Machine {m} ({mname}):")
        for (j, o), bi, ei in sched_per_m[m]:
            su = setup[(j, o)]
            jname = J_names[j - 1]
            start_setup = bi
            start_proc = bi + su
            lines.append(
                f"    - Job {jname} - Operation {o}: "
                f"Start setup = {start_setup:.3f}, start = {start_proc:.3f}, end = {ei:.3f}"
            )
            gantt.append((mname, jname, o, start_setup, start_proc, ei))

    return {"Cmax": sol.get_value(Cmax), "lines": lines, "gantt": gantt}
