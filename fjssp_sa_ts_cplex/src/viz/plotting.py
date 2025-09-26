from typing import List, Tuple, Sequence, Any
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from src.core.models import Job, Machine

def plot_gantt(
    data: Any,
    title: str = "Gantt",
    legend_right: bool = True,
    show_job_legend: bool = True
):
    fig, ax = plt.subplots(figsize=(10, 4))
    is_jobs_mode = isinstance(data, (tuple, list)) and len(data) == 2 and isinstance(data[0], list)
    handles = []
    if is_jobs_mode:
        jobs: List[Job] = data[0]
        machines: List[Machine] = data[1]
        machines_sorted = sorted(machines, key=lambda x: x.name)
        job_names = [j.job_name for j in jobs]
        cmap = plt.cm.get_cmap("tab20", max(1, len(job_names)))
        color_of = {jn: cmap(i) for i, jn in enumerate(job_names)}
        bar_h, gap = 0.35, 0.15
        for i, m in enumerate(machines_sorted):
            y = i * (bar_h + gap)
            for op_name, start, end in m.operations:
                jname, opid_s = op_name.split("O")[0], op_name.split("O")[1]
                opid = int(opid_s)
                job = next(j for j in jobs if j.job_name == jname)
                op = next(o for o in job.operations if o.operation_id == opid)
                setup_end = start + op.setup_time
                color = color_of[jname]
                ax.barh(y, op.setup_time, left=start, height=bar_h, color=color, edgecolor="black", hatch="//", alpha=0.9)
                ax.barh(y, op.time_required, left=setup_end, height=bar_h, color=color, edgecolor="black")
                ax.text(setup_end + op.time_required / 2.0, y, f"O{opid}", va="center", ha="center", color="white", fontsize=8)

        ax.set_yticks([i * (bar_h + gap) for i in range(len(machines_sorted))])
        ax.set_yticklabels([m.name for m in machines_sorted])
        handles = [mpatches.Patch(facecolor="white", edgecolor="black", hatch="//", label="Setup")]
        if show_job_legend:
            for jn in job_names:
                handles.append(mpatches.Patch(facecolor=color_of[jn], edgecolor="black", label=f"Job {jn}"))
    else:
        gantt_rows: Sequence[Tuple[str, str, int, float, float, float]] = data
        machines = sorted({r[0] for r in gantt_rows})
        jobs = sorted({r[1] for r in gantt_rows})
        cmap = plt.cm.get_cmap("tab20", max(1, len(jobs)))
        color_of = {jn: cmap(i) for i, jn in enumerate(jobs)}
        bar_h, gap = 0.35, 0.15
        for i, mname in enumerate(machines):
            y = i * (bar_h + gap)
            rows = [r for r in gantt_rows if r[0] == mname]
            for (_, jname, op, ss, sp, e) in rows:
                c = color_of[jname]
                setup_dur = max(0.0, sp - ss)
                ax.barh(y, setup_dur, left=ss, height=bar_h, color=c, edgecolor="black", hatch='//', alpha=0.9)
                proc_dur = max(0.0, e - sp)
                ax.barh(y, proc_dur, left=sp, height=bar_h, color=c, edgecolor="black")
                if proc_dur > 0:
                    ax.text(sp + proc_dur / 2.0, y, f"O{op}", ha="center", va="center", color="white", fontsize=8)

        ax.set_yticks([i * (bar_h + gap) for i in range(len(machines))])
        ax.set_yticklabels(machines)

        handles = [mpatches.Patch(facecolor="white", edgecolor="black", hatch="//", label="Setup")]
        if show_job_legend:
            for jn in jobs:
                handles.append(mpatches.Patch(facecolor=color_of[jn], edgecolor="black", label=f"Job {jn}"))

    ax.set_xlabel("Time"); ax.set_ylabel("Machines"); ax.set_title(title)
    plt.tight_layout()

    if legend_right and handles:
        ax.legend(handles=handles, title="Jobs", loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=True)
        fig.subplots_adjust(right=0.78)
    elif handles:
        ax.legend(handles=handles, frameon=True)

    return fig, ax

def plot_history(history: List[float], title: str = "Best makespan over iterations"):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(len(history)), history)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Best Cmax")
    ax.set_title(title)
    fig.tight_layout()
    return fig, ax
