from bppy import SimpleEventSelectionStrategy
import random

class QTableCompatibleESS(SimpleEventSelectionStrategy):
    def __init__(self, Q, optimal=False) -> None:
        self.Q = Q
        self.optimal = optimal
        self.reward_sum = 0
        super().__init__()

    def select(self, statements, r_t, s_t):
        self.reward_sum += r_t
        selectable_events = list(self.selectable_events(statements))
        if len(selectable_events) == 0:
            self.reset_to_initial()
            return None
        if s_t in self.Q:
            if self.optimal:
                choices = [key for key in self.Q[s_t].keys() if self.Q[s_t][key] == max(self.Q[s_t].values())]
            else:
                choices = [key for key in self.Q[s_t].keys() if self.Q[s_t][key] + self.reward_sum > -1]
            try:
                a_t = random.choice(choices)
            except IndexError:
                a_t = random.choice(selectable_events)
        else:
            a_t = random.choice(selectable_events)
        return a_t

    def reset_to_initial(self):
        self.reward_sum = 0

