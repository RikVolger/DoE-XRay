"""Generates experimental matrix for tomography experiments

Uses the python DOE2 library and numpy
"""


import pyDOE2
import numpy as np

# experimental levels required of the different fluid additions
levels = [
    5,      # compound A
    5,      # compound B
    5,      # compound C
    5,      # compound D
    ]

# reduction values. 100000 leads to 37 GB array requirement, not possible
reduction = 8

# Create Generalized Subset Design
design = pyDOE2.gsd(levels, reduction)

# Save design values as txt file
np.savetxt("./design.txt", design, fmt="%d")

print(f"{design.shape[0]} experiments required.")
