import math, copy, random
from typing import List, Tuple, Dict, Optional
from src.core.models import Job, Machine
from src.core.scheduler import schedule_operations, objective_makespan

def _neighbor(jobs: List[Job], machines: List[Machine], n_hints: int = 2):
    new_jobs = copy.deepcopy(jobs)
    new_machines = copy.deepcopy(machines)
    pool = []
    for j in new_jobs:
        for op in j.operations:
            elig = [m.name for m in new_machines if m.name in op.tool_requirements]
            if len(elig) >= 2:
                pool.append((j.job_name, op.operation_id, elig))
    if not pool:
        schedule_operations(new_jobs, new_machines)
        return new_jobs, new_machines
    k = min(max(1, n_hints), len(pool))
    chosen = random.sample(pool, k)
    hints: Dict[Tuple[str, int], str] = {(jn, oid): random.choice(elig) for jn, oid, elig in chosen}
    schedule_operations(new_jobs, new_machines, hints=hints)
    return new_jobs, new_machines

def simulated_annealing(
    jobs: List[Job],
    machines: List[Machine],
    initial_temp: float,
    cooling_rate: float,
    max_iter: int,
    n_hints_per_move: int = 2,
    seed: Optional[int] = None
):
    if seed is not None:
        random.seed(seed)
    current_jobs = copy.deepcopy(jobs)
    current_machines = copy.deepcopy(machines)
    schedule_operations(current_jobs, current_machines)
    current_obj = objective_makespan(current_machines)
    best_jobs = copy.deepcopy(current_jobs); best_machines = copy.deepcopy(current_machines); best_obj = current_obj
    T = float(initial_temp)
    history = [best_obj]
    for _ in range(max_iter):
        nj, nm = _neighbor(current_jobs, current_machines, n_hints=n_hints_per_move)
        obj = objective_makespan(nm)
        if obj < best_obj:
            best_jobs, best_machines, best_obj = copy.deepcopy(nj), copy.deepcopy(nm), obj
        delta = obj - current_obj
        if (delta < 0) or (random.random() < math.exp(-delta / max(T, 1e-9))):
            current_jobs, current_machines, current_obj = nj, nm, obj
        T = max(T * cooling_rate, 1e-9)
        history.append(best_obj)
    return best_jobs, best_machines, history
