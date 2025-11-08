# 🔬 Research & Development (AI) Assignment

### Parametric Curve Fitting — Estimation of Unknown Variables (θ, M, X)

---

## 🧠 Problem Overview

The objective of this assignment is to determine the unknown parameters **θ**, **M**, and **X** in the following **parametric equation of a curve**:

[
\begin{aligned}
x(t) &= t\cos(\theta) - e^{M|t|}\sin(0.3t)\sin(\theta) + X \
y(t) &= 42 + t\sin(\theta) + e^{M|t|}\sin(0.3t)\cos(\theta)
\end{aligned}
]

The given data (`xy_data.csv`) contains observed points that lie on this curve for:

[
6 < t < 60
]

The unknown parameters are constrained as follows:
[
0° < \theta < 50°,	 -0.05 < M < 0.05,	 0 < X < 100
]

---

## 🎯 Objective

The goal is to **estimate θ, M, and X** such that the model-generated curve closely fits the observed data points.

Performance is evaluated using the **L1 distance** between predicted and observed points.
Additional credit is given for explanation, reasoning, and reproducibility of results.

---

## ⚙️ Approach & Methodology

The solution was developed using **Python** with numerical optimization techniques.

### Step-by-step approach:

1. **Data loading:**
   The file `xy_data.csv` was read using `pandas`.
   Since the CSV does not contain explicit `t` values, it was assumed that the data points are **uniformly sampled** in the range (6 < t < 60).

2. **Model definition:**
   A function representing the parametric equations was implemented in Python.

3. **Objective functions:**
   Two cost functions were used:

   * **L2 loss** (sum of squared errors) for smooth convergence.
   * **L1 loss** (sum of absolute coordinate errors) for final accuracy, aligning with the assignment metric.

4. **Optimization:**

   * Stage 1: Used **L-BFGS-B** (a quasi-Newton optimizer) on the L2 loss to find a good initial guess.
   * Stage 2: Refined the parameters using **Powell’s method** to minimize the L1 loss directly.

5. **Validation & visualization:**

   * Plotted the observed and predicted points using Matplotlib.
   * Verified the final curve in **Desmos** for correctness and alignment.

---

## 📈 Results

| Parameter   | Symbol | Value              |
| ----------- | ------ | ------------------ |
| θ (radians) | θ      | **0.4906853921**   |
| θ (degrees) | θ      | **28.1142020341°** |
| M           | M      | **0.0214149186**   |
| X           | X      | **54.9010741476**  |

### Fit quality:

* **Total L1 distance:** 37865.10
* **Mean L1 per point:** 25.24

The parameters are within the specified bounds, and the fitted curve visually matches the given data distribution.

---

## 🧮 Final Parametric Expression (for Desmos)

Copy and paste the following into [Desmos Graphing Calculator](https://www.desmos.com/calculator):

```
(t*cos(0.4906853921) - e^(0.0214149186*abs(t))*sin(0.3t)*sin(0.4906853921) + 54.9010741476,
 42 + t*sin(0.4906853921) + e^(0.0214149186*abs(t))*sin(0.3t)*cos(0.4906853921)) {6 < t < 60}
```

This reproduces the final fitted curve visually.

---

## 🧩 Repository Structure

```
flam-assignment/
├── xy_data.csv
├── fit_parametric_curve.py
├── flam-assignment.ipynb
├── fitted_curve.png
└── README.md
```

---

## 🚀 How to Run

### 🔹 Local (Windows / Linux)

```bash
pip install numpy pandas scipy matplotlib
python fit_parametric_curve.py
```

### 🔹 Google Colab

1. Upload `xy_data.csv` using the `files.upload()` command.
2. Run each code cell in order.
3. The notebook will output optimal parameters, L1 scores, and plots.

---

## 🔍 Assumptions

* The dataset is uniformly sampled for `t ∈ (6, 60)`.
* All computations are in **radians** unless otherwise specified.
* The exponential term `e^{M|t|}` remains numerically stable as |M| < 0.05.

---

## 📊 Visualization Example

A plot comparing the **observed points (blue)** and **fitted curve (orange)** demonstrates close alignment and periodic behavior consistent with the dataset.

*(`plots/fitted_curve.png` included in the repository)*

---
**Author:** Gautham Ratiraju
**Repository:** [https://github.com/Gautham07s/flam-assignment](https://github.com/Gautham07s/flam-assignment)
