from examples.sokoban import init_bprogram, map_settings, pygame_settings
from dfs.dfs_bprogram import DFSBProgram
from algorithms.spot_solver import SpotSolver
from algorithms.value_iteration import ValueIteration

from examples.sokoban_pygame.sokoban_maps import maps
import sys
import pickle

def save_obj(obj, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)

eval_runs = 1000
eval_run_max_length = 1000

if len(sys.argv) > 1:
    i = int(sys.argv[1])
else:
    eval_runs = 5
    eval_run_max_length = 1000
    i = 1
map_settings["map"] = maps[i]
pygame_settings["display"] = False
dfs = DFSBProgram(init_bprogram)
(init, states_dict, events, liveness_bthreads), dfs_time = dfs.run()
print("dfs_time:", dfs_time)
save_obj(states_dict, "output/states_dict_" + str(i))
states = list(states_dict)
save_obj(states, "output/states_" + str(i))
print("graph size:", len(states))
print("graph edges:", sum([len(s.transitions) for s in states]))
graph = DFSBProgram.save_graph(init, states, "output/graph_sokoban_" + str(i) + ".dot")

spot_ess, spot_time = SpotSolver.compute_ess(states_dict, events, liveness_bthreads)
#spot_success_rate = SpotSolver.evaluate(spot_ess, init_bprogram, eval_runs, eval_run_max_length)
print("spot_time:", spot_time)
#print("spot_success_rate:", spot_success_rate)
save_obj(spot_ess, "output/spot_ess_" + str(i))


value_iteration_ess, value_iteration_time = ValueIteration.compute_ess(states, 0.99, 0.01, liveness_bthreads)
value_iteration_ess.spot_ess = spot_ess
value_iteration_ess.spot_ess.reset_to_initial()
value_iteration_success_rate = ValueIteration.evaluate(value_iteration_ess, init_bprogram, eval_runs,
                                                        eval_run_max_length)
save_obj(value_iteration_ess, "output/value_iteration_ess_" + str(i))
print("value_iteration_time:", value_iteration_time)
print("value_iteration_success_rate:", value_iteration_success_rate)





# from examples.sokoban import init_bprogram, map_settings, pygame_settings
# from dfs.dfs_bprogram import DFSBProgram
# from algorithms.spot_solver import SpotSolver
# from algorithms.value_iteration import ValueIteration
# from algorithms.q_learning import *
# from bp.bp_env import BPEnv
# import pandas as pd
# from examples.sokoban_pygame.sokoban_maps import maps
#
# eval_runs = 10
# eval_run_max_length = 10
# num_episodes = [1_000, 10_000, 10_000, 10_000]
# episode_timeout = [100, 100, 100, 100]
#
#
#
# results = pd.DataFrame(columns=["map",
#                                 "DFS time",
#                                 "spot time",
#                                 "spot success",
#                                 "value iteration time",
#                                 "value iteration success",
#                                 # "qlearning time",
#                                 # "qlearning success"
#                                 ])
#
# for i in maps:
#     if i > 2: break
#     map_settings["map"] = maps[i]
#     pygame_settings["display"] = False
#     dfs = DFSBProgram(init_bprogram)
#     (init, states_dict, events), dfs_time = dfs.run()
#     states = list(states_dict)
#     graph = DFSBProgram.save_graph(init, states, "output/_graph_sokoban_" + str(i) + ".dot")
#
#     spot_ess, spot_time = SpotSolver.compute_ess(states_dict, events)
#     spot_success_rate = SpotSolver.evaluate(spot_ess, init_bprogram, eval_runs, eval_run_max_length)
#
#
#     value_iteration_ess, value_iteration_time = ValueIteration.compute_ess(states, 0.99, 0.01)
#     value_iteration_success_rate = ValueIteration.evaluate(value_iteration_ess, init_bprogram, eval_runs,
#                                                            eval_run_max_length)
#
#     # env = BPEnv()
#     # env.set_bprogram_generator(init_bprogram)
#     # (qlearning_ess, Q, q_results, episodes, mean_reward), qlearning_time = QLearning.compute_ess(env,
#     #                                                                                              num_episodes[i],
#     #                                                                                              0.1,
#     #                                                                                              0.99,
#     #                                                                                              False,
#     #                                                                                              5,
#     #                                                                                              glie_10,
#     #                                                                                              episode_timeout[i])
#     #
#     # qlearning_success_rate = ValueIteration.evaluate(qlearning_ess, init_bprogram, eval_runs, eval_run_max_length)
#
#     results = results.append({"map": int(i),
#                               "DFS time": dfs_time,
#                               "spot time": spot_time,
#                               "spot success": spot_success_rate,
#                               "value iteration time": value_iteration_time,
#                               "value iteration success": value_iteration_success_rate,
#                               # "qlearning time": qlearning_time,
#                               # "qlearning success": qlearning_success_rate
#                               },
#                              ignore_index=True)
# results.to_csv("output/_sokoban_results.csv", index=False)