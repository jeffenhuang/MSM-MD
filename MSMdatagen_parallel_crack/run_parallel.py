############################################################################
# File Name: run_parallel.py
# Description: This file is python script to run the lammps in a parallel 
#              model
# Command line: py run_parallel.py -n [num core]
#
############################################################################

############################################################################
#
# History
#
# Date        Author           Description
# 27/07/2017  Jianfeng Huang   First submit to Github
# 27/07/2017  Jianfeng Huang   Change the position list-positionxlist and positionylist
#                              and add logging info
# 30/07/2017  Jianfeng Huang   Modified positionlist and parameters.
# 11/08/2017  Jianfeng Huang   Revise for flexible cycle nodes
############################################################################

#!/usr/local/bin/python
#Authors: Laalitha Liyanage, Sungho Kim
#Purpose: Calculate material properties of fcc systemls

import logging
import os
import re
import sys,getopt
import math
import random
import shutil
#import numpy
#========================================================================================================================================
#--------------------------------------------------Default setting-----------------------------------------------------------------------
#========================================================================================================================================
logging.basicConfig(filename='run_parallel.log',level=logging.DEBUG)
logging.info('Job Start...')
datafile="datafile"

# Default lattice parameter
a=3.51
nty=1

#Paramters of interatomic potential
pair_style = "eam/alloy"
pair_coeff = "* * Fe.eam.alloy Fe"

#Constants to convert units
unit_conversion1 = 160.217646 # 1 eV/A^3 = 1.60217646E-19 / 1E-30 Pa = 160.217646 GPa
unit_conversion2 = 16021.765 #1 eV/A^3 to mJ/m^2

def arg(argv):
    np = ''
    try:
       opts, args = getopt.getopt(argv,"hn:",["ncore="])
    except getopt.GetoptError:
       print("run.py -n <ncore>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print("run.py -n <ncore>")
          sys.exit()
       elif opt in ("-n", "--ncore"):
          np = arg
    return np

#Command to execute LAMMPS
from sys import platform
if platform == "linux" or platform == "linux2":
    # linux
    executable = "mpirun -np "+str(arg(sys.argv[1:]))+" /users/rmb15111/bin/lammps/src/lmp_mpi"
elif platform == "darwin":
    # OS X
    executable = ""
elif platform == "win32":
    # Windows...
    executable = "mpiexec -n "+str(arg(sys.argv[1:]))+" lmp_mpi -sf omp -pk omp 4"
    #executable = "lmp_serial"

inputfile1 = "in.crack.init.msm"
inputfile2 = "in.crack.load.msm"

logging.info('executable command is: %s', executable)

#Percentage strain and no. of points for elastic constant calculation
perc = .1
nt = 6

#The parameters
rand0 = random.random()        # Random number in range [0, 1)
rand1 = 2*rand0 - 1            # Random number in range [-1, 1)

#1 deformation rate, the deformation rate is 0.002 which is a threshold for generation of hysteresis loop during MD simulation
ratelist = [0.006]
#rate = 0.002+0.001*rand1       # The deformation rate at the range of [0.001,0.003)

#2 temperature
templist = [973]
#temp = 773+3*rand1             # The temperature is at 773k the range of [770,776)

#3 the hight of exclusive atom with bond
pb = 9

#4 the unbond block center position to the yhi of the simulation box parameter list
positionxlist=[100]
positionylist=[15,20,25]

#5 Strain list
#Strain list is the maximum strain for tensile or compress
strainlist=[0.005,0.01,0.015]

#Length of vacuum for surface energy calculation
vacuum =  15.0
load = "load"
relax = "relax"
num = 1
tensile = "t"
compress = "c"
marginx = 85
marginy = [0,5,10]

TotalCycle=6;
StepsInCycle=12;

def GetStrain(strain,index, stepInCycle):
    indexInCycle=index%stepInCycle
    if indexInCycle==0:
        indexInCycle=stepInCycle
        
    quartStep=int(stepInCycle/4)
    
    if indexInCycle<=quartStep:
        return strain/quartStep/(1+(indexInCycle-1)*strain/quartStep)
    elif indexInCycle<=3*quartStep:
        return strain/quartStep/(1+(2*quartStep+1-indexInCycle)*strain/quartStep)
    else:
        return strain/quartStep/(1-(4*quartStep+1-indexInCycle)*strain/quartStep)

def Initial(i,pox,j,poy,temp):
    os.system("%s -in %s -v temp %d -v pbx %d -v pox %d -v pby %d -v poy %d"%(executable, inputfile1, temp, i, pox,j,poy))

def OneStep(loadtype, stepNumber, temp,rate,strain):
    stepstrain=GetStrain(strain, stepNumber, StepsInCycle)
    print("***********Strain for step %d is %f"%(stepstrain, stepstrain))
    os.system("%s -in %s -v stype %s -v num %d -v lt %s -v temp %d -v rate %f -v strain %f"%(executable,inputfile2,load,stepNumber,loadtype, temp,rate,stepstrain))
    os.system("%s -in %s -v stype %s -v num %d -v lt %s -v temp %d -v rate %f -v strain %f"%(executable,inputfile2,relax,stepNumber,loadtype, temp,rate,stepstrain))

def OneCycle(numCycle, numSteps, temp, rate, strain):
    #step forward
    
    quartStep=int(numSteps/4)
    for i in range(numCycle*numSteps+1, numCycle*numSteps+quartStep+1):
        OneStep(tensile, i, temp, rate, strain)
    
    for j in range(numCycle*numSteps+quartStep+1, numCycle*numSteps+3*quartStep+1):
        OneStep(compress, j, temp, rate, strain)
        
    for k in range(numCycle*numSteps+3*quartStep+1, (numCycle+1)*numSteps+1):
        OneStep(tensile, k, temp, rate, strain)

def FatigueLoad(totalCycle, numSteps, temp, rate, strain):
    for i in range(0, totalCycle):
        OneCycle(i, numSteps, temp, rate, strain)

def CheckDir():
    dirs = ["./restart", "./dump", "./log", "./output", "./init", "./config"]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def main():
    try:
        maindir = "./data"
        filetocopy = ["in.crack.init.msm", "in.crack.load.msm", "Mishin-Ni-Al-2009.eam.alloy"]
        for rate in ratelist:
            inrate = rate+0.0001*rand1
            for temp in templist:
                intemp = temp+3*rand1
                for pox in positionxlist:
                    #for i in range(pox-marginx, pox):
                        i=pox-marginx
                        for poy in positionylist:
                            for my in marginy: #range(poy-marginy,poy):
                                for instrain in strainlist:
                                    j=poy-my
                                    dir=maindir+'_'+str(inrate)+'_'+str(intemp)+'_'+str(pox)+'_'+str(i)+'_'+str(poy)+'_'+str(j)+'_'+str(instrain)
                                    print(dir)
                                    if not os.path.exists(dir):
                                        os.makedirs(dir)

                                    for file in filetocopy:
                                        shutil.copy2(file, dir)
                                    os.chdir(dir)
                                    CheckDir()
                                    Initial(i,pox,j,poy, intemp)
                                    FatigueLoad(TotalCycle,StepsInCycle, intemp,inrate, instrain)
                                    os.chdir("..")
    except:
       print("run.py -n <ncore>")
       print(sys.exc_info())
       sys.exit(2)                                    
                                    



if __name__ == "__main__":
   main()
            

