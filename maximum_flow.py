import numpy as np
from matplotlib import pyplot as plt


def calculate_surface_from_diameter(d):
    r = d / 2
    A = r**2 * np.pi

    return A


def calculate_gas_flow_from_velocity(u_g, d):
    A = calculate_surface_from_diameter(d)

    F_g = u_g * A * 10**3 * 60  # l/min

    return F_g


def calculate_max_velocity_from_diameter(F_g_max, d):
    A = calculate_surface_from_diameter(d)

    u_g_max = F_g_max / (A * 10**3 * 60)

    return u_g_max


u_g_range = np.linspace(0, 0.30)
d_range = np.atleast_2d([.10, .15, .16, .17, .20]).T

F_g = calculate_gas_flow_from_velocity(u_g_range, d_range)

plt.figure(figsize=(5, 3), dpi=300)
plt.plot(u_g_range, F_g.T, label=[f"{d[0]:.2f} cm" for d in d_range])
plt.plot([0, 0.3], [10, 10], linestyle="dashed", color="#00000040")
plt.plot([0, 0.3], [100, 100], linestyle="dashed", color="#00000061")
plt.title("$F_g$ required for $u_g$ in different diameter columns")
plt.legend()
plt.xlabel("$u_g\ (cm/s)$")
plt.ylabel("$F_g\ (l/min)$")
plt.tight_layout()

d_range_dense = np.linspace(0.05, 0.30)
F_g_max = np.atleast_2d([10, 100, 150, 300, 1500]).T

u_g_max = calculate_max_velocity_from_diameter(F_g_max, d_range_dense)

plt.figure(figsize=(5, 3), dpi=300)
plt.plot(d_range_dense, u_g_max.T, label=[f"{F[0]:.0f} l/min" for F in F_g_max])
plt.plot([0.05, 0.3], [0.3, 0.3], linestyle="dashed", color="#00000040")
plt.title("$u_{g, max}$ as a function of $d_{column}$ for given $F_{g, max}$")
plt.legend()
plt.xlabel("$d\ (m)$")
plt.ylabel("$u_{g, max}\ (m/s)$")
plt.xlim((0.05, 0.3))
plt.ylim((0, 0.5))
plt.tight_layout()

plt.show()
