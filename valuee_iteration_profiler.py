# from examples.sokoban import init_bprogram, map_settings, pygame_settings
# from dfs.dfs_bprogram import DFSBProgram
from algorithms.value_iteration import ValueIteration

# from examples.sokoban_pygame.sokoban_maps import maps

# map_settings["map"] = maps[1]
# pygame_settings["display"] = False
# dfs = DFSBProgram(init_bprogram)
# (init, states_dict, events), dfs_time = dfs.run()
# states = list(states_dict)
import pickle
# pickle.dump( states, open("/Users/tomyaacov/Downloads/s.pickle", "wb" ) )
states = pickle.load( open( "/Users/tomyaacov/Downloads/s.pickle", "rb" ) )
value_iteration_ess, value_iteration_time = ValueIteration.compute_ess(states, 1, 0.001)
