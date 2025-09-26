import copy
from typing import List
from src.core.models import Job, Machine
from src.core.scheduler import schedule_operations, objective_makespan

def tabu_search(jobs: List[Job], machines: List[Machine], max_iterations: int, tabu_tenure: int):
    best_jobs = copy.deepcopy(jobs); best_machines = copy.deepcopy(machines)
    schedule_operations(best_jobs, best_machines)
    best_obj = objective_makespan(best_machines)
    current_jobs = copy.deepcopy(best_jobs); current_machines = copy.deepcopy(best_machines)
    current_obj = best_obj
    tabu = []
    history = [best_obj]
    for _ in range(max_iterations):
        schedule_operations(current_jobs, current_machines)
        neighbors = []
        for m_idx, m in enumerate(current_machines):
            if len(m.operations) > 1:
                for i in range(len(m.operations)-1):
                    nj = copy.deepcopy(current_jobs); nm = copy.deepcopy(current_machines)
                    nm[m_idx].operations[i], nm[m_idx].operations[i+1] = nm[m_idx].operations[i+1], nm[m_idx].operations[i]
                    schedule_operations(nj, nm)
                    neighbors.append((nj, nm, (m_idx, i, i+1)))
        if not neighbors:
            history.append(best_obj); continue
        bestN = None; bestNobj = float('inf')
        for nj, nm, mv in neighbors:
            obj = objective_makespan(nm)
            if mv not in tabu or obj < best_obj:
                if obj < bestNobj:
                    bestN, bestNobj = (nj, nm, mv), obj
        if bestN is None:
            history.append(best_obj); continue
        current_jobs, current_machines, mv = bestN
        current_obj = bestNobj
        tabu.append(mv)
        if len(tabu) > tabu_tenure:
            tabu.pop(0)
        if current_obj < best_obj:
            best_jobs, best_machines, best_obj = copy.deepcopy(current_jobs), copy.deepcopy(current_machines), current_obj
        history.append(best_obj)
    return best_jobs, best_machines, history
