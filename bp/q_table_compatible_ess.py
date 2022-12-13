from bppy import SimpleEventSelectionStrategy
import random

class QTableCompatibleESS(SimpleEventSelectionStrategy):
    def __init__(self, Q, optimal=False) -> None:
        self.Q = Q
        #self.optimal = optimal
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
        return a_t

    def reset_to_initial(self):
        self.reward_sums = [0]*len(self.Q)

