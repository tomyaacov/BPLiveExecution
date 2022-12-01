import random
from utils import timer
from bp.q_table_compatible_ess import QTableCompatibleESS


def glie_3(i, num_episodes):
    if i >= num_episodes - 100:
        return 0
    return 1


def glie_10(i, num_episodes):
    if i >= num_episodes - 100:
        return 0
    return 1 - (i / num_episodes)


def epsilon_greedy_online(bprogram, Q, s_t, epsilon, reward_sum):
    if random.random() > epsilon:
        if s_t in Q:
            try:
                return random.choice([key for key in Q[s_t].keys() if Q[s_t][key] == max(Q[s_t].values())])
                # return random.choice([key for key in Q[s_t].keys() if reward_sum + Q[s_t][key] > -1])
            except IndexError:
                return random.choice(tuple(bprogram.event_selection_strategy.selectable_events(bprogram.tickets)))
        else:
            return random.choice(tuple(bprogram.event_selection_strategy.selectable_events(bprogram.tickets)))
    else:
        try:
            return random.choice(tuple(bprogram.event_selection_strategy.selectable_events(bprogram.tickets)))
        except IndexError:
            return None


def must_finish(bprogram):
    return [x.get('must_finish', False) for x in bprogram.tickets]


def qlearning(environment, num_episodes, alpha, gamma, testing, seed, glie, episode_timeout=None):
    random.seed(seed)
    Q = dict()
    test_results = []
    tested_episodes = []
    mean_reward = []
    for i in range(num_episodes):
        done = False
        s_t = environment.reset()
        steps_counter = 0
        reward_sum = 0
        if s_t not in Q:
            Q[s_t] = {i: 0 for i in
                      environment.bprogram.event_selection_strategy.selectable_events(environment.bprogram.tickets)}
        epsilon = glie(i, num_episodes)
        a_t = epsilon_greedy_online(environment.bprogram, Q, s_t, epsilon, reward_sum)
        while not done:
            s_t_1, r_t, bprogram_done, _ = environment.step(a_t)
            reward_sum += r_t
            a_t_1 = epsilon_greedy_online(environment.bprogram, Q, s_t_1, epsilon, reward_sum)
            if s_t_1 not in Q:
                if bprogram_done:
                    Q[s_t_1] = {0: 0}
                else:
                    Q[s_t_1] = {i: 0 for i in environment.bprogram.event_selection_strategy.selectable_events(
                        environment.bprogram.tickets)}

            Q[s_t][a_t] = Q[s_t][a_t] + alpha * (r_t + gamma * max(Q[s_t_1].values()) - Q[s_t][a_t])

            s_t, a_t = s_t_1, a_t_1
            timeout = steps_counter == episode_timeout
            done = bprogram_done or timeout
            steps_counter += 1
        if testing:
            test_results.append(reward_sum)
            tested_episodes.append(i)
            mean_reward.append(sum(test_results[-100:]) / len(test_results[-100:]))
            if i % 100 == 0:
                print(f"Round {i} ended with {mean_reward[-1]} mean reward")
    return Q, test_results, tested_episodes, mean_reward


def run(environment, Q, seed, episode_timeout, optimal=False):
    random.seed(seed)
    s_t = environment.reset()
    run = ""
    reward_sum = 0
    if s_t in Q:
        if optimal:
            choices = [key for key in Q[s_t].keys() if Q[s_t][key] == max(Q[s_t].values())]
        else:
            choices = [key for key in Q[s_t].keys() if Q[s_t][key] + reward_sum > -1]
        try:
            a_t = random.choice(choices)
        except IndexError:
            a_t = random.choice(
                tuple(environment.bprogram.event_selection_strategy.selectable_events(environment.bprogram.tickets)))
    else:
        a_t = random.choice(
            tuple(environment.bprogram.event_selection_strategy.selectable_events(environment.bprogram.tickets)))
    run += a_t.name
    steps_counter = 0
    while True:
        s_t_1, r_t, done, _ = environment.step(a_t)
        reward_sum += r_t
        if done:
            break
        if s_t_1 in Q:
            if optimal:
                choices = [key for key in Q[s_t_1].keys() if Q[s_t_1][key] == max(Q[s_t_1].values())]
            else:
                choices = [key for key in Q[s_t_1].keys() if reward_sum + Q[s_t_1][key] > -1]
            try:
                a_t_1 = random.choice(choices)
            except IndexError:
                a_t_1 = random.choice(tuple(
                    environment.bprogram.event_selection_strategy.selectable_events(environment.bprogram.tickets)))
        else:
            a_t_1 = random.choice(
                tuple(environment.bprogram.event_selection_strategy.selectable_events(environment.bprogram.tickets)))
        s_t, a_t = s_t_1, a_t_1
        run += a_t.name
        if steps_counter == episode_timeout:
            break
        steps_counter += 1
    return reward_sum, run


def Q_test(environment, Q, rounds, seed, episode_timeout, optimal=False):
    total_reward = 0
    success = 0
    for i in range(rounds):
        r, s = run(environment, Q, seed + i, episode_timeout, optimal)
        total_reward += r
        if r == 0:
            success += 1
    print("Average Reward:", total_reward / rounds, "Successful Round pct.", success / rounds)


class QLearning:

    @staticmethod
    @timer
    def compute_ess(environment, num_episodes, alpha, gamma, testing, seed, glie, episode_timeout=None):
        Q, results, episodes, mean_reward = qlearning(environment, num_episodes, alpha, gamma, testing, seed, glie, episode_timeout)
        return QTableCompatibleESS(Q), Q, results, episodes, mean_reward





