# BPLiveExecution
Code appendix for the paper "Adding Liveness to Executable
Specifications"

* *Note: the project requires Conda*

## Running the code:
## Installation

1. Clone the project :

```shell
git clone https://github.com/tomyaacov/BPLiveExecution.git
```


2. Create a virtual environment and activate it:

```shell
cd BPLiveExecution
conda create --name BPLiveExecution python=3.7 --file requirements.txt
source activate BPLiveExecution
```


## Usage
*IMPORTANT: The evaluation requires a lot of RAM.
We recommend using a machine with at least 64GB of RAM.*

### Run parameters
* map name - the name of the map to run on. one of the following:
    * map_6_8_3
    * map_12_11_1
    * map_13_12_1
    * map_9_10_2
    * map_7_7_2
    * map_7_7_3
    * map_11_9_2
    * map_6_6_3
    * map_6_7_3
    * map_8_8_2
    * map_8_2
    * map_10_9_2
    * map_9_7_2_
    * map_9_7_2
    * map_10_7_2
    * map_8_9_2
    * map_8_7_2
    * map_9_8_2
    * map_9_9_2
    * map_11_8_2
* single/multiple requirements - whether to run the single ("0") or multiple ("1") liveness requirements scenario.

### Executing the code
An example of running the code on the map_6_8_3 map with the single liveness requirement scenario is as follows:
```shell
python main_sokoban.py "map_6_8_3" "0"
```

### Output
The code outputs the runtime of the automata-based and MDP-based methods described in the paper. Additionally, it evaluates the robustness of the MDP-based solution, as described in th paper (requires a lot of RAM).