# Job-Splitting FJSSP with Hybrid GA and CPLEX

This project provides two complementary approaches to solve the **Flexible Job-Shop Scheduling Problem with Job-Splitting (FJSSP-JS)**:

* A **Hybrid Genetic Algorithm (HGA)** with Local Search (LSA)
* A **Mixed-Integer Programming (MIP)** model implemented with **IBM CPLEX** via `docplex`

The repository is designed for researchers and students who want to study and benchmark heuristic and exact approaches for advanced scheduling problems in manufacturing and logistics.

---

## Folder Structure

```
JOBSPLIT-FJSSP-HGA-CPLEX/
├── cplex_solver/
│   └── cplex_solver.py        
├── hga/
│   ├── hga.py                 
│   ├── encoding.py           
│   ├── mutation.py            
│   ├── lsa.py                
│   ├── scheduling.py          
│   ├── selection.py, crossover.py, population.py, plot.py, io.py
├── data/
│   ├── 1data.xlsx             
│   └── 2data.xlsx             
├── scripts/
│   ├── run_hga.py             
│   └── run_cplex.py
├── math model/           
│   └── JobSplit_FJSSP.pdf   
├── ref/           
│   └── MIP & hybrid GA.pdf         
├── README.md
├── CITATION.cff
├── requirements.txt
└── .gitignore
```

---

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/trungiemiu/Scheduling.git
   cd Scheduling/jobsplit_fjssp_hga_cplex
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Make sure IBM CPLEX 12.9+ is installed if you want to run the MIP model.

---

## Data Format

The solver supports two schemas:

### A) Light schema (e.g., `data/2data.xlsx`)

* **ProcessingTime**: `Job, Operation, Machine, Processing Time`
* **Lotsize**: `Job, Lotsize`
* **SetupTime** (optional): `Job, Operation, Machine, Setup Time`

Eligibility is inferred from rows in `ProcessingTime`. Non-positive IDs are ignored.

### B) OPL-like schema (e.g., `data/1data.xlsx`)

* **JOSet**: `(job, op)`
* **JOMSet**: `(job, op, machine)`
* **Processingtime**: `(job, op, machine, p)`
* **Lotsize**: `(job, g)`
* **SetupTime** (optional): `(job, op, machine, h)`

---

## Usage

### Run HGA

```bash
python scripts/run_hga.py --data data/2data.xlsx --pop-size 20 --iters 50 --s 10 --beta 5 --seed 42
```

* `--s`: minimum sub-lot size (HGA enforces multiples of s).
* Eligibility is enforced: invalid (job, op, machine) triples cause an error.

### Run CPLEX

```bash
python scripts/run_cplex.py --xlsx data/2data.xlsx --smin 10 --timelimit 600
```

* `--smin`: minimum sub-lot size (linear constraint $\alpha_{ijk} \ge s$).
* If `SetupTime` exists, it is included; otherwise setup times default to 0.

---

## Model Overview

* **Objective**: minimize makespan $C_{max}$.
* **Decision variables**:

  * `x_{ijkl} ∈ {0,1}`: operation assignment to machine position
  * `α_{ijk} ≥ 0`: sub-lot size on machine k
  * `C_{ijk} ≥ 0`: completion times
  * `Cmax ≥ 0`
* **Constraints**:

  * Lot conservation: $∑_k α_{ijk} = g_i$
  * Lower/upper bounds with `smin`: $smin·∑_l x_{ijkl} ≤ α_{ijk} ≤ g_i·∑_l x_{ijkl}$
  * Machine capacity & sequence continuity
  * Precedence inside jobs
  * Optional setup time $h_{ijk}$

---

## Citation

If you use this work, please cite via the `CITATION.cff` file or:

```
Le, Trung. (2025). Job-Splitting FJSSP with Hybrid GA and CPLEX.
GitHub repository: https://github.com/trungiemiu/Scheduling
```

---

## License

MIT License (recommended).
