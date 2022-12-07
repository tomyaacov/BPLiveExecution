from examples.sokoban import init_bprogram, map_settings, pygame_settings
from dfs.dfs_bprogram import DFSBProgram
from algorithms.spot_solver import SpotSolver
from algorithms.value_iteration import ValueIteration
from algorithms.q_learning import *
from bp.bp_env import BPEnv
import pandas as pd
from examples.sokoban_pygame.sokoban_maps import maps

eval_runs = 10
eval_run_max_length = 10
num_episodes = [1_000, 10_000, 10_000, 10_000]
episode_timeout = [100, 100, 100, 100]



results = pd.DataFrame(columns=["map",
                                "DFS time",
                                "spot time",
                                "spot success",
                                "value iteration time",
                                "value iteration success",
                                # "qlearning time",
                                # "qlearning success"
                                ])

for i in maps:
    map_settings["map"] = maps[i]
    pygame_settings["display"] = False
    dfs = DFSBProgram(init_bprogram)
    (init, states_dict, events), dfs_time = dfs.run()
    states = list(states_dict)
    graph = DFSBProgram.save_graph(init, states, "output/graph_sokoban_" + str(i) + ".dot")

    spot_ess, spot_time = SpotSolver.compute_ess(states_dict, events)
    spot_success_rate = SpotSolver.evaluate(spot_ess, init_bprogram, eval_runs, eval_run_max_length)


    value_iteration_ess, value_iteration_time = ValueIteration.compute_ess(states, 1, 0.001)
    value_iteration_success_rate = ValueIteration.evaluate(value_iteration_ess, init_bprogram, eval_runs,
                                                           eval_run_max_length)

    # env = BPEnv()
    # env.set_bprogram_generator(init_bprogram)
    # (qlearning_ess, Q, q_results, episodes, mean_reward), qlearning_time = QLearning.compute_ess(env,
    #                                                                                              num_episodes[i],
    #                                                                                              0.1,
    #                                                                                              0.99,
    #                                                                                              False,
    #                                                                                              5,
    #                                                                                              glie_10,
    #                                                                                              episode_timeout[i])
    #
    # qlearning_success_rate = ValueIteration.evaluate(qlearning_ess, init_bprogram, eval_runs, eval_run_max_length)

    results = results.append({"map": int(i),
                              "DFS time": dfs_time,
                              "spot time": spot_time,
                              "spot success": spot_success_rate,
                              "value iteration time": value_iteration_time,
                              "value iteration success": value_iteration_success_rate,
                              # "qlearning time": qlearning_time,
                              # "qlearning success": qlearning_success_rate
                              },
                             ignore_index=True)
results.to_csv("output/sokoban_results.csv", index=False)