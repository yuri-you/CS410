import random

from util import argmin_random_tie


def min_conflicts_value(csp, var, current):
    """Return the value that will give var the least number of conflicts.
    If there is a tie, choose at random."""
    return argmin_random_tie(csp.domains[var], key=lambda val: csp.nconflicts(var, val, current))

def min_conflicts(csp, max_steps=100000):
    """Solve a CSP by Hill Climbing on the number of conflicts."""
    """ YOUR CODE HERE """
    from random import choice
    from .variable_order import mrv
    def random_choose(assignment):
        l=csp.variables
        if len(l)==len(assignment):
            return choice(l)
        else:
            return mrv(assignment,csp)
    assignment=dict()
    step=0
    while(len(assignment)<len(csp.variables) or not csp.goal_test(assignment)) and step<max_steps:
        var=random_choose(assignment)    
        val=min_conflicts_value(csp,var,assignment)
        csp.assign(var,val,assignment)
        step+=1
    if csp.goal_test(assignment):
        return assignment
    else: return None 
