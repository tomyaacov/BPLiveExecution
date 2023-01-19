from bp.q_table_compatible_ess import QTableCompatibleESS
from utils import timer
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import mdptoolbox
from scipy.sparse import csr_matrix

class ValueIteration:

    @staticmethod
    def compute_ess(states, states_dict, gamma, convergence_threshold, liveness_bthreads, per_bthread=True):
        if not per_bthread:
            Q, t = ValueIteration.compute_Q(states, states_dict, gamma, convergence_threshold)
            return QTableCompatibleESS(Q, per_bthread=False), t
        num_of_bthreads = len(list(states[0].rewards.values())[0])
        with ThreadPoolExecutor(num_of_bthreads) as executor:
            processes = [executor.submit(ValueIteration.compute_Q_per_bthread, states, states_dict, gamma, convergence_threshold, i) if i in liveness_bthreads
                         else executor.submit(ValueIteration.dummy_Q, states, i) for i in range(num_of_bthreads)]
            Q = dict([(i, p.result()) for i,p in enumerate(processes)])
            t = max([x[1] for x in Q.values()])
            Q = dict([(k,v[0]) for k,v in Q.items()])
        return QTableCompatibleESS(Q), t

    @staticmethod
    def compute_Q_per_bthread(states, states_dict, gamma, convergence_threshold, bt_id):
        states_dict_flipped = dict([(v, k) for k, v in states_dict.items()])

        actions = set()
        for k in states_dict:
            for evt in k.transitions:
                actions.add(evt)
        actions = list(actions)

        S = len(states_dict_flipped) + 1

        transitions = []
        for i in range(len(actions)):
            transitions.append(csr_matrix((S, S), dtype='uint8'))
        rewards = []
        for i in range(len(actions)):
            rewards.append(csr_matrix((S, S), dtype='uint8'))

        for k, v in states_dict_flipped.items():
            for evt_i, evt in enumerate(actions):
                if evt in v.rewards:
                    rewards[evt_i][states_dict[v], states_dict[v.transitions[evt]]] = v.rewards[evt][bt_id]
                    transitions[evt_i][states_dict[v], states_dict[v.transitions[evt]]] = 1
                else:
                    rewards[actions.index(evt)][states_dict[v], S-1] = -2
                    transitions[actions.index(evt)][states_dict[v], S - 1] = 1

        for evt_i, evt in enumerate(actions):
            transitions[actions.index(evt)][S - 1, S - 1] = 1
            rewards[actions.index(evt)][S - 1, S - 1] = 0

        vi = mdptoolbox.mdp.ValueIteration(transitions, rewards, gamma, epsilon=convergence_threshold)
        _, t = ValueIteration.run_alg(vi)
        Q = np.zeros((S, len(actions)))
        V = np.array(vi.V)
        for i in range(len(V)):
            for evt_i, evt in enumerate(actions):
                next_s = np.argmax(transitions[evt_i][i])
                Q[i, evt_i] = rewards[evt_i][i, next_s] + gamma * V[next_s]

        Q_dict = {}
        for i in range(Q.shape[0]):
            if i == S - 1:
                s_id = "sink"
            else:
                s_id = states_dict_flipped[i].id
            Q_dict[s_id] = {}
            for j in range(Q.shape[1]):
                Q_dict[s_id][actions[j]] = Q[i, j]

        return Q_dict, t

    @staticmethod
    @timer
    def run_alg(vi):
        vi.run()

    @staticmethod
    def dummy_Q(states, i):
        Q = {}
        for s in states[::-1]:
            Q[s.id] = {}
            for a in s.transitions:
                Q[s.id][a] = 0
        return Q, 0

    @staticmethod
    def evaluate(Q_ess: QTableCompatibleESS, init_bprogram, runs, run_max_length):
        bad_runs = 0
        for i in range(runs):
            bprogram = init_bprogram()
            bprogram.event_selection_strategy = Q_ess
            bprogram.setup()
            s = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
            prev_must_finish = [x.get('must_finish', False) for x in bprogram.tickets]
            next_must_finish = prev_must_finish
            for j in range(run_max_length):
                event = bprogram.event_selection_strategy.select(bprogram.tickets, prev_must_finish, next_must_finish, s)
                # Finish the program if no event is selected
                if event is None:
                    bad_runs += 1
                    break
                prev_must_finish = [x.get('must_finish', False) for x in bprogram.tickets]
                bprogram.advance_bthreads(event)
                next_must_finish = [x.get('must_finish', False) for x in bprogram.tickets]
                s = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
            Q_ess.reset_to_initial()
        return (runs - bad_runs) / runs

    @staticmethod
    def compute_Q(states, states_dict, gamma, convergence_threshold):
        states_dict_flipped = dict([(v, k) for k, v in states_dict.items()])

        actions = set()
        for k in states_dict:
            for evt in k.transitions:
                actions.add(evt)
        actions = list(actions)

        S = len(states_dict_flipped) + 1

        transitions = []
        for i in range(len(actions)):
            transitions.append(csr_matrix((S, S)))
        rewards = []
        for i in range(len(actions)):
            rewards.append(csr_matrix((S, S)))

        for k, v in states_dict_flipped.items():
            for evt_i, evt in enumerate(actions):
                if evt in v.rewards:
                    rewards[evt_i][states_dict[v], states_dict[v.transitions[evt]]] = v.rewards[evt]
                    transitions[evt_i][states_dict[v], states_dict[v.transitions[evt]]] = 1
                else:
                    rewards[actions.index(evt)][states_dict[v], S-1] = -2
                    transitions[actions.index(evt)][states_dict[v], S - 1] = 1

        for evt_i, evt in enumerate(actions):
            transitions[actions.index(evt)][S - 1, S - 1] = 1
            rewards[actions.index(evt)][S - 1, S - 1] = 0

        vi = mdptoolbox.mdp.ValueIteration(transitions, rewards, gamma, epsilon=convergence_threshold)
        _, t = ValueIteration.run_alg(vi)
        Q = np.zeros((S, len(actions)))
        V = np.array(vi.V)
        for i in range(len(V)):
            for evt_i, evt in enumerate(actions):
                next_s = np.argmax(transitions[evt_i][i])
                Q[i, evt_i] = rewards[evt_i][i, next_s] + gamma * V[next_s]

        Q_dict = {}
        for i in range(Q.shape[0]):
            if i == S - 1:
                s_id = "sink"
            else:
                s_id = states_dict_flipped[i].id
            Q_dict[s_id] = {}
            for j in range(Q.shape[1]):
                Q_dict[s_id][actions[j]] = Q[i, j]

        return Q_dict, t



