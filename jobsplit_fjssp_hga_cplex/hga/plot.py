from typing import List, Optional
import pandas as pd
import matplotlib.pyplot as plt

def plot_history(history_makespan: List[float], path: Optional[str] = None) -> None:
    plt.figure(figsize=(10, 5))
    xs = range(len(history_makespan))
    plt.plot(xs, history_makespan)
    plt.title("Best Makespan over Generations")
    plt.xlabel("Generation (0 = initial)")
    plt.ylabel("Makespan")
    plt.grid(True)
    plt.tight_layout()
    if path:
        plt.savefig(path, dpi=150)
        plt.close()
    else:
        plt.show()

def plot_gantt_chart(details: List[dict], path: Optional[str] = None) -> None:
    df = pd.DataFrame(details)
    if df.empty:
        return

    uniq = df[["J", "O"]].drop_duplicates().reset_index(drop=True)
    color_map = {tuple(r): f"C{i % 10}" for i, r in uniq.iterrows()}

    plt.figure(figsize=(16, 8))
    for _, row in df.iterrows():
        color = color_map[(int(row["J"]), int(row["O"]))]
        dur = float(row["End"]) - float(row["Start"])
        plt.barh(row["M"], dur, left=row["Start"], color=color, edgecolor="black")
        plt.text(row["Start"] + dur / 2.0, row["M"],
                 f"J{int(row['J'])}O{int(row['O'])}\n{int(row['Sublot'])}",
                 ha="center", va="center", fontsize=8)

    plt.xlabel("Time")
    plt.ylabel("Machine")
    plt.title("Gantt Chart")
    plt.yticks(sorted(df["M"].unique()))
    plt.tight_layout()
    if path:
        plt.savefig(path, dpi=150)
        plt.close()
    else:
        plt.show()
