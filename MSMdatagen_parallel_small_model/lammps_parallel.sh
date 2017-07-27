#

export PROCS_ON_EACH_NODE=12


# ************* SGE qsub options ****************
#Export env variables and keep current working directory
#$ -V -cwd
#Select parallel environment and number of parallel queue slots (nodes)
#$ -pe mpi-verbose 8
#$ -P huang-mdssuee.prj
#Combine STDOUT/STDERR
#$ -j y
#Specify output file
#$ -o out.$JOB_ID
#Request resource reservation (reserve slots on each scheduler run until enough have been gathered to run the job
#$ -R y
#Request exclusivity of each node
#$ -ac runtime="12hours"
# ************** END SGE qsub options ************

export NCORES=`expr $PROCS_ON_EACH_NODE \* $NSLOTS`
export OMPI_MCA_btl=openib,self

export TMI_CONFIG=$MPI_HOME/etc64/tmi.conf
export I_MPI_FABRICS=shm:tmi

python run_parallel.py -n $NCORES
