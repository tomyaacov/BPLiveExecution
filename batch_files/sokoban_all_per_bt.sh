#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
##SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name sokoban_all_per_bt ### name of the job. replace my_job with your desired job name
#SBATCH --output sokoban_all_per_bt.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=250G ### total amount of RAM
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32 ##. // max 128

### Start you code below ####
module load anaconda ### load anaconda module
source activate BPLiveExecution

echo "map_6_8_3"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_6_8_3" "1"

echo "map_12_11_1"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_12_11_1" "1"

echo "map_13_12_1"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_13_12_1" "1"

echo "map_9_10_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_9_10_2" "1"

echo "map_7_9_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_7_9_2" "1"

echo "map_7_7_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_7_7_2" "1"

echo "map_7_7_3"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_7_7_3" "1"

echo "map_11_9_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_11_9_2" "1"

echo "map_6_6_3"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_6_6_3" "1"

echo "map_6_7_3"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_6_7_3" "1"

echo "map_8_8_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_8_8_2" "1"

echo "map_8_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_8_2" "1"

echo "map_10_9_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_10_9_2" "1"

echo "map_9_7_2_"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_9_7_2_" "1"

echo "map_9_7_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_9_7_2" "1"

echo "map_10_7_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_10_7_2" "1"

echo "map_8_9_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_8_9_2" "1"

echo "map_8_7_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_8_7_2" "1"

echo "map_9_8_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_9_8_2" "1"

echo "map_7_6_3"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_7_6_3" "1"

echo "map_9_9_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_9_9_2" "1"

echo "map_11_8_2"
~/.conda/envs/BPLiveExecution/bin/python ~/repos/BPLiveExecution/main_sokoban.py "map_11_8_2" "1"