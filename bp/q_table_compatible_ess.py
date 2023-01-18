from bppy import SimpleEventSelectionStrategy
import random

class QTableCompatibleESS(SimpleEventSelectionStrategy):
    def __init__(self, Q, spot_ess=None, noise=None, per_bthread=True) -> None:
        self.per_bthread = per_bthread
        self.Q = Q
        self.spot_ess = spot_ess
        self.noise = noise
        if self.per_bthread:
            self.reward_sums = [0]*len(Q)
        else:
            self.reward_sums = 0
        super().__init__()

    def select(self, statements, prev_must_finish, next_must_finish, s_t):
        if not self.per_bthread:
            self.reward_sums += self.reward(prev_must_finish, next_must_finish)
            selectable_events = list(self.selectable_events(statements))
            if len(selectable_events) == 0:
                self.reset_to_initial()
                return None
            if s_t in self.Q:
                choices = [x for x in selectable_events if self.Q[s_t][x.name] + self.reward_sums > -1]
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
        self.reward_sums = [x+y for x, y in zip(self.reward_sums, self.reward(prev_must_finish, next_must_finish))]
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
        if self.per_bthread:
            self.reward_sums = [0] * len(self.Q)
        else:
            self.reward_sums = 0
        self.spot_ess.reset_to_initial()

    def reward(self, prev_must_finish, next_must_finish):
        if self.per_bthread:
            return [int(m1)-int(m2) for m1, m2 in zip(prev_must_finish, next_must_finish)]
        else:
            return int(not any(next_must_finish)) - int(not any(prev_must_finish))

