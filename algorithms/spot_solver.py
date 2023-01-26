from bp.spot_ess import SpotESS
import spot
import buddy
from utils import timer

spot.setup()

class SpotSolver:

    @staticmethod
    @timer
    def compute_ess(states_dict, events, liveness_bthreads, per_bthread=True):
        state_liveness = {}
        if per_bthread:
            state_liveness[0] = SpotSolver.solve_game_per_bthread(states_dict, events)
            return SpotESS(states_dict, state_liveness)
        else:
            state_liveness[0] = SpotSolver.solve_game(states_dict, events)
            return SpotESS(states_dict, state_liveness)


    @staticmethod
    def solve_game(states_dict, events):
        states = list(states_dict)
        bdict = spot.make_bdd_dict()
        game = spot.make_twa_graph(bdict)
        dict_bdd = {}
        for e in events:
            dict_bdd[e] = buddy.bdd_ithvar(game.register_ap(e))

        game.new_states(len(states_dict))
        for s1, id1 in states_dict.items():
            for e, s2 in s1.transitions.items():
                if any(s1.must_finish):
                    game.new_edge(id1, states_dict[s2], dict_bdd[e])
                else:
                    game.new_edge(id1, states_dict[s2], dict_bdd[e], [0])

        game.set_init_state(0)
        game.set_buchi()
        game.prop_state_acc(True)
        spot.set_state_players(game, [True] * len(states))

        _, t = SpotSolver.run_alg(game)
        print(t)

        state_liveness = {}
        for i, b in enumerate(spot.get_state_winners(game)):
            state_liveness[i] = b
        return state_liveness

    @staticmethod
    def solve_game_per_bthread(states_dict, events):
        states = list(states_dict)
        bdict = spot.make_bdd_dict()
        game = spot.make_twa_graph(bdict)
        dict_bdd = {}
        for e in events:
            dict_bdd[e] = buddy.bdd_ithvar(game.register_ap(e))

        game.new_states(len(states_dict))
        for s1, id1 in states_dict.items():
            for e, s2 in s1.transitions.items():
                l = [i for i in range(len(s2.must_finish)) if not s2.must_finish[i]]
                game.new_edge(id1, states_dict[s2], dict_bdd[e], l)

        game.set_init_state(0)
        game.set_generalized_buchi(len(s1.must_finish))
        spot.set_state_players(game, [True] * len(states))

        p_game, t = SpotSolver.run_alg_per_bt(game, states)
        print(t)


        state_liveness = {}
        try:
            orig = list(p_game.get_original_states())
        except Exception:
            orig = list(range(len(spot.get_state_winners(p_game))))
        for i, b in enumerate(spot.get_state_winners(p_game)):
            state_liveness[orig[i]] = b
        return state_liveness

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

    @staticmethod
    @timer
    def run_alg(game):
        spot.solve_game(game)

    @staticmethod
    @timer
    def run_alg_per_bt(game, states):
        p_game = spot.partial_degeneralize(game)
        try:
            spot.set_state_players(p_game, [True] * len(p_game.get_original_states()))
        except Exception:
            spot.set_state_players(p_game, [True] * len(states))
        spot.solve_game(p_game)
        # p_game = spot.parity_type_to_parity(game)
        # if p_game is None:
        #     pass
        # spot.set_state_players(p_game, [True] * len(states))
        # spot.solve_parity_game(p_game)
        return p_game


