import numpy as np
import pandas as pd
import math
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import os

# -------------------------------
# Configuration
# -------------------------------
DATA_PATH = os.path.join('data', 'xy_data.csv')  # Change path if needed
PLOT_PATH = os.path.join('plots', 'fitted_curve.png')

# Ensure directories exist
os.makedirs('plots', exist_ok=True)
os.makedirs('data', exist_ok=True)

# -------------------------------
# Load Data
# -------------------------------
try:
    data = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"CSV file not found at {DATA_PATH}. Please place xy_data.csv in the data/ folder.")

# Use t from file if available; otherwise assume uniform sampling
t = data['t'].values if 't' in data.columns else np.linspace(6, 60, len(data))
x_obs = data['x'].values
y_obs = data['y'].values
n = len(data)

# -------------------------------
# Model Function
# -------------------------------
def model(params, t):
    theta, M, X = params
    exp_term = np.exp(M * np.abs(t)) * np.sin(0.3 * t)
    x_pred = t * np.cos(theta) - exp_term * np.sin(theta) + X
    y_pred = 42 + t * np.sin(theta) + exp_term * np.cos(theta)
    return x_pred, y_pred

# -------------------------------
# Objective Functions
# -------------------------------
def obj_L1(params):
    x_pred, y_pred = model(params, t)
    return np.sum(np.abs(x_pred - x_obs) + np.abs(y_pred - y_obs))

def obj_L2(params):
    x_pred, y_pred = model(params, t)
    return np.sum((x_pred - x_obs)**2 + (y_pred - y_obs)**2)

# -------------------------------
# Optimization
# -------------------------------
print("\nStarting optimization...")

# Parameter bounds: theta (radians), M, X
bounds = [(1e-10, 50 * math.pi / 180 - 1e-10), (-0.05, 0.05), (1e-10, 100 - 1e-10)]

# Initial guess
x0 = np.array([0.5, 0.0, 20.0])

# Stage 1: L2 optimization (smooth objective)
res_l2 = minimize(obj_L2, x0, method='L-BFGS-B', bounds=bounds)

# Stage 2: L1 refinement (target metric)
res_l1 = minimize(obj_L1, res_l2.x, method='Powell', bounds=bounds, options={'maxiter': 20000})

theta_opt, M_opt, X_opt = res_l1.x
x_pred, y_pred = model(res_l1.x, t)

total_L1 = np.sum(np.abs(x_pred - x_obs) + np.abs(y_pred - y_obs))
mean_L1 = total_L1 / n
theta_deg = theta_opt * 180 / math.pi

# -------------------------------
# Output Results
# -------------------------------
print("\n✅ Optimization Complete")
print(f"Theta (radians): {theta_opt:.10f}")
print(f"Theta (degrees): {theta_deg:.6f}")
print(f"M: {M_opt:.10f}")
print(f"X: {X_opt:.10f}")
print(f"Total L1 distance: {total_L1:.6f}")
print(f"Mean L1 per point: {mean_L1:.6f}")

# -------------------------------
# Visualization
# -------------------------------
plt.figure(figsize=(8,6))
plt.scatter(x_obs, y_obs, s=6, label='Observed Data', alpha=0.6)
plt.plot(x_pred, y_pred, '-', linewidth=2, label='Fitted Curve', color='orange')
plt.axis('equal')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Observed vs Fitted Parametric Curve')
plt.grid(True)
plt.tight_layout()
plt.savefig(PLOT_PATH)
plt.show()

# -------------------------------
# Export LaTeX Expression
# -------------------------------
latex_expr = (
    r"(t*cos({theta:.10f}) - e^({M:.10f}*abs(t))*sin(0.3t)*sin({theta:.10f}) + {X:.10f}, "
    r"42 + t*sin({theta:.10f}) + e^({M:.10f}*abs(t))*sin(0.3t)*cos({theta:.10f}))".format(
        theta=theta_opt, M=M_opt, X=X_opt
    )
)

print("\n📜 LaTeX Expression (for Desmos or README):\n")
print(latex_expr)

# Save results to text file
with open('results.txt', 'w') as f:
    f.write(f"Theta (rad): {theta_opt:.10f}\n")
    f.write(f"Theta (deg): {theta_deg:.6f}\n")
    f.write(f"M: {M_opt:.10f}\n")
    f.write(f"X: {X_opt:.10f}\n")
    f.write(f"Total L1: {total_L1:.6f}\n")
    f.write(f"Mean L1 per point: {mean_L1:.6f}\n\n")
    f.write("LaTeX Expression:\n")
    f.write(latex_expr)

print(f"\nResults saved to 'results.txt' and plot saved to '{PLOT_PATH}'.")
