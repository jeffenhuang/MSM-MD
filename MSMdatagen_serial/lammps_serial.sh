#  Simple serial job submission script

# Specifies  that all environment variables active within the qsub
#    utility be exported to the context of the job.
#$ -V
# Execute the job from the current working directory. Standard output and
#      standard error files will be written to this directory
#$ -cwd
#Specify  project
#$ -P huang-mdssuee.prj
# Submit to the queue called serial.q
#$ -q serial-low.q 
# Merges standard error stream with standard output
#$ -j y 
# Specifies the name of the file containing the standard output
#$ -o out.$JOB_ID 
# Add runtime indication
#$ -ac runtime="12hours"
#==============================================================

python run_serial.py
