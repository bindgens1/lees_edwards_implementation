"""
Shear a system of pure DPD particles using LE boundary conditions. Save kinetic, dissipative, non-dissipative stress values and number of pairs during simulation.
"""

import espressomd
from espressomd.accumulators import Correlator
from espressomd.observables import ParticlePositions, ParticleVelocities

import espressomd.lees_edwards as lees_edwards

import numpy as np

from scipy import integrate
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt

import argparse

import json

# Set up of parameters

#Give in parameters
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--kT', type=float, default=1.0,
                     help="temperature")
parser.add_argument('--rcut', type=float, default=1.0,
                     help="DPD fluid particle diameter")
parser.add_argument('--aij', type=float, default=175,
                     help="DPD fluid repulsion parameter ")
parser.add_argument('--gamma', type=float, default=4.5,
                     help="DPD thermostat friction")
parser.add_argument('--rho', type=float, default=3,
                     help="DPD fluid density")
parser.add_argument('--vel', type=float, default=1.0,
                     help="Shear velocity")
parser.add_argument('--samples', type=int, default=200000,
                     help="number of sampling loops")
parser.add_argument('--iterations', type=int, default=100,
                     help="number of iterations")
parser.add_argument('--N', type=int, default=10000,
                     help="number of DPD particles")
parser.add_argument('--savedata', action='store_true',
                     help ="write the data to a data base")
parser.add_argument('--n_nodes_x', type=int, default=8,
                     help ="Number of nodes in one 'False' direction")
parser.add_argument('--n_nodes_y', type=int, default=8,
                     help ="Number of nodes in other 'False' direction")
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
vel = args.vel

# Calculate box length
vol = args.N / args.rho
l = np.cbrt(vol)

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

system.lees_edwards.protocol = lees_edwards.LinearShear(
        shear_velocity = vel,
        shear_direction = 0,
        shear_plane_normal = 1)
#system.integrator.run(100000)

# Set up of correlators for positions and velocity
dso = espressomd.observables.DPDStress()

# Open txt-files to save non-correlated results
dpd_stress = open("dpd_stress.txt","w")
old_stress = open("old_stress.txt","w")
kin_stress = open("kin_stress.txt","w")
temp = open("temp.txt","w")
ener = open("energy.txt","w")

# Sampling + write non-correlated results in txt-files
for i in range(args.samples):

    dpd_stress.write(str(dso.calculate()[0]) + ";" +
                     str(dso.calculate()[1]) + ";" +
                     str(dso.calculate()[2]) + ";" +
                     str(dso.calculate()[3]) + ";" +
                     str(dso.calculate()[4]) + ";" +
                     str(dso.calculate()[5]) + ";" +
                     str(dso.calculate()[6]) + ";" +
                     str(dso.calculate()[7]) + ";" +
                     str(dso.calculate()[8]) + "\n")
    dpd_stress.flush()

    stress = system.analysis.stress_tensor()
    energy = system.analysis.energy()
	
    old_stress.write(str(stress['total'][0,1]) + "\n")
    old_stress.flush()

    kin_stress.write(str(stress['kinetic'][0,1]) + "\n")
    kin_stress.flush()

    temp.write(str(energy['kinetic']) + "\n")
    temp.flush()

    ener.write(str(energy['total']) + "\n")
    ener.flush()

    print("Step:", i, flush=True)
    system.integrator.run(iterations)

#Close all the txt-files
dpd_stress.close()
old_stress.close()
kin_stress.close()
temp.close()
ener.close()
