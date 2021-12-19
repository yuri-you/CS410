def no_inference(csp, var, value, assignment, removals):
    return True

def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()  # It is necessary for using csp.prune()
    for item in csp.neighbors[var]:
        if value in csp.curr_domains[item]:
            csp.prune(item,value,removals)
        if len(csp.curr_domains[item])==0:
            return False
    return True

def AC3(csp, removals=None):
    def revise(Xi, Xj):
        """Return true if we remove a value."""
        """ YOUR CODE HERE """
        if len(csp.curr_domains[Xi])==1 and csp.curr_domains[Xi][0] in csp.curr_domains[Xj]:
            csp.prune(Xj,csp.curr_domains[Xi][0],removals)
            return True
        else:return False    

    csp.support_pruning()  # It is necessary for using csp.prune()
    #queue = {(Xi, Xk) for Xi in csp.variables if len(csp.curr_domains[Xi])==1 for Xk in csp.neighbors[Xi]}
    queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    while queue:
        """ YOUR CODE HERE """
        Xi,Xj=queue.pop()
        if revise(Xi,Xj):
            for item in csp.neighbors[Xj]:
                queue.add((Xj,item))       
    return True  # CSP is satisfiable

def mac(csp, var, value, assignment, removals, constraint_propagation=AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, removals)
