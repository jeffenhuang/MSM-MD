# MSM-MD
# Author: Jianfeng Huang 
# SEBE, Glasgow Caledonian University, Unitied Kingdom, G40BA
# 2018 Nov

This repository is a Markov State Model integrated with Molecular Dynamics (MSM-MD) simulation codes which includes 
1 shell scripts run on HPC (Archie-WeST), file extension *.sh
2 LAMMPS codes for nickel superalloy fatigue microstates initiation, in.*.msm, *.alloy
3 python codes that automatically execute LAMMPS simulation programme, *.py
4 and Matlab codes for MSM simulation, *.m

The MD codes run on LAMMPS (LAMMPS 64-bit 20170127) which assosiated with the change of polycrystalline modelling of FCC structure, dislocation recogonition, and Peierls-Nabarro dislocation energy potential field which in repository: 

https://github.com/jeffenhuang/lammps.git

The simulation content includes:
(a), a parallel computing of nickel superalloys fatigue response microstates under a temperature of 893 K with NPT ensemble;
(b), a serial computing, same as (a) does;
(c), MSM simulation of fatigue process on matlab with the MD simulation result of the microstates.

