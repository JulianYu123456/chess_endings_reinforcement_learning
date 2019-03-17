import numpy as np

def deterministic_policy_eval_step_win_loss(states_actions, V, pi):
    # 
    delta = 0
    for state, actions in states_actions.items():
        action = pi[state]
        next_node = actions[action]['next_state']
        reward = actions[action]['status']
        V_updated = 0
        if next_node in V:
            V_updated = -(reward + V[next_node])
        else:
            V_updated = -reward
        delta = max(delta, np.abs(V_updated - V[state]))
        V[state] = V_updated
    return V, delta

def policy_improve_win_loss(V, states_actions):
    pi = {}
    for state, actions in states_actions.items():
        actions_list = [] # list(actions.keys())
        expected_rewards = [] #np.zeros(len(actions))
        for i, (action, data) in enumerate(actions.items()):
            actions_list.append(action)
            next_state = data['next_state']
            reward = data['status']
            if next_state in V:
                expected_rewards.append(-(reward + V[next_state]))
            else:
                expected_rewards.append(-reward)

        pi[state] = actions_list[np.argmax(expected_rewards)]
        if state == '4k3/8/4K2R/8/8/8/8/8 w':
            print(np.argmax(expected_rewards))
            print(actions_list)
            print(expected_rewards)
    return pi

def deterministic_policy_eval_step_shortest_path(states_actions, V, pi, winning_reward=1e3):
    # Evaluation in place (in contrast with evaluation with 2 arrays).
    # Needs less memory and converges too
    # pi is a dict and pi[s] is the best action for that state. (The most probable action)
    delta = 0
    for state, actions in states_actions.items():
        action = pi[state]
        next_node = actions[action]['next_state']
        reward = actions[action]['status']
        V_updated = 0
        if next_node in V:
            V_updated = -(reward + V[next_node]) - np.sign(-V[next_node])
        else:
            V_updated = -reward * winning_reward
        delta = max(delta, np.abs(V_updated - V[state]))
        V[state] = V_updated
    return V, delta


def policy_improve_shortest_path(V, states_actions, winning_reward=1e3):
    pi = {}
    for state, actions in states_actions.items():
        actions_list = [] # list(actions.keys())
        expected_rewards = [] #np.zeros(len(actions))
        for i, (action, data) in enumerate(actions.items()):
            actions_list.append(action)
            next_state = data['next_state']
            reward = data['status']
            if next_state in V:
                expected_rewards.append(-(reward + V[next_state]) - np.sign(-V[next_state]))
            else:
                expected_rewards.append(-reward * winning_reward)

        pi[state] = actions_list[np.argmax(expected_rewards)]
        if state == '4k3/8/4K2R/8/8/8/8/8 w':
            print(actions_list[np.argmax(expected_rewards)])
            print(actions_list)
            print(expected_rewards)
    return pi


def policy_iteration(states_actions, pi_old, deterministic_policy_eval_step = deterministic_policy_eval_step_shortest_path, policy_improve=policy_improve_shortest_path, theta=1e-6, verbose = 0):
    # Politica inicial
    policy_updates = 100
    while policy_updates > 0:
        # Calculo values de politica
        V, iters = policy_evaluation(deterministic_policy_eval_step, states_actions, pi_old, theta, verbose=verbose)
        # Mejoro política con values
        pi = policy_improve(V, states_actions)

        policy_updates = 0
        for j, (state, accion) in enumerate(pi.items()):
            if accion != pi_old[state]:
                 policy_updates += 1
        pi_old = pi.copy()
        if verbose:
            print('Number of differences of new policy vs old policy:', policy_updates)
            print('---------------------------')
    return pi_old, V


def policy_evaluation(policy_eval_step, states_actions, pi, theta, verbose=0):
    if verbose:
        print('Policy evaluation iteration number: ', end=' ')
    
    V = {}
    iters = 0
    for state in states_actions:
        V[state] = 0
    delta = theta + 1
    while theta<delta: 
        V, delta = policy_eval_step(states_actions, V, pi)
        iters += 1
        if verbose:
            print(iters, end=' ')
    print()
    return V, iters