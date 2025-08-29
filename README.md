# Scheduling Problems Repository

Welcome to the **Scheduling Repository** – a comprehensive collection of problems, models, and solution methods for **Scheduling Problems** and their variants. This repository is designed for researchers, students, and practitioners who are interested in studying, implementing, and benchmarking optimization methods for scheduling in manufacturing, services, and logistics.

## 🔎 About Scheduling Problems

Scheduling problems arise in diverse real-world contexts, where limited resources must be allocated to tasks over time. The objective is often to minimize makespan, lateness, or cost, or to maximize throughput and efficiency. Scheduling is a cornerstone of **operations research** and **industrial engineering**, with applications in:

* Manufacturing systems and production planning
* Job shop and flow shop scheduling
* Workforce scheduling and rostering
* Project management
* Healthcare operations (operating rooms, staff shifts)
* Transportation and logistics

Scheduling is typically **NP-hard**, meaning that exact optimization methods struggle to solve large instances efficiently. This makes it an important domain for both theoretical research and practical innovations.

## ⚙️ Repository Content

This repository contains:

* **Problem definitions**: Mathematical formulations and standardized data formats.
* **Solution methods**: Implementations of exact algorithms, heuristics, and metaheuristics.
* **Test instances**: Sample datasets and benchmark cases for evaluation.
* **Visualization tools**: Gantt chart plotting and performance tracking.

## 🧠 Solution Approaches

Scheduling problems can be approached using a variety of methods:

### 1. **Exact Methods**

* Mixed Integer Programming (MIP)
* Branch and Bound / Branch and Cut
* Constraint Programming

These methods guarantee optimality but are often limited to small and medium-scale problems.

### 2. **Heuristics**

* Dispatching rules (e.g., Shortest Processing Time, Earliest Due Date)
* Greedy constructive methods
* Local search

Heuristics provide quick solutions, useful for large-scale and real-time applications.

### 3. **Metaheuristics**

* Genetic Algorithms (GA)
* Simulated Annealing (SA)
* Tabu Search (TS)
* Particle Swarm Optimization (PSO)
* Ant Colony Optimization (ACO)
* Hybrid and Adaptive Metaheuristics

Metaheuristics balance solution quality with scalability, making them popular in practice.

### 4. **Advanced Approaches**

* Matheuristics (combination of exact methods and heuristics)
* Decomposition techniques
* Learning-enhanced optimization (machine learning + OR)

## 🚀 Why This Repository?

* To **learn**: Gain hands-on experience with scheduling models and algorithms.
* To **experiment**: Benchmark methods on classical and custom datasets.
* To **contribute**: Share improvements, new models, or new solution approaches.

## 📌 How to Use

1. Clone the repository:

   ```bash
   git clone https://github.com/trungiemiu/Scheduling.git
   ```
2. Explore subfolders for specific problem types and algorithms.
3. Run scripts to test and visualize scheduling solutions.

## 📚 References

For further study of scheduling theory and applications:

* Pinedo, M. (2016). *Scheduling: Theory, Algorithms, and Systems*.
* Brucker, P. (2007). *Scheduling Algorithms*.

---

This repository is a growing collection of scheduling problems and solutions. Contributions, feedback, and new methods are welcome to expand its scope and impact.
