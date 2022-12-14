#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
##SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name sokoban1 ### name of the job. replace my_job with your desired job name
#SBATCH --output sokoban1.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=32G ### total amount of RAM
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6 ##. You may reduce that number to 6 and get double the RAM per thread

### Start you code below ####
module load anaconda ### load anaconda module
source activate BPLiveExecution
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py 1