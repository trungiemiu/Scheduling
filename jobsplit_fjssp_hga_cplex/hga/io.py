from typing import Dict, List, Tuple
import pandas as pd

Lookup = Dict[Tuple[int, int, int], float] 

def create_processing_time_lookup_table(processing_time_rows):
    lookup = {}
    for j, o, m, p in processing_time_rows:
        lookup[(int(j), int(o), int(m))] = float(p)
    return lookup


def read_job_scheduling_data(file_path: str):
    xls = pd.ExcelFile(file_path)
    ls_df = pd.read_excel(xls, sheet_name="Lotsize", usecols=lambda c: True)
    cols_lc = {c.lower().strip(): c for c in ls_df.columns}
    if "lot size" in cols_lc:
        lot_col = cols_lc["lot size"]
    elif "lotsize" in cols_lc:
        lot_col = cols_lc["lotsize"]
    else:
        lot_col = ls_df.select_dtypes(include="number").columns[0]
    lot_size = [int(x) for x in ls_df[lot_col].tolist()]
    num_job = len(lot_size)
    pt_sheet = "ProcessingTime" if "ProcessingTime" in xls.sheet_names else "Processing Time"

    allowed = {"job", "operation", "machine", "processingtime", "processing time", "time"}
    pt_df = pd.read_excel(
        xls, sheet_name=pt_sheet,
        usecols=lambda c: c.strip().lower() in allowed
    )

    m = {c.lower().strip(): c for c in pt_df.columns}
    jcol = m.get("job")
    ocol = m.get("operation")
    mcol = m.get("machine")
    tcol = m.get("processingtime") or m.get("processing time") or m.get("time")
    if not all([jcol, ocol, mcol, tcol]):
        raise ValueError(
            f"ProcessingTime not enough dolumn (Job, Operation, Machine, Processing Time/ProcessingTime/Time). "
            f"Current: {list(pt_df.columns)}"
        )
    num_operation = int(pt_df[ocol].max())
    num_machine = int(pt_df[mcol].max())
    processing_lookup: Lookup = {}
    for _, r in pt_df.iterrows():
        j, o, mm, tt = int(r[jcol]), int(r[ocol]), int(r[mcol]), float(r[tcol])
        processing_lookup[(j, o, mm)] = tt

    return num_job, num_operation, num_machine, lot_size, processing_lookup
