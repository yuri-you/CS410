from icecream import ic
from utils  import expected_utility

def value_iteration(mdp, epsilon=0.001):
    """
    Solving an MDP by value iteration. [You may refer to Lecture 6, Slide 55 and Figure 17.4 in the reference book]
    
    paras: an MDP, an accuracy parameter epsilon which indicates the maximum change in the utility of any state in an iteration

    return: utilities, the optimal policy (to extract the optimal policy, you may use the best_policy() function)
    """
    def check_stop(U1,tmp_U):
        for s in U1:
            if abs(tmp_U[s]-U1[s])>=epsilon:
                return False
        return True
    U1 = {s: 0 for s in mdp.states}
    R, T, gamma = mdp.R, mdp.T, mdp.gamma
    import random
    policy = {s: random.choice(mdp.actions(s)) for s in mdp.states}
    t=0
    while True:
        """ YOUR CODE HERE """
        t+=1
        tmp_U=dict()
        for s in U1:
            if s in mdp.terminals:
                tmp_U[s]=U1[s]
                continue
            a=policy[s]
            v_s=expected_utility(a,s,U1,mdp)
            tmp_U[s]=v_s
        policy=best_policy(mdp,tmp_U)
        if check_stop(U1,tmp_U):
            return U1,policy
        else:
            U1=tmp_U

def best_policy(mdp, U):
    """
    Conduct policy extraction by using the function expected_utility(). Given an MDP and a utility function U, determine the best policy,
    as a mapping from state to action. [You may refer to Lecture 6, Slide 66]
        
    paras: an MDP, utilities U

    return: the extracted best policy
    """
    max=99999
    policy=dict()
    for s in mdp.states:
        if s in mdp.terminals:
            policy[s]=None
            continue
        value=-max
        for a in mdp.actions(s):
            now_value=expected_utility(a,s,U,mdp)
            if now_value>value:
                value=now_value
                action=a
        policy[s]=action
    return policy

    """ YOUR CODE HERE """