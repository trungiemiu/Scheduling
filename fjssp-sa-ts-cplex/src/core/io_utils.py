import pandas as pd
from typing import Any, Dict, List, Tuple
from .models import Machine, Job, Operation

def load_data_from_excel(file_path: str):
    xl = pd.ExcelFile(file_path)
    machine_caps: Dict[str, int] = {}
    if "Machines" in xl.sheet_names:
        mdf = xl.parse("Machines")
        mdf.columns = [str(c).strip() for c in mdf.columns]
        for _, r in mdf.iterrows():
            machine_caps[str(r["Machine Name"])] = int(r["Machine Capacity"])
    if "Jobs" not in xl.sheet_names:
        raise ValueError("Missing sheet 'Jobs'")
    df = xl.parse("Jobs")
    df.columns = [str(c).strip() for c in df.columns]
    req = ["Job Name", "Operation ID", "Machine Name", "Time Required", "Tools Needed", "Setup Time"]
    miss = [c for c in req if c not in df.columns]
    if miss:
        raise ValueError("Missing columns in Jobs: " + ", ".join(miss))
    df["Job Name"] = df["Job Name"].astype(str)
    df["Operation ID"] = df["Operation ID"].astype(int)
    df["Machine Name"] = df["Machine Name"].astype(str)
    df["Time Required"] = df["Time Required"].astype(float)
    df["Tools Needed"] = df["Tools Needed"].astype(int)
    df["Setup Time"] = df["Setup Time"].astype(float)
    machine_names = sorted(df["Machine Name"].unique().tolist())
    machines: List[Machine] = [Machine(m, int(machine_caps.get(m, 10))) for m in machine_names]
    for m, cap in machine_caps.items():
        if m not in machine_names:
            machines.append(Machine(m, int(cap)))
    jobs_dict: Dict[str, Dict[int, Operation]] = {}
    for _, r in df.iterrows():
        jn = r["Job Name"]
        oid = int(r["Operation ID"])
        mn = r["Machine Name"]
        t = float(r["Time Required"])
        w = int(r["Tools Needed"])
        s = float(r["Setup Time"])
        if jn not in jobs_dict:
            jobs_dict[jn] = {}
        if oid in jobs_dict[jn]:
            jobs_dict[jn][oid].tool_requirements[mn] = w
        else:
            jobs_dict[jn][oid] = Operation(jn, oid, t, {mn: w}, s)
    jobs: List[Job] = [
        Job(jn, [jobs_dict[jn][k] for k in sorted(jobs_dict[jn].keys())])
        for jn in sorted(jobs_dict.keys())
    ]
    return machines, jobs

GanttRow = Tuple[str, str, int, float, float, float]

def _to_gantt_rows(data: Any) -> List[GanttRow]:
    try:
        jobs, machines = data
        setup_of: Dict[Tuple[str, int], float] = {
            (op.job_name, int(op.operation_id)): float(op.setup_time)
            for j in jobs for op in j.operations
        }
        rows: List[GanttRow] = []
        for m in sorted(machines, key=lambda x: x.name):
            for fullname, start, end in sorted(m.operations, key=lambda t: t[1]):
                jname, _, op_s = fullname.partition("O")
                opid = int(op_s)
                ss = float(start)
                sp = ss + setup_of[(jname, opid)]
                rows.append((m.name, jname, opid, ss, sp, float(end)))
        return rows
    except Exception:
        return list(data)

def print_schedule(data: Any, return_lines: bool = False):
    rows = _to_gantt_rows(data)
    lines: List[str] = []
    machines = sorted({r[0] for r in rows})
    for mname in machines:
        lines.append(f"Machine {mname}:")
        mr = [r for r in rows if r[0] == mname]
        mr.sort(key=lambda r: r[3])
        for _, jname, opid, ss, sp, e in mr:
            lines.append(
                f"    - Job {jname} - Operation {opid}: "
                f"Start setup = {ss:.3f}, start = {sp:.3f}, end = {e:.3f}"
            )
    if return_lines:
        return lines
    for ln in lines:
        print(ln)
