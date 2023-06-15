# Based on https://doi.org/10.1021/je60081a007
# Some functions to calculate the density of KCl solutions.

import numpy as np
from matplotlib import pyplot as plt

d = np.array([
    [1.002e3, 0.472e2, -1.73],
    [-0.168, -0.537e-1, -0.615e-2],
    [-0.248e-2, 0.128e-3, 0.112e-3]
]).T

a = np.array([
    [0.489, -0.744e-1, 0.755e-2],
    [-0.280e-2, 0.132e-2, -0.176e-3],
    [0.189e-4, -0.767e-5, 0.104e-5]
]).T

t = 25
p = 0.1e-3


def calculate_alpha(t, m):
    alpha = 0
    for i in range(3):
        for j in range(3):
            alpha += a[i, j] * m**i * t**j

    return alpha


def calculate_rho_0(t, m):
    rho_0 = 0
    for i in range(3):
        for j in range(3):
            rho_0 += d[i, j] * m**i * t**j

    return rho_0


def calculate_rho(p, t, m):
    return calculate_rho_0(t, m) * (1 + calculate_alpha(t, m) * p)


concentrations = np.linspace(0, 4)

densities = calculate_rho(p, t, concentrations)
alphas = 1 + calculate_alpha(t, concentrations) * p
rho_0_s = calculate_rho_0(t, concentrations)
plot_vector = np.array([densities, alphas, rho_0_s]).T
plt.plot(concentrations, plot_vector, label=["$\\rho$", "$\\alpha$", "$\\rho_0$"])
plt.legend()
plt.xlabel("Concentration ($mol/kg$)")
plt.ylabel("Density ($kg/m^3$)")
plt.show()

print(calculate_rho(p, t, 2))
