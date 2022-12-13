from bp.q_table_compatible_ess import QTableCompatibleESS
from utils import timer
from concurrent.futures import ThreadPoolExecutor


class ValueIteration:

    @staticmethod
    @timer
    def compute_ess(states, gamma, convergence_threshold, liveness_bthreads):
        num_of_bthreads = len(list(states[0].rewards.values())[0])
        with ThreadPoolExecutor(num_of_bthreads) as executor:
            processes = [executor.submit(ValueIteration.compute_Q_per_bthread, states, gamma, convergence_threshold, i) if i in liveness_bthreads
                         else executor.submit(ValueIteration.dummy_Q, states, i) for i in range(num_of_bthreads)]
            Q = dict([(i, p.result()) for i,p in enumerate(processes)])
        return QTableCompatibleESS(Q)

    @staticmethod
    def compute_Q_per_bthread(states, gamma, convergence_threshold, i):
        delta = 1
        J, _J = {}, {}
        while delta > convergence_threshold:
            _J = J
            Q = {}
            delta = 0
            for s in states[::-1]:
                Q[s.id] = {}
                for a in s.transitions:
                    Q[s.id][a] = s.rewards[a][i] + gamma * _J.get(s.transitions[a].id, 0)
                if len(Q[s.id]) > 0:
                    J[s.id] = max(Q[s.id].values())
                else:
                    J[s.id] = 0
                delta = max(delta, abs(J[s.id] - _J.get(s.id, 0)))
        return Q

    @staticmethod
    def dummy_Q(states, i):
        Q = {}
        for s in states[::-1]:
            Q[s.id] = {}
            for a in s.transitions:
                Q[s.id][a] = 0
        return Q

    @staticmethod
    def evaluate(Q_ess: QTableCompatibleESS, init_bprogram, runs, run_max_length):
        bad_runs = 0
        for i in range(runs):
            bprogram = init_bprogram()
            bprogram.event_selection_strategy = Q_ess
            bprogram.setup()
            program_finished = False
            reward = [0 for x in bprogram.tickets]
            s = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
            for j in range(run_max_length):
                event = bprogram.event_selection_strategy.select(bprogram.tickets, reward, s)
                # Finish the program if no event is selected
                if event is None:
                    bad_runs += 1
                    program_finished = True
                    break
                prev_must_finish = [x.get('must_finish', False) for x in bprogram.tickets]
                bprogram.advance_bthreads(event)
                next_must_finish = [x.get('must_finish', False) for x in bprogram.tickets]
                reward = [int(m1)-int(m2) for m1, m2 in zip(prev_must_finish, next_must_finish)]
                s = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
            Q_ess.reset_to_initial()
        return (runs - bad_runs) / runs




