from itertools import cycle
import matplotlib.pyplot as plt

__all__ = ["generate_color_map"]

def generate_color_map(num_jobs: int):
    try:
        colors = plt.get_cmap("tab20").colors
    except Exception:
        colors = plt.rcParams["axes.prop_cycle"].by_key().get("color", ["C0", "C1", "C2", "C3"])
    color_cycle = cycle(colors)
    return {f"J{i + 1}": next(color_cycle) for i in range(num_jobs)}
