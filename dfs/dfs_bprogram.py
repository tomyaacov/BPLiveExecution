from dfs.dfs_node import DFSNode
import graphviz

from utils import timer


class DFSBProgram:
    def __init__(self, bprogram_gen):
        self.bprogram_gen = bprogram_gen

    def get_bprogram(self, node):
        bprogram = self.bprogram_gen()
        bprogram.setup()
        for event in node.prefix:
            bprogram.advance_bthreads(event)
        return bprogram

    @timer
    def run(self):
        total_events = set()
        bprogram = self.bprogram_gen()
        bprogram.setup()
        init_s = DFSNode(tuple(), "_".join([str(x.get('state', 'D')) for x in bprogram.tickets]))
        init_s.must_finish = [x.get('must_finish', False) for x in bprogram.tickets] # initial must finish must be false
        visited = {}
        # Create a stack for DFS
        stack = []
        # Push the current source node.
        stack.append(init_s)

        while (len(stack)):
            # Pop a vertex from stack
            s = stack.pop()

            # Stack may contain same vertex twice. So
            # we need to print the popped item only
            # if it is not visited.
            if not visited.get(s):
                #print(s.id)
                visited[s] = True

            # Get all adjacent vertices of the popped vertex s
            # If a adjacent has not been visited, then push it
            # to the stack.
            bprogram = self.get_bprogram(s)
            events = bprogram.event_selection_strategy.selectable_events(bprogram.tickets)
            for event in events:
                total_events.add(event)
                bprogram = self.get_bprogram(s)
                bprogram.advance_bthreads(event)
                new_s = DFSNode(s.prefix + (event,), "_".join([str(x.get('state', 'D')) for x in bprogram.tickets]))
                new_s.must_finish = [x.get('must_finish', False) for x in bprogram.tickets]
                s.transitions[event] = new_s
                s.rewards[event] = DFSBProgram.reward(s, new_s)
                if not visited.get(new_s):
                    stack.append(new_s)
        visited = dict([(k, i) for i,(k,_) in enumerate(visited.items())])
        s_to_change = [k for k,v in visited.items() if v == 0][0]
        number_to_change = visited[init_s]
        visited[init_s] = 0
        visited[s_to_change] = number_to_change
        return init_s, visited, total_events

    @staticmethod
    def save_graph(init, states, name):
        g = graphviz.Digraph()
        for s in states:
            g.node(s.id, shape='doublecircle' if s == init else 'circle', color="red" if any(s.must_finish) else "green")
        for s in states:
            for e, s_new in s.transitions.items():
                g.edge(s.id, s_new.id, label=e.name)
        g.render(name)
        return g

    @staticmethod
    def reward(s1, s2):
        reward = 0
        for j in range(len(s1.must_finish)):
            if s1.must_finish[j] and not s2.must_finish[j]:
                reward += 1
            if not s1.must_finish[j] and s2.must_finish[j]:
                reward -= 1
        # if reward == 0 and any(new_hot_states):
        #     reward = -0.001
        return reward


