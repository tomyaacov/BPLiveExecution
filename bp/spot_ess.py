from bppy import SimpleEventSelectionStrategy
import random

class SpotESS(SimpleEventSelectionStrategy):

    def __init__(self, states_dict, state_liveness) -> None:
        super().__init__()
        self.states_dict = states_dict
        self.states_dict_flip = dict(((v, k) for k, v in self.states_dict.items()))
        self.state_liveness = state_liveness
        self.current_state = self.states_dict_flip[0]

    def remove_dead_states(self, selectable_events):
        final_events = []
        for e, next_s in self.current_state.transitions.items():
            if e in selectable_events and self.state_liveness[self.states_dict[next_s]]:
                final_events.append((e, next_s))
        return final_events

    def select(self, statements):
        selectable_events = self.selectable_events(statements)
        selectable_events = self.remove_dead_states(selectable_events)
        if selectable_events:
            selected_event, next_state = random.choice(tuple(selectable_events))
            self.current_state = self.states_dict_flip[self.states_dict[next_state]]
            return selected_event
        else:
            self.reset_to_initial()
            return None

    def reset_to_initial(self):
        self.current_state = self.states_dict_flip[0]


