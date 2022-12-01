from bp.q_table_compatible_ess import QTableCompatibleESS
from utils import timer


class ValueIteration:

    @staticmethod
    @timer
    def compute_ess(states, gamma, convergence_threshold):
        delta = 1
        J, _J = {}, {}
        for s in states:
            J[s.id] = 0
            _J[s.id] = 0
        while delta > convergence_threshold:
            _J = J
            Q = {}
            for s in states:
                Q[s.id] = {}
                for a in s.transitions:
                    Q[s.id][a] = s.rewards[a] + gamma * _J[s.transitions[a].id]
            J = {}
            delta = 0
            for s in states:
                if len(Q[s.id]) > 0:
                    J[s.id] = max(Q[s.id].values())
                else:
                    J[s.id] = 0
                delta = max(delta, abs(J[s.id] - _J[s.id]))
        return QTableCompatibleESS(Q)

    @staticmethod
    def evaluate(Q_ess: QTableCompatibleESS, init_bprogram, runs, run_max_length):
        bad_runs = 0
        for i in range(runs):
            bprogram = init_bprogram()
            bprogram.event_selection_strategy = Q_ess
            bprogram.setup()
            program_finished = False
            reward = 0
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
                reward = 0
                for k in range(len(prev_must_finish)):
                    if prev_must_finish[k] and not next_must_finish[k]:
                        reward += 1
                    if not prev_must_finish[k] and next_must_finish[k]:
                        reward -= 1
                s = "_".join([str(x.get('state', 'D')) for x in bprogram.tickets])
            if not program_finished:
                if any(next_must_finish):
                    bad_runs += 1
            Q_ess.reset_to_initial()
        return (runs - bad_runs) / runs




