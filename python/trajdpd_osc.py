"""
Shear a system of pure DPD particles using LE boundary conditions. Save kinetic, dissipative, non-dissipative stress values and number of pairs during simulation.
"""

import espressomd
from espressomd.io.writer import h5md

import espressomd.lees_edwards as lees_edwards

import numpy as np

import argparse

import json

# Set up of parameters

#Give in parameters
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--kT', type=float, default=1.0,
                     help="temperature")
parser.add_argument('--rcut', type=float, default=1.0,
                     help="DPD fluid particle diameter")
parser.add_argument('--aij', type=float, default=25.0,
                     help="DPD fluid repulsion parameter ")
parser.add_argument('--gamma', type=float, default=4.5,
                     help="DPD thermostat friction")
parser.add_argument('--rho', type=float, default=3,
                     help="DPD fluid density")
parser.add_argument('--vel', type=float, default=1.0,
                     help="Shear velocity")
parser.add_argument('--samples', type=int, default=3000,
                     help="number of sampling loops")
parser.add_argument('--iterations', type=int, default=10000,
                     help="number of iterations")
parser.add_argument('--N', type=int, default=10000,
                     help="number of DPD particles")
parser.add_argument('--savedata', action='store_true',
                     help ="write the data to a data base")
parser.add_argument('--n_nodes_x', type=int, default=8,
                     help ="Number of nodes in one 'False' direction")
parser.add_argument('--n_nodes_y', type=int, default=8,
                     help ="Number of nodes in other 'False' direction")
parser.add_argument('--frequency', type=float, default=0.1,
                     help ="Frequency of the osc shear flow")
parser.add_argument('--amplitude', type=float, default=0.1,
                     help ="Amplitude of the osc shear flow")


args = parser.parse_args()

# Give parameters simpler names
gamma = args.gamma
kT = args.kT
r_cut = args.rcut
rho = args.rho
n_part = args.N
F_max = args.aij
n_nodes_y = args.n_nodes_y
n_nodes_x = args.n_nodes_x
iterations = args.iterations
frequency = args.frequency
amplitude = args.amplitude


# Calculate box length
vol = args.N / args.rho
l = np.cbrt(vol)

# Calculate shearing params
omega = 2 * np.pi * frequency
amplitude = l * amplitude

# Set up the box
system = espressomd.System(box_l=[l, l, l])
system.set_random_state_PRNG()
np.random.seed(seed=system.seed)

# Test line for lees edwards
system.cell_system.node_grid = [1, n_nodes_x, n_nodes_y]
system.cell_system.set_domain_decomposition(fully_connected=[True, False, False])
system.cell_system.set_domain_decomposition()

# Add randomly distributed DPD particles to the box
pos = system.box_l * np.random.random((n_part, 3))
system.part.add(pos=pos)

# Set up the time step, skin and thermostat
dt = 0.005
system.time_step = dt
system.thermostat.set_dpd(kT=kT, seed=42)
system.cell_system.skin = 0.4

# Set up the DPD friction interaction
system.non_bonded_inter[0, 0].dpd.set_params(
    weight_function=1, gamma=gamma, r_cut=r_cut,
    trans_weight_function=0, trans_gamma=0, trans_r_cut=0)

# Set up the repulsive interaction
system.non_bonded_inter[0,0].hat.set_params(F_max=F_max, cutoff=r_cut)

# Warm up and equilibration
system.integrator.run(100000)

# Take care of the COM movement
system.galilei.galilei_transform()

# Add Lees-Edwards to the script
system.cell_system.node_grid = [1, n_nodes_x, n_nodes_y]
system.cell_system.set_domain_decomposition(fully_connected=[True, False, False])

system.lees_edwards.protocol = lees_edwards.OscillatoryShear(
        frequency = omega,
        amplitude = amplitude,
        shear_direction = 0,
        shear_plane_normal = 1)

# Open h5md file
h5 = h5md.H5md(filename="./trajectory.h5", write_pos=True, write_lees_edwards_offset = True, write_vel = True, write_ordered=True)


# Sampling + write h5md files
for i in range(args.samples):

    h5.write()

    print("Step:", i, flush=True)
    system.integrator.run(iterations)

#Close all the files
h5.close()
