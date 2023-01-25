from examples.sokoban_new import init_bprogram, map_settings, pygame_settings
from algorithms.spot_solver import SpotSolver
from algorithms.value_iteration import ValueIteration
from examples.sokoban_pygame.sokoban_maps import maps
import sys
import javaobj
from dfs.dfs_node import DFSNode


def transform_dict(d, per_bthread):
    visited = {}
    nodes_map = {}
    total_events = set()
    counter = 0
    for s in d:
        try:
            n = DFSNode(tuple(), str(s))
        except Exception:
            print(s)
            continue
        must_finish_str = str(d[s]["H"]).split(",")
        must_finish_dict = dict([(must_finish_str[2*i], must_finish_str[2*i+1] == "1") for i in range(len(must_finish_str)//2)])
        n.must_finish = [must_finish_dict["box" + str(x)] for x in range(len(must_finish_dict))]
        visited[n] = counter
        nodes_map[str(s)] = n
        counter += 1
    for s in d:
        for e in d[s]:
            if e == "H":
                continue
            l = str(e)
            nodes_map[str(s)].transitions[l] = nodes_map[str(d[s][e])]
            if per_bthread:
                nodes_map[str(s)].rewards[l] = sum([int(y)-int(x) for x,y in zip(nodes_map[str(d[s][e])].must_finish, nodes_map[str(s)].must_finish)])
            else:
                nodes_map[str(s)].rewards[l] = int(not any(nodes_map[str(d[s][e])].must_finish)) - \
                                               int(not any(nodes_map[str(s)].must_finish))
            total_events.add(l)
    s_to_change = [k for k, v in visited.items() if v == 0][0]
    init_s = [nodes_map[x] for x in nodes_map if x.startswith("I")][0]
    number_to_change = visited[init_s]
    visited[init_s] = 0
    visited[s_to_change] = number_to_change
    return init_s, visited, total_events, None


eval_runs = 100
eval_run_max_length = 1000

if len(sys.argv) > 1:
    i = sys.argv[1]
    PER_BT = sys.argv[2] == "1"
else:
    eval_runs = 10
    eval_run_max_length = 100
    i = "map_6_8_3"
    PER_BT = False

def format_map(file_name):
    l = []
    with open("examples/maps/" + file_name, "r") as f:
        for line in f:
            l.append(line.strip("\n"))
    return l

map_settings["map"] = format_map(i)
pygame_settings["display"] = False

with open("examples/graph_objects/sokoban_cobp_" + str(i) + ".ser", "rb") as fd:
    jobj = fd.read()
    pobj = javaobj.loads(jobj)
    init, states_dict, events, liveness_bthreads = transform_dict(pobj, PER_BT)

states = list(states_dict)
print("graph size:", len(states))
print("graph edges:", sum([len(s.transitions) for s in states]))

spot_ess, spot_time = SpotSolver.compute_ess(states_dict, events, liveness_bthreads, per_bthread=PER_BT)
#spot_success_rate = SpotSolver.evaluate(spot_ess, init_bprogram, eval_runs, eval_run_max_length)
print("spot_time:", spot_time)
#print("spot_success_rate:", spot_success_rate)

value_iteration_ess, value_iteration_time = ValueIteration.compute_ess(states, states_dict, events, 0.99, 0.01, per_bthread=PER_BT)
print("value_iteration_time:", value_iteration_time)
value_iteration_ess.spot_ess = spot_ess
value_iteration_ess.spot_ess.reset_to_initial()
value_iteration_success_rate = ValueIteration.evaluate(value_iteration_ess, init_bprogram, eval_runs, eval_run_max_length)
print("value_iteration_success_rate:", value_iteration_success_rate)

import numpy as np
value_iteration_ess, value_iteration_time = ValueIteration.compute_ess(states, states_dict, events, 0.999, 0.0001, per_bthread=PER_BT)
noises = [0.01, 0.02, 0.03, 0.04, 0.05]
for noise in noises:
    value_iteration_ess.spot_ess = spot_ess
    value_iteration_ess.spot_ess.reset_to_initial()
    value_iteration_ess.set_noise(lambda: np.random.normal(0, noise))
    value_iteration_success_rate = ValueIteration.evaluate(value_iteration_ess, init_bprogram, eval_runs,
                                                           eval_run_max_length)
    print("value_iteration_success_rate with noise", noise, ":", value_iteration_success_rate)

