from bppy import SimpleEventSelectionStrategy
import random

class QTableCompatibleESS(SimpleEventSelectionStrategy):
    def __init__(self, Q, spot_ess=None, per_bthread=True) -> None:
        self.per_bthread = per_bthread
        self.Q = Q
        self.spot_ess = spot_ess
        self.noise = lambda: 0
        if self.per_bthread:
            self.reward_sums = 0
        else:
            self.reward_sums = 0
        super().__init__()

    def get_copy(self):
        spot_ess = self.spot_ess.get_copy()
        obj = QTableCompatibleESS(self.Q, spot_ess, self.per_bthread)
        obj.noise = self.noise
        return obj


    def select(self, statements, prev_must_finish, next_must_finish, s_t):
        self.reward_sums += self.reward(prev_must_finish, next_must_finish)
        selectable_events = list(self.selectable_events(statements))
        if len(selectable_events) == 0:
            self.reset_to_initial()
            return None
        if s_t in self.Q:
            choices = [x for x in selectable_events if self.Q[s_t][x.name] + self.noise() + self.reward_sums > -0.5]
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
        if self.per_bthread:
            self.reward_sums = 0
        else:
            self.reward_sums = 0
        self.spot_ess.reset_to_initial()

    def reward(self, prev_must_finish, next_must_finish):
        if self.per_bthread:
            return sum([int(m1)-int(m2) for m1, m2 in zip(prev_must_finish, next_must_finish)])
        else:
            return int(not any(next_must_finish)) - int(not any(prev_must_finish))

    def set_noise(self, f):
        # self.noise = {}
        # for s, v in self.Q.items():
        #     self.noise[s] = {}
        #     for a, _ in v.items():
        #         self.noise[s][a] = f()
        self.noise = f

