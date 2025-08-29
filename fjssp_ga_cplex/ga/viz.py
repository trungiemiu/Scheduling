import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import AnchoredText

from .gene import parse_gene 
from .schedule import get_operation_details

__all__ = [
    "plot_makespan_history",
    "plot_gantt_chart",
    "animate_gantt_and_makespan",
    "chromosome_gantt_chart",
]


def plot_makespan_history(makespan_history):
    if not makespan_history:
        print("plot_makespan_history: empty history, skip.")
        return
    plt.figure(figsize=(10, 6))
    plt.plot(makespan_history, marker="o")
    plt.title("Makespan History Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Makespan")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


def plot_gantt_chart(operation_details, ax, job_colors, show_xlabel=True):
    ax.clear()
    ax.set_xlabel("Time" if show_xlabel else "")
    ax.set_ylabel("Machines")

    if not operation_details:
        ax.set_title("Gantt Chart (no data)")
        return

    mmax = max(machine for _, machine, _, _, _ in operation_details)
    ax.set_yticks(range(1, mmax + 1))
    ax.set_yticklabels(range(1, mmax + 1))
    ax.grid(True, axis="both", linestyle="--", alpha=0.35)

    for gene, machine, start, end, duration in operation_details:
        op_label = "O?"
        job_key = None
        try:
            j, o = parse_gene(gene)
            job_key = f"J{j}"
            op_label = f"O{o}"
        except Exception:
            if isinstance(gene, str):
                job_key = gene[:2] if len(gene) >= 2 else "J?"
                op_label = gene[2:] if len(gene) > 2 else "O?"
            else:
                job_key = "J?"

        color = job_colors.get(job_key, None)
        ax.broken_barh([(start, duration)], (machine - 0.4, 0.8), facecolors=color)
        ax.text(start + duration / 2.0, machine, op_label, ha="center", va="center", color="white")

    ax.set_title("Gantt Chart")


def animate_gantt_and_makespan(details_history, makespan_history, color_map, num_generations: int):
    if not details_history or not makespan_history:
        print("animate_gantt_and_makespan: empty input, skip.")
        return None

    fig = plt.figure(figsize=(10,6), constrained_layout=True, dpi=100)
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 2])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])

    def update(frame):
        plot_gantt_chart(details_history[frame], ax1, color_map, show_xlabel=False)
        ax1.set_title(f"Gantt Chart - Generation {frame + 1}")

        handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in color_map.values()]
        labels = list(color_map.keys())
        if handles and labels:
            leg = ax1.legend(handles, labels, title="Jobs",
                             loc="upper right", frameon=True, fancybox=True, borderpad=0.4)
            leg.get_frame().set_alpha(0.85)
            leg.get_frame().set_edgecolor("0.5")
            leg.set_draggable(True)

        ax2.clear()
        ax2.plot(makespan_history[: frame + 1], marker="o")
        ymax = max(makespan_history) if makespan_history else 1.0
        ax2.set_ylim(0, ymax * 1.1)
        ax2.set_title("Makespan History", pad=10) 
        ax2.set_xlabel("Generation")
        ax2.set_ylabel("Makespan")
        ax2.grid(True, linestyle="--", alpha=0.4)
        at = AnchoredText(f"Current Makespan: {makespan_history[frame]:.2f}",
                          loc="upper right", prop=dict(size=10), frameon=True, borderpad=0.5)
        at.patch.set_boxstyle("round,pad=0.4")
        at.patch.set_edgecolor("black")
        at.patch.set_facecolor("lightgrey")
        ax2.add_artist(at)

    ani = FuncAnimation(fig, update, frames=num_generations, repeat=False)
    if not hasattr(animate_gantt_and_makespan, "_anims"):
        animate_gantt_and_makespan._anims = []
    animate_gantt_and_makespan._anims.append(ani)

    plt.show()
    return ani


def chromosome_gantt_chart(best_chromosome, machines, processing_times, title="Gantt Chart"):
    operation_details = get_operation_details(best_chromosome, machines, processing_times)
    fig, ax = plt.subplots(figsize=(10, 6))
    num_jobs = max(len(machine) for machine in machines.values())
    from .utils import generate_color_map
    color_map = generate_color_map(num_jobs)

    plot_gantt_chart(operation_details, ax, color_map, show_xlabel=True)

    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in color_map.values()]
    labels = list(color_map.keys())
    if handles and labels:
        leg = ax.legend(handles, labels, title="Jobs",
                        loc="upper right", frameon=True, fancybox=True, borderpad=0.4)
        leg.get_frame().set_alpha(0.85)
        leg.get_frame().set_edgecolor("0.5")

    ax.set_title(title)
    plt.tight_layout()
    plt.show()
