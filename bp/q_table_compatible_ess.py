from bppy import SimpleEventSelectionStrategy
import random

class QTableCompatibleESS(SimpleEventSelectionStrategy):
    def __init__(self, Q, spot_ess=None, noise=None) -> None:
        self.Q = Q
        self.spot_ess = spot_ess
        self.noise = noise
        self.reward_sums = [0]*len(Q)
        super().__init__()

    def select(self, statements, r_t, s_t):
        self.reward_sums = [x+y for x, y in zip(self.reward_sums, r_t)]
        selectable_events = list(self.selectable_events(statements))
        if len(selectable_events) == 0:
            self.reset_to_initial()
            return None
        if all([s_t in Q_i for i, Q_i in self.Q.items()]):
            choices = [x for x in selectable_events if all([Q_i[s_t][x] + self.reward_sums[i] > -1 for i, Q_i in self.Q.items()])]
            try:
                a_t = random.choice(choices)
            except IndexError:
                a_t = random.choice(selectable_events)
        else:
            a_t = random.choice(selectable_events)
        if a_t in self.spot_ess.get_selectable_events(statements):
            self.spot_ess.advance(statements, a_t)
            return a_t
        else:
            return None

    def reset_to_initial(self):
        self.reward_sums = [0]*len(self.Q)
        self.spot_ess.reset_to_initial()

