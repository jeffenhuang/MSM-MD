############################################################################
# File Name: run_serial.py
# Description: This file is python script to run the lammps in a serial 
#              model
# Command line: py run_serial.py
#
############################################################################

############################################################################
#
# History
#
# Date        Author           Description
# 27/07/2017  Jianfeng Huang   First submit to Github
#
############################################################################

#!/usr/local/bin/python
#Authors: Laalitha Liyanage, Sungho Kim
#Purpose: Calculate material properties of fcc system

import os
import re
import sys,getopt
import math
import random
import shutil
#import numpy as np

import logging

# 
logging.basicConfig(filename='run_serial.log', level=logging.INFO)

logging.debug('debug message')
logging.info('info message')
logging.warn('warn message')
logging.error('error message')
logging.critical('critical message')

#========================================================================================================================================
#--------------------------------------------------Default setting-----------------------------------------------------------------------
#========================================================================================================================================

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
    executable = "/users/rmb15111/bin/lmp_serial"
elif platform == "darwin":
    # OS X
    executable = ""
elif platform == "win32":
    # Windows...
    executable = "mpiexec -n "+str(arg(sys.argv[1:]))+" lmp_mpi -sf omp -pk omp 4"
    #executable = "lmp_serial"
    print(executable)
    
#Percentage strain and no. of points for elastic constant calculation
perc = .1
nt = 6

#The parameters
rand0 = random.random()        # Random number in range [0, 1)
rand1 = 2*rand0 - 1            # Random number in range [-1, 1)

#1 deformation rate, the deformation rate is 0.002 which is a threshold for generation of hysteresis loop during MD simulation
ratelist = [0.004]
#rate = 0.002+0.001*rand1       # The deformation rate at the range of [0.001,0.003)

#2 temperature
templist = [873]
#temp = 773+3*rand1             # The temperature is at 773k the range of [770,776)

#3 the hight of exclusive atom with bond
pb = 9

#4 the unbond block center position to the yhi of the simulation box parameter list
positionxlist=range(299,300)
positionylist=range(149,150)

#Length of vacuum for surface energy calculation
vacuum =  15.0
load = "load"
relax = "relax"
num = 1
tensile = "t"
compress = "c"
marginx = 275
marginy = 125

def FirstHalfCycle(i,pox,j,poy,temp,rate):
    os.system("%s -in in.init.msm -v temp %d -v pbx %d -v pox %d -v pby %d -v poy %d"%(executable, temp, i, pox,j,poy))
    os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,1,tensile, temp,rate))
    os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,1,tensile, temp,rate))
    os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,2,tensile, temp,rate))
    os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,2,tensile, temp,rate))
    os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,3,tensile, temp,rate))
    
def CycleLoad(startLoop, endLoop,rate,temp):
    for i in range(startLoop, endLoop):
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,i*8+3,compress, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,i*8+4,compress, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,i*8+4,compress, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,i*8+5,compress, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,i*8+5,compress, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,i*8+6,compress, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,i*8+6,compress, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,i*8+7,compress, temp,rate))

        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,i*8+7,tensile, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,i*8+8,tensile, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,i*8+8,tensile, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,i*8+9,tensile, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,i*8+9,tensile, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,i*8+10,tensile, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,relax,i*8+10,tensile, temp,rate))
        os.system("%s -in in.load.msm -v stype %s -v num %d -v lt %s -v temp %d -v rate %f"%(executable,load,i*8+11,tensile, temp,rate))

def CheckDir():
    dirs = ["./restart", "./dump", "./log", "./output", "./init", "./config"]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def main():
    try:
        maindir = "./data"
        filetocopy = ["in.init.msm", "in.load.msm", "Mishin-Ni-Al-2009.eam.alloy"]
        for rate in ratelist:
            inrate = rate+0.0001*rand1
            for temp in templist:
                intemp = temp+3*rand1
                for pox in positionxlist:
                    #for i in range(pox-marginx, pox):
                        i=pox-marginx
                        for poy in positionylist:
                            #for j in range(poy-marginy,poy):
                                j=poy-marginy
                                dir=maindir+'_'+str(rate)+'_'+str(temp)+'_'+str(pox)+'_'+str(i)+'_'+str(poy)+'_'+str(j)
                                print(dir)
                                if not os.path.exists(dir):
                                    os.makedirs(dir)
                                    for file in filetocopy:
                                        shutil.copy2(file, dir)
                                    os.chdir(dir)
                                    CheckDir()
                                    FirstHalfCycle(i,pox,j,poy, intemp,inrate)
                                    CycleLoad(0,6,inrate,intemp)
                                    os.chdir("..")
    except:
       print("run.py -n <ncore>")
       sys.exit(2)                                    
                                    



if __name__ == "__main__":
   main()
            

