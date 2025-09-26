from __future__ import annotations
import random, sys
from typing import Dict, Iterable, List, Optional, TextIO, Tuple
from .models import Job, Machine, Operation

OperationKey = Tuple[str, int]
__all__ = ["schedule_operations", "objective_makespan",
           "collect_machine_sequences", "print_machine_schedules"]

# ---------- small utils ----------
def _split_op(fullname: str) -> Tuple[Optional[str], Optional[int]]:
    if "O" not in fullname: return None, None
    j, _, s = fullname.partition("O")
    try: return j, int(s)
    except ValueError: return j, None

def _fmt_op(j: str, oid: int) -> str: return f"{j}O{int(oid)}"

def objective_makespan(machines: Iterable[Machine]) -> float:
    return max((m.next_available_time() for m in machines), default=0.0)

def collect_machine_sequences(machines: Iterable[Machine]) -> Dict[str, List[OperationKey]]:
    seq: Dict[str, List[OperationKey]] = {}
    for m in machines:
        ops = [(_split_op(n)[0], _split_op(n)[1]) for (n, *_ ) in m.operations]
        ops = [(j, o) for (j, o) in ops if j is not None and o is not None]
        if ops: seq[m.name] = ops
    return seq

def _candidates(op: Operation, machines: Iterable[Machine], ready: float) -> List[Tuple[Machine, float]]:
    total = op.setup_time + op.time_required
    out: List[Tuple[Machine, float]] = []
    for m in machines:
        tools = op.tool_requirements.get(m.name)
        if tools is None: continue
        start = max(ready, m.next_available_time())
        if m.can_allocate(tools, start, total): out.append((m, start))
    return out

def _peek_pref(msq: Dict[str, List[OperationKey]], key: OperationKey) -> Optional[str]:
    for m, seq in msq.items():
        if seq and seq[0] == key: return m
    return None

def _consume(msq: Dict[str, List[OperationKey]], m: str, key: OperationKey) -> None:
    if msq.get(m) and msq[m][0] == key: msq[m].pop(0)

def schedule_operations(
    jobs: List[Job],
    machines: List[Machine],
    hints: Optional[Dict[OperationKey, str]] = None,
    use_machine_sequences: bool = True,
    randomize: bool = True,
) -> List[OperationKey]:
    hints = {(j, int(o)): m for (j, o), m in (hints or {}).items()}
    msq = collect_machine_sequences(machines) if use_machine_sequences else {}
    for m in machines: m.clear()
    ready = {j.job_name: 0.0 for j in jobs}
    unscheduled: List[OperationKey] = []
    max_ops = max((len(j.operations) for j in jobs), default=0)
    for k in range(max_ops):
        for j in jobs:
            op = j.get_operation(k)
            if op is None: continue
            key: OperationKey = (j.job_name, op.operation_id)

            pref = hints.get(key) or _peek_pref(msq, key)
            cand = _candidates(op, machines, ready[j.job_name])
            if pref:
                cand = [c for c in cand if c[0].name == pref] or cand
            if not cand:
                unscheduled.append(key); continue

            sel = (random.choice(cand) if (randomize and not pref and len(cand) > 1)
                   else min(cand, key=lambda t: (t[1], t[0].name)))
            m, start = sel
            total = op.setup_time + op.time_required
            tools = op.tool_requirements.get(m.name)
            if not m.allocate(tools, start, total):
                placed = False
                for mm, st in sorted(cand, key=lambda t: (t[1], t[0].name)):
                    tt = op.tool_requirements.get(mm.name)
                    if mm.allocate(tt, st, total):
                        m, start, tools, placed = mm, st, tt, True; break
                if not placed: unscheduled.append(key); continue

            end = start + total
            m.add_operation_bar(_fmt_op(j.job_name, op.operation_id), start, end)
            ready[j.job_name] = end
            _consume(msq, m.name, key)

    return unscheduled
