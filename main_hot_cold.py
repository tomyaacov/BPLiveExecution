from examples.hot_cold import init_bprogram, params
from dfs.dfs_bprogram import DFSBProgram
from algorithms.spot_solver import SpotSolver
from algorithms.value_iteration import ValueIteration
from algorithms.q_learning import *
from bp.bp_env import BPEnv
import pandas as pd


n_sizes = [5, 10, 15, 20, 25, 30, 35, 40, 50]
num_episodes = [100]*len(n_sizes)
episode_timeout = [x*4 for x in n_sizes]
eval_runs = [100]*len(n_sizes)
eval_run_max_length = [x*4 for x in n_sizes]

results = pd.DataFrame(columns=["N",
                                "DFS time",
                                "spot time",
                                "spot success",
                                "value iteration time",
                                "value iteration success",
                                # "qlearning time",
                                # "qlearning success"
                                ])

for i, N in enumerate(n_sizes):
    params["n"] = N
    dfs = DFSBProgram(init_bprogram)
    (init, states_dict, events, liveness_bthreads), dfs_time = dfs.run()
    states = list(states_dict)
    graph = DFSBProgram.save_graph(init, states, "output/graph_hot_cold_" + str(i) + ".dot")

    spot_ess, spot_time = SpotSolver.compute_ess(states_dict, events, liveness_bthreads)
    spot_success_rate = SpotSolver.evaluate(spot_ess, init_bprogram, eval_runs[i], eval_run_max_length[i])

    value_iteration_ess, value_iteration_time = ValueIteration.compute_ess(states, states_dict, 0.99, 0.1, liveness_bthreads)
    value_iteration_ess.spot_ess = spot_ess
    value_iteration_ess.spot_ess.reset_to_initial()
    value_iteration_success_rate = ValueIteration.evaluate(value_iteration_ess, init_bprogram, eval_runs[i], eval_run_max_length[i])

    # env = BPEnv()
    # env.set_bprogram_generator(init_bprogram)
    # (qlearning_ess, Q, q_results, episodes, mean_reward), qlearning_time = QLearning.compute_ess(env,
    #                                                                                            num_episodes[i],
    #                                                                                            0.1,
    #                                                                                            0.99,
    #                                                                                            False,
    #                                                                                            5,
    #                                                                                            glie_10,
    #                                                                                            episode_timeout[i])
    # qlearning_success_rate = ValueIteration.evaluate(qlearning_ess, init_bprogram, eval_runs, eval_run_max_length)

    results = results.append({"N": int(N),
                              "DFS time": dfs_time,
                              "spot time": spot_time,
                              "spot success": spot_success_rate,
                              "value iteration time": value_iteration_time,
                              "value iteration success": value_iteration_success_rate,
                              # "qlearning time": qlearning_time,
                              # "qlearning success": qlearning_success_rate
                              },
                             ignore_index=True)


results.to_csv("output/_hot_cold_results5.csv", index=False)