from bppy import SimpleEventSelectionStrategy
import random

class SpotESS(SimpleEventSelectionStrategy):

    def __init__(self, states_dict, state_liveness) -> None:
        super().__init__()
        self.states_dict = states_dict
        self.states_dict_flip = dict(((v, k) for k, v in self.states_dict.items()))
        self.state_liveness = state_liveness
        self.current_state = self.states_dict_flip[0]

    def get_copy(self):
        return SpotESS(self.states_dict, self.state_liveness)

    def remove_dead_states(self, selectable_events):
        final_events = []
        selectable_events = list(selectable_events)
        selectable_events_names = [x.name for x in selectable_events]
        for e, next_s in self.current_state.transitions.items():
            if e in selectable_events_names and all([sl[self.states_dict[next_s]] for i, sl in self.state_liveness.items()]):
                final_events.append((selectable_events[selectable_events_names.index(e)], next_s))
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

    def get_selectable_events(self, statements):
        selectable_events = self.selectable_events(statements)
        selectable_events = self.remove_dead_states(selectable_events)
        return [x[0] for x in selectable_events]

    def advance(self, statements, e):
        selectable_events = self.selectable_events(statements)
        selectable_events = self.remove_dead_states(selectable_events)
        if selectable_events:
            for selected_event, next_state in selectable_events:
                if e == selected_event:
                    self.current_state = self.states_dict_flip[self.states_dict[next_state]]
                    return selected_event
            raise ValueError("Event is not selectable")
        else:
            raise ValueError("Event is not selectable")

    def reset_to_initial(self):
        self.current_state = self.states_dict_flip[0]


