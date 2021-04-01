# Lees Edwards boundary conditions
# Companion data and scripts

This repository contains extra information for the publication *Lees-Edwards boundary conditions for translation invariant shear flow: implementation and transport properties* by Sebastian Bindgen, Erin Koos, Florian Weik, Rudolf Weeber, and Pierre de Buyl.

A preprint of the article is available at *intert link here*.

## Hardware

All simulations were performed in the Genius Cluster of KU euven and the University of Hasselt.
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
A script to build Espresso on the Genius cluster is provided in `lees_edwards_implementation/build_config/build_es.sh`. The necessary configuration file is available in `lees_edwards_implementation/build_config/myconfig.hpp`.

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
