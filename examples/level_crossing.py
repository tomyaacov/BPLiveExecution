from bppy import *


must_finish = "must_finish"
state = "state"

Approaching = lambda i: BEvent("Approaching", {"type": i})
Entering = lambda i: BEvent("Entering", {"type": i})
Leaving = lambda i: BEvent("Leaving", {"type": i})
Lower = BEvent("Lower")
Raise = BEvent("Raise")
Any_Approaching = EventSet(lambda e: e.name == "Approaching")

@b_thread
def r1_passengers():  # train approaching, entering, and then leaving
    for i in range(3):
        yield {request: Approaching("Passengers"), state: 0}
        yield {request: Entering("Passengers"), state: 1}
        yield {request: Leaving("Passengers"), state: 2}

@b_thread
def r1_freight():  # train approaching, entering, and then leaving
    for i in range(3):
        yield {request: Approaching("Freight"), must_finish: True, state: 0}
        yield {request: Entering("Freight"), must_finish: True, state: 1}
        yield {request: Leaving("Freight"), state: 2}

@b_thread
def r1_maintenance():  # train approaching, entering, and then leaving
    for i in range(3):
        yield {request: Approaching("Maintenance"), state: 0}
        yield {request: Entering("Maintenance"), state: 1}
        yield {request: Leaving("Maintenance"), state: 2}

@b_thread
def r2():  # The barriers are lowered when a train is approaching and then raised as soon as possible.
    while True:
        yield {waitFor: Any_Approaching, state: 0}
        yield {request: Lower, state: 1}
        yield {request: Raise, state: 2}

@b_thread
def r3(type):  # A train may not enter while barriers are up.
    while True:
        yield {waitFor: Lower, block: Entering(type), state: 0}
        yield {waitFor: Raise, state: 1}

@b_thread
def r4(type):  # The barriers may not be raised while a train is in the intersection zone.
    while True:
        yield {waitFor: Approaching(type), state: 0}
        yield {waitFor: Leaving(type), block: Raise, state: 1}

@b_thread
def r7():  # a maintenance train must enter between 2 freight trains entering.
    while True:
        yield {waitFor: Entering("Freight"), state: 0}
        yield {waitFor: Entering("Maintenance"), block: Entering("Freight"), state: 1}



bthreads_list = [r1_passengers(), r1_freight(), r1_maintenance()] + \
                    [r3(i) for i in ["Passengers", "Freight", "Maintenance"]] + \
                    [r4(i) for i in ["Passengers", "Freight", "Maintenance"]] + \
                    [r2()]
bprogram =  BProgram(bthreads=bthreads_list, event_selection_strategy=SimpleEventSelectionStrategy(),
                 listener=PrintBProgramRunnerListener())

bprogram.run()


# def init_bprogram():
#     bthreads_list = [r1_passengers(), r1_freight(), r1_maintenance(), control()] + \
#                     [r3(i) for i in ["Passengers", "Freight", "Maintenance"]] + \
#                     [r4(i) for i in ["Passengers", "Freight", "Maintenance"]] + \
#                     [r2()]
#     return BProgram(bthreads=bthreads_list, event_selection_strategy=SimpleEventSelectionStrategy(),
#                  listener=PrintBProgramRunnerListener())
#
# if __name__ == "__main__":
#     # dfs = DFSBProgram(init_bprogram)
#     # init, states = dfs.run()
#     # DFSBProgram.save_graph(init, states, "graph.dot")
#     # Q = q_value_iteration(states, 0.99, 0.001)
#     # env = BPEnv()
#     # env.set_bprogram_generator(init_bprogram)
#     # Q_test(env, Q, 1000, 1, 1000, optimal=True)
#     env = BPEnv()
#     env.set_bprogram_generator(init_bprogram)
#     Q, results, episodes, mean_reward = qlearning(env, 10000, 0.1, 0.99, True, 5, glie_10, 1000)
#     Q_test(env, Q, 1000, 1, 1000, optimal=True)
