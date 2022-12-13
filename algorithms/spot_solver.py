from bp.spot_ess import SpotESS
import spot
import buddy
from utils import timer
from concurrent.futures import ThreadPoolExecutor

spot.setup()

class SpotSolver:

    @staticmethod
    @timer
    def compute_ess(states_dict, events, liveness_bthreads):
        num_of_bthreads = len(list(list(states_dict.keys())[0].rewards.values())[0])
        with ThreadPoolExecutor(num_of_bthreads) as executor:
            processes = [executor.submit(SpotSolver.solve_game_per_bthread, states_dict, events, i) if i in liveness_bthreads
                         else executor.submit(SpotSolver.dummy_state_liveness, states_dict, i) for i in range(num_of_bthreads)]
            state_liveness = dict([(i, p.result()) for i, p in enumerate(processes)])
        return SpotESS(states_dict, state_liveness)

    @staticmethod
    def solve_game_per_bthread(states_dict, events, i):
        states = list(states_dict)
        bdict = spot.make_bdd_dict()
        game = spot.make_twa_graph(bdict)
        dict_bdd = {}
        for e in events:
            dict_bdd[e.name] = buddy.bdd_ithvar(game.register_ap(e.name))

        game.new_states(len(states_dict))
        for s1, id1 in states_dict.items():
            for e, s2 in s1.transitions.items():
                if any(s1.must_finish):
                    game.new_edge(id1, states_dict[s2], dict_bdd[e.name])
                else:
                    game.new_edge(id1, states_dict[s2], dict_bdd[e.name], [0])

        game.set_init_state(0)
        game.set_buchi()
        game.prop_state_acc(True)
        spot.set_state_players(game, [True] * len(states))

        spot.solve_game(game)

        state_liveness = {}
        for i, b in enumerate(spot.get_state_winners(game)):
            state_liveness[i] = b
        return state_liveness
    @staticmethod
    def dummy_state_liveness(states_dict, i):
        return dict([(i, True) for n, i in states_dict.items()])


    @staticmethod
    def evaluate(spot_ess: SpotESS, init_bprogram, runs, run_max_length):
        bad_runs = 0
        for i in range(runs):
            bprogram = init_bprogram()
            bprogram.event_selection_strategy = spot_ess
            bprogram.setup()
            program_finished = False
            for j in range(run_max_length):
                event = bprogram.next_event()
                # Finish the program if no event is selected
                if event is None:
                    bad_runs += 1
                    program_finished = True
                    break
                bprogram.advance_bthreads(event)
            if not program_finished:
                if any(bprogram.event_selection_strategy.current_state.must_finish):
                    bad_runs += 1
            spot_ess.reset_to_initial()
        return (runs - bad_runs) / runs


