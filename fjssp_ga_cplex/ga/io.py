import re
import pandas as pd
from collections import defaultdict

def read_parameters_from_excel(file_path: str):
    xls = pd.ExcelFile(file_path)
    df_p = pd.read_excel(xls, 'P')
    required_cols_p = {'j', 'o', 'P'}
    if not required_cols_p.issubset(set(df_p.columns)):
        raise ValueError(f"'P' sheet must contain columns: {required_cols_p}")

    num_jobs = int(df_p['j'].max())
    num_ops  = int(df_p['o'].max())

    processing_times = {}
    for o in range(1, num_ops + 1):
        row_list = []
        for j in range(1, num_jobs + 1):
            vals = df_p[(df_p['j'] == j) & (df_p['o'] == o)]['P'].values
            if len(vals) == 0:
                raise ValueError(f"Missing processing time for (j={j}, o={o})")
            row_list.append(float(vals[0]))
        processing_times[o] = row_list

    df_m = pd.read_excel(xls, 'M')
    required_cols_m = {'j', 'o'}
    if not required_cols_m.issubset(set(df_m.columns)):
        raise ValueError(f"'M' sheet must contain columns: {required_cols_m}")

    machine_cols = [c for c in df_m.columns if c not in ('j', 'o')]

    norm_machine_ids = []
    for c in machine_cols:
        try:
            norm_machine_ids.append(int(c))
        except Exception:
            digits = re.findall(r"\d+", str(c))
            if not digits:
                raise ValueError(f"Cannot parse machine id from column '{c}'")
            norm_machine_ids.append(int(digits[-1]))

    machines = {o: [None] * num_jobs for o in range(1, num_ops + 1)}
    for _, r in df_m.iterrows():
        j = int(r['j']); o = int(r['o'])
        assigned = None
        for col_name, mid in zip(machine_cols, norm_machine_ids):
            try:
                is_one = int(r[col_name]) == 1
            except Exception:
                is_one = False
            if is_one:
                assigned = mid
                break
        if assigned is None:
            raise ValueError(f"No machine assigned for (j={j}, o={o}) in 'M' sheet")
        machines[o][j - 1] = assigned

    def build_order(machines_dict):
        machine_count = defaultdict(int)
        for op in sorted(machines_dict.keys()):
            for m in machines_dict[op]:
                machine_count[m] += 1
        order = []
        for m, count in machine_count.items():
            order.extend([m] * count)
        return order

    order = build_order(machines)
    return machines, processing_times, order

def read_data(file_path: str):
    return read_parameters_from_excel(file_path)
