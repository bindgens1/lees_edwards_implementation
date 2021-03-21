"""
Determine the diffusion coefficient of a DPD fluid via the velocity autocorrelation and via the MSD of the DPD particles.
"""

import espressomd
from espressomd.accumulators import Correlator
from espressomd.observables import ParticlePositions, ParticleVelocities

import espressomd.lees_edwards as lees_edwards

import numpy as np

from scipy import integrate
from scipy.optimize import curve_fit

from espressomd.io.writer import h5md

import argparse

import json

def msd_fit(t, D):
    return 6.0 * D * t

def vacf_fit(t, p0, p1):
    return p0 * (1-np.exp(-p1*t))

# Set up of parameters

# Give in parameters
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--kT', type=float, default=1.0,
                     help="temperature")
parser.add_argument('--rcut', type=float, default=1.0,
                     help="DPD fluid particle diameter")
parser.add_argument('--aij', type=float, default=25,
                     help="DPD fluid repulsion parameter ")
parser.add_argument('--gamma', type=float, default=4.5,
                     help="DPD thermostat friction")
parser.add_argument('--rho', type=float, default=3,
                     help="DPD fluid density")
parser.add_argument('--samples', type=int, default=1000,
                     help="number of sampling loops")
parser.add_argument('--N', type=int, default=10000,
                     help="number of DPD particles")
parser.add_argument('--savedata', action='store_true',
                     help ="write the data to a data base")
args = parser.parse_args()

# Give parameters simpler names
gamma = args.gamma
kT = args.kT
r_cut = args.rcut
rho = args.rho
n_part = args.N
F_max = args.aij

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
system.integrator.run(10000)

# Set up of correlators for positions and velocity
pos_obs = ParticlePositions(ids=(np.arange(n_part)))
vel_obs = ParticleVelocities(ids=(np.arange(n_part)))

c_pos = Correlator(obs1=pos_obs, tau_lin=16, tau_max=10000., delta_N=10,
                   corr_operation="square_distance_componentwise",
                   compress1="discard1")
c_vel = Correlator(obs1=vel_obs, tau_lin=16, tau_max=10., delta_N=1,
                   corr_operation="scalar_product", compress1="discard1")

system.auto_update_accumulators.add(c_pos)
system.auto_update_accumulators.add(c_vel)

# Open h5md file
h5 = h5md.H5md(filename="./trajectory.h5", write_pos=True, write_lees_edwards_offset = True, write_vel = True, write_ordered=True)

for i in range(args.samples):
    print(i, flush=True)
    h5.write()
    system.integrator.run(5000)

#Close all the files
h5.close()

# Finalizing and results of correlators
c_pos.finalize()
c_vel.finalize()
vacf = c_vel.result()
msd = c_pos.result()

#Saving the results of correlators in numpy-files
np.save('dpd_sample_msd.npy', msd)
np.save('dpd_sample_vacf.npy', vacf)

# Integral of vacf via Green-Kubo
# D= 1/3 int_0^infty <v(t_0)v(t_0+t)> dt
I = 1. / 3. * integrate.cumtrapz(vacf[:, 2], vacf[:, 0], initial=0) / n_part
popt1, pcov1 = curve_fit(vacf_fit, vacf[:,0], I, sigma = 1./np.sqrt(vacf[:, 1]))

# Fit MSD to analytical solution
# <x(t_0)x(t_0+t)> = 6 * D * t
popt2, pcov2 = curve_fit(msd_fit, msd[:, 0], msd[:, 2]+msd[:, 3]+msd[:, 4], sigma = 1./np.sqrt(msd[:, 1]))

# Printing the results
print("Diffusion coefficient form VACF:", popt1[0])
print("Diffusion coefficient from MSD:", popt2[0])

# Saving the data in json-file

if args.savedata == True:

    data = args.__dict__
    data['Diff coeff VACF'] = popt1[0]
    data['Diff coeff MSD'] = popt2[0]
    print(data)

    with open('diffcoeff.json', 'a') as f:
       json.dump(data, f, indent=4)
