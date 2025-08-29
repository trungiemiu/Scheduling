# FJSSP-GA & CPLEX

This repository provides a Python implementation of the **Flexible Job Shop Scheduling Problem (FJSSP)** using two approaches:

* **Genetic Algorithm (GA):** A metaheuristic implemented in Python with operators (selection, crossover, mutation, repair, etc.) and visualization via machine-based Gantt charts.
* **CPLEX (docplex):** A Mixed Integer Programming (MIP) model formulation with machine assignment variables, solved using IBM CPLEX, and visualized using the same GA-style Gantt charts.

---

## ✨ Features

* **GA implementation:** Population-based search, repair operators, and makespan tracking.
* **CPLEX model:** Incorporates machine assignment, disjunctive constraints, and produces optimal or near-optimal schedules.
* **Visualization:** Gantt charts based on chromosomes (from GA) or machine assignments (from CPLEX).
* **Clean project structure:** Clear separation of GA, CPLEX, and scripts for easy execution.

---

## 📂 Project Structure

```
fjssp_ga_cplex/
├─ ga/                  # Genetic Algorithm implementation
│  ├─ operators/        # GA operators (crossover, mutation, repair, etc.)
│  ├─ ga.py, mainga.py, schedule.py, utils.py, viz.py
├─ cplex_solver/        # CPLEX MIP model & visualization helpers
│  ├─ cplex_solver.py
│  └─ viz.py
├─ scripts/             # Command-line entry points
│  ├─ run_ga.py         # Run GA solver
│  └─ run_cplex.py      # Run CPLEX solver
├─ data/                # Input data
│  └─ Data.xlsx
├─ Math models/         # Documentation 
│  └─ Code_Cplex.docx   # Code if you use the IBM CPlex Studio 
│  └─ Mathematical Model.docx # Math model for FJSSP 
├─ README.md
├─ LICENSE
├─ requirements.txt
├─ pyproject.toml
├─ CITATION.cff
└─ .gitignore
```

---

## ▶️ Usage

### Run GA

```bash
# Run with Python module
python -m scripts.run_ga --input data/Data.xlsx --pop 20 --gen 100 --mut 0.2 --viz

# Or use shortcut (after pip install -e .)
runga --input data/Data.xlsx --pop 20 --gen 100 --mut 0.2 --viz
```

### Run CPLEX

```bash
# Run with Python module
python -m scripts.run_cplex --input data/Data.xlsx --viz --title "FJSSP Gantt (CPLEX)"

# Or use shortcut (after pip install -e .)
runcplex --input data/Data.xlsx --viz --title "FJSSP Gantt (CPLEX)"
```

* `--viz`: plot Gantt chart using GA-style visualization.
* `--title`: custom chart title.

---

## 📜 Data Format (Excel)

* **Sheet `indices`:** contains `numJ`, `numO`, `numM`.
* **Sheet `P`:** columns `j`, `o`, `P` for processing times.
* **Sheet `M`:** columns `j`, `o`, and machine eligibility (1 = can process, 0 = not available).

---

## 📦 Installation

```bash
cd fjssp_ga_cplex
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt

# Or editable mode with CLI shortcuts
pip install -e .
```

---

## 🧾 Citation

If you use this code, please cite it as described in [CITATION.cff](CITATION.cff).

---

## 📜 License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for details.
