from .value_order import lcv
from .variable_order import mrv


def backtracking(
    csp,
    select_unassigned_variable=mrv,
    order_domain_values=lcv
):

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if csp.nconflicts(var,value,assignment)==0:
                csp.assign(var,value,assignment)
                new_assignment=backtrack(assignment)
                if new_assignment is not None:
                    return new_assignment
                else:csp.unassign(var,assignment)
        return None        

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result

def backtracking_with_inference(
    csp,
    inference,
    select_unassigned_variable=mrv,
    order_domain_values=lcv
):
    def backtrack(assignment):
        """ YOUR CODE HERE """
        if len(assignment) == len(csp.variables):return assignment
        var=select_unassigned_variable(assignment,csp)
        var = select_unassigned_variable(assignment, csp)
        domains=order_domain_values(var, assignment, csp)
        for value in domains:
            removals=[]
            if csp.nconflicts(var,value,assignment)>0:continue
            if not inference(csp,var,value,assignment,removals):
                csp.restore(removals)
                removals.clear()
                continue
            for i in domains:
                if i!=value and i in csp.curr_domains[var]:
                    csp.prune(var,i,removals)
            csp.assign(var,value,assignment)
            new_assignment=backtrack(assignment)
            if new_assignment is not None:return new_assignment
            else: 
                csp.unassign(var,assignment)
            csp.restore(removals)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result
