# Lees Edwards boundary conditions - Companion data and scripts

This repository contains extra information for the publication *Lees-Edwards boundary conditions for translation invariant shear flow: implementation and transport properties* by Sebastian Bindgen, Erin Koos, Florian Weik, Rudolf Weeber, and Pierre de Buyl.

A preprint of the article is available at *insert link here*.

## Hardware

All simulations were performed in the Genius Cluster of KU Leuven and the University of Hasselt.
The hardware specifications are summarized with the following command-line programs:

```bash
user@tier2-p-login-2 ~ $ uname -mosv
Linux #1 SMP Fri Dec 18 16:34:56 UTC 2020 x86_64 GNU/Linux
user@tier2-p-login-2 ~ $ grep -E '(^model name|^vendor_id|^flags)' /proc/cpuinfo  | sort | uniq
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer xsave avx f16c rdrand lahf_lm abm 3dnowprefetch epb cat_l3 cdp_l3 invpcid_single intel_ppin intel_pt ssbd mba ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm mpx rdt_a avx512f avx512dq rdseed adx smap clflushopt clwb avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts pku ospke md_clear spec_ctrl intel_stibp flush_l1d
model name	: Intel(R) Xeon(R) Gold 6140 CPU @ 2.30GHz
vendor_id	: GenuineIntel
```

## Compilers and building ESPResSo

### Build script and configuration file
A script to build Espresso on the Genius cluster is provided in `build_config/build_es.sh`. The necessary configuration file is available in `build_config/myconfig.hpp`.

### Compilers

The compilers used are, for C:
```bash
user@tier2-p-login-2 ~ $ icc --version
icc (ICC) 18.0.1 20171018
Copyright (C) 1985-2017 Intel Corporation.  All rights reserved.

user@tier2-p-login-2 ~ $ mpiicc --version
icc (ICC) 18.0.1 20171018
Copyright (C) 1985-2017 Intel Corporation.  All rights reserved.

user@tier2-p-login-2 ~ $ mpiicpc --version
icpc (ICC) 18.0.1 20171018
Copyright (C) 1985-2017 Intel Corporation.  All rights reserved.

```
It is important to add `-fp-model=strict` to the `CMAKE_CXX_FLAGS` when the Intel compiler is used.

## Reproducing data

In order to reproduce the figures presented in the paper you can use the available Python script. The analysis is done with Jupyter notebooks.
Python was used in version 3.6.4 on the cluster. 

### Python scripts

1. Diffusion coefficient  
To measure the diffusion coefficient the file `diffdpp.py` is used together with the parameter file `params_dpd.csv`. The analysis can be done with the file `01-evaluate_diffusion_coeff.ipynb` and the final plot is created with `02-plot_diffusion_coefficient.ipynb`. We provide example data in the files `diffcoeff_50628659.npy`, `diffcoeff_50630218.npy`, `diffcoeff_50630219.npy` to create the plot presented in the paper (Figure 3). To go effectively over the entire range of simulation parameters `atools` is used as available here [atools](https://github.com/gjbex/atools) in order to create job arrays in place of single jobs. An example of a job script using such an array can be found in `param_sweep_dpd_compl.pbs`

2. Convergence of stress autocorrelation functions  
The script `viscdpd.py` offers a measurement of the viscosity using the autocorrelation of the stress. In the file `03-plot_acf_convergence.ipynb` we show the convergence of the integral of the autocorrelation function for the different stress contributions. One of these is presented as Figure 4 in the paper.

3. Measurements of viscosity  
The viscosity of the DPD fluid is measured with the Green-Kubo method using the script `viscdpd.py`. The file `ledpd.py` provides a script to measure the viscosity with Lees-Edwards boundary conditions. The viscosity of the DPD fluids is evaluated in `04-evaluate_viscosity_green-kubo.ipynb` using the Green-Kubo method. The notebook `05-evaluate_Lees-Edwards_viscosity.ipynb` provides an evaluation routine for viscosities measured via the Lees-Edwards method. In order to compare these two measurement methods the file `06-plot_viscosity_comparison.ipynb` can be used where a side by side comparison is shown as well as a graph with all data overlayed. The files `visc_gk.txt` and `visc_le.txt` can be used as input to plot the comparison graphs as shown in the paper as Figure 5.

4. Flow profile and mean square displacement  
The script `trajdpd.py` creates trajectory files using the h5md-format during simulations with continous shear with the velocities provided in `params_dpd_vel.csv`. The notebook `07-plot_flowprofile.ipynb` plots the flow profiles for selected shear velocites as presented as Figure 6 in the paper. The notebook `08-plot_enhanced_diffusion_lin_shear.ipynb` evaluates the contribution of the enhanced diffusion and compares the obtained result with the ones of the quiescent simulations. This is shown as Figure 7 of the paper. 
The same data for oscillatory shear flow can be generated using `trajdpd_osc.py` and the parameters (frequency and amplitude) given in `params_dpd_osc.csv`. The notebook `09-evaluate_enhanced_diffusion_osc_shear.ipynb` evaluates the trajectories and creates the files `diffcoeff_osc_x_50617507.npy`, `diffcoeff_osc_x_50620357.npy`, `diffcoeff_osc_x_50623020.npy`, `diffcoeff_osc_z_50617507.npy`, `diffcoeff_osc_z_50620357.npy`, `diffcoeff_osc_z_50623020.npy` that can be used as input for the notebook `10-plot_enhanced_diffusion_osc_shear.ipynb` to generate the final plot showing the enhanced diffusion behaviour. This corresponds to Figure 8 of the paper.
