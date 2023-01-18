from examples.sokoban import init_bprogram, map_settings, pygame_settings
from algorithms.spot_solver import SpotSolver
from algorithms.value_iteration import ValueIteration
from examples.sokoban_pygame.sokoban_maps import maps
import sys
import pydot
from dfs.dfs_node import DFSNode

def transform_graph(g):
    visited = {}
    nodes_map = {}
    total_events = set()
    for s in g.get_nodes():
        try:
            n = DFSNode(tuple(), s.get_id().strip('"'))
        except Exception:
            print(s.get_name())
            continue
        must_finish_str = s.get_label("hot").strip('"').split(",")
        must_finish_dict = dict([(must_finish_str[2*i], must_finish_str[2*i+1] == "1") for i in range(len(must_finish_str)//2)])
        n.must_finish = [must_finish_dict["box" + str(x)] for x in range(len(must_finish_dict))]
        visited[n] = int(s.get_name())
        nodes_map[s.get_name()] = n
    for e in g.get_edge_list():
        l = e.get_label().strip('"')
        nodes_map[e.get_source()].transitions[l] = nodes_map[e.get_destination()]
        nodes_map[e.get_source()].rewards[l] = int(not any(nodes_map[e.get_destination()].must_finish)) - \
                                               int(not any(nodes_map[e.get_source()].must_finish))
        total_events.add(l)

    return nodes_map["0"], visited, total_events, None


eval_runs = 10
eval_run_max_length = 10

if len(sys.argv) > 1:
    i = int(sys.argv[1])
else:
    eval_runs = 10
    eval_run_max_length = 100
    i = 2
map_settings["map"] = maps[i]
pygame_settings["display"] = False

graphs = pydot.graph_from_dot_file("output/sokoban_cobp_" + str(i) + ".dot")
graph = graphs[0]
init, states_dict, events, liveness_bthreads = transform_graph(graph)

states = list(states_dict)
print("graph size:", len(states))
print("graph edges:", sum([len(s.transitions) for s in states]))

spot_ess, spot_time = SpotSolver.compute_ess(states_dict, events, liveness_bthreads, per_bthread=False)
spot_success_rate = SpotSolver.evaluate(spot_ess, init_bprogram, eval_runs, eval_run_max_length)
print("spot_time:", spot_time)
print("spot_success_rate:", spot_success_rate)

value_iteration_ess, value_iteration_time = ValueIteration.compute_ess(states, states_dict, 0.99, 0.01, liveness_bthreads, per_bthread=False)
print("value_iteration_time:", value_iteration_time)
value_iteration_ess.spot_ess = spot_ess
value_iteration_ess.spot_ess.reset_to_initial()
value_iteration_success_rate = ValueIteration.evaluate(value_iteration_ess, init_bprogram, eval_runs, eval_run_max_length)
print("value_iteration_success_rate:", value_iteration_success_rate)


