#


module load compilers/intel/14.0.2
module load mpi/intel/impi/4.1.3

# ************* SGE qsub options ****************
#Export env variables and keep current working directory
#$ -V -cwd
#Select parallel environment and number of parallel queue slots (nodes)
#$ -pe multiway 96 
#$ -P huang-mdssuee.prj
#Combine STDOUT/STDERR
#$ -j y
#Specify output file
#$ -o out.$JOB_ID
#Request resource reservation (reserve slots on each scheduler run until enough have been gathered to run the job
#$ -R y
#Request exclusivity of each node
#$ -ac runtime="12hours"
#$ -l h_rt=96:00:00
# ************** END SGE qsub options ************

export NCORES=96
export TMI_CONFIG=$MPI_HOME/etc64/tmi.conf
export I_MPI_FABRICS=shm:tmi

python run_parallel.py -n $NCORES
