# FJSSP-SA-TS-CPLEX

This project implements **Flexible Job Shop Scheduling (FJSSP)** with three approaches:

* **CPLEX MIP model** (`src/solvers/cplex_mip.py`, run with `scripts/run_cplex.py`)
* **Simulated Annealing (SA)** (`src/heuristics/sa.py`, run with `scripts/run_sa.py`)
* **Tabu Search (TS)** (`src/heuristics/tabu.py`, run with `scripts/run_ts.py`)

## Repository structure

```
FJSSP-SA-TS-CPLEX/
├─ data/         # Excel input instances
├─ docs/         # Papers, slides
├─ scripts/      # Entry points
├─ src/
│  ├─ core/      # models, scheduler, io_utils
│  ├─ heuristics/# sa, tabu
│  ├─ solvers/   # cplex_mip
│  └─ viz/       # plotting
└─ requirements.txt
```

## Installation

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
```

> Note: CPLEX and its Python bindings (docplex/cplex) are required if running the MIP solver.

## Running examples

```bash
# Run CPLEX MIP
python scripts/run_cplex.py --data data\3J7O3M.xlsx --plot

# Run Simulated Annealing
python scripts/run_sa.py --data data\3J7O3M.xlsx --iters 1000 --seed 42 --plot

# Run Tabu Search
python scripts/run_ts.py --data data\3J7O3M.xlsx --iters 600 --seed 42 --plot
```

### Common arguments

* `--data`: path to Excel instance file
* `--iters`: number of iterations (for heuristics)
* `--seed`: random seed for reproducibility
* `--plot`: plot a Gantt chart of the schedule

## Data format

See `data/README.md`.
Excel files define:

* **Processing Times**: each operation has candidate machines and times
* **Setup Times** (optional): changeover time between operations on the same machine
* **Jobs/Operations**: order of operations within each job

## Results

* Logs and metrics: `experiments/<run>/`
* Figures: `results/figures/`
* Summary tables: `results/tables/`

## Citation

See `../CITATION.cff`.

## License

MIT (see `../LICENSE`).
