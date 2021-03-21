"""
Determine the diffusion coefficient of a pure DPD fluid via the Green-Kubo relations using the stress autocorrelation function. Analysis is performed separately.
"""

import espressomd
from espressomd.accumulators import Correlator
from espressomd.observables import ParticlePositions, ParticleVelocities
from espressomd.galilei import GalileiTransform

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
parser.add_argument('--aij', type=float, default=100,
                     help="DPD fluid repulsion parameter ")
parser.add_argument('--gamma', type=float, default=4.5,
                     help="DPD thermostat friction")
parser.add_argument('--rho', type=float, default=3,
                     help="DPD fluid density")
parser.add_argument('--samples', type=int, default=500000,
                     help="number of sampling loops")
parser.add_argument('--iterations', type=int, default=10,
                     help="number of iterations per sample")
parser.add_argument('--N', type=int, default=10000,
                     help="number of DPD particles")
parser.add_argument('--savedata', action='store_true',
                     help ="write the data to a data base")
parser.add_argument('--tau_lin', type=int, default=16,
                     help ="Tau lin for all correlations")
parser.add_argument('--tau_max', type=int, default=100000,
                     help ="Tau max for all correlations")
parser.add_argument('--timestep', type=float, default=0.005,
                     help="Timestep for whole simulation")
args = parser.parse_args()

# Give parameters simpler names
gamma = args.gamma
kT = args.kT
r_cut = args.rcut
rho = args.rho
n_part = args.N
F_max = args.aij
iterations=args.iterations
tau_lin = args.tau_lin
tau_max = args.tau_max
timestep = args.timestep

# Calculate box length
vol = args.N / args.rho
l = np.cbrt(vol)

# Set up the box
system = espressomd.System(box_l=[l, l, l])
system.set_random_state_PRNG()
np.random.seed(seed=system.seed)

# Add randomly distributed DPD particles to the box
pos = system.box_l * np.random.random((n_part, 3))
system.part.add(pos=pos)

# Set up the time step, skin and thermostat
dt = timestep
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
system.integrator.run(1000000)

# Reset COM movement
g = GalileiTransform()
g.galilei_transform()

# Set up of correlators to obtain stress autocorrelation functions
dso = espressomd.observables.DPDStress()
plain_old_stress = espressomd.observables.StressTensor()

c_dpd = Correlator(obs1=dso, tau_lin=tau_lin, tau_max=tau_max, delta_N=1,
                   corr_operation="componentwise_product", compress1="discard1")
c_old = Correlator(obs1=plain_old_stress, tau_lin=tau_lin, tau_max=tau_max, delta_N=1,
                   corr_operation="componentwise_product", compress1="discard1")

system.auto_update_accumulators.add(c_dpd)
system.auto_update_accumulators.add(c_old)

# Open txt-files to save non-correlated results
dpd_stress = open("dpd_stress.txt","w")
old_stress = open("old_stress.txt","w")
kin_stress = open("kin_stress.txt","w")
temp = open("temp.txt","w")
ener = open("energy.txt","w")

# Sampling + write non-correlated results in txt-files
for i in range(args.samples):

    stress = system.analysis.stress_tensor()
    energy = system.analysis.energy()

    dpd_stress.write(str(dso.calculate()[1]) + "\n")
    dpd_stress.flush()

    old_stress.write(str(stress['total'][0,1]) + "\n")
    old_stress.flush()

    kin_stress.write(str(stress['kinetic'][0,1]) + "\n")
    kin_stress.flush()
    
    temp.write(str(energy['kinetic']) + "\n")
    temp.flush()
    
    ener.write(str(energy['total']) + "\n")
    ener.flush()

    print(i, flush=True)
    system.integrator.run(iterations)

# Finalizing and results of correlators
c_dpd.finalize()
c_old.finalize()

dpd_stress_acf = c_dpd.result()
old_stress_acf = c_old.result()

#Saving the results of correlators in numpy-files
np.save('dpd_sample_dpd_stress_acf.npy', dpd_stress_acf)
np.save('dpd_sample_old_stress_acf.npy', old_stress_acf)

# Close non-correlated stress files
dpd_stress.close()
old_stress.close()
kin_stress.close()
temp.close()
ener.close()

