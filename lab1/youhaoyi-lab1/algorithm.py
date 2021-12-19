from numpy.core.fromnumeric import nonzero
from problem import Direction, SearchProblem


class SearchAlgorithm:
    def __init__(self, algo_name):
        assert algo_name in ["tiny", "bfs", "dfs"], "Invalid algorithm."

        if algo_name == "tiny":
            self._solver = tiny_maze_search
        elif algo_name == "bfs":
            self._solver = breadth_first_search
        elif algo_name == "dfs":
            self._solver = depth_first_search

    def __call__(self, problem):
        return self._solver(problem)


def tiny_maze_search(problem):
    """Returns a sequence of moves that solves tinyMaze."""
    s = Direction.SOUTH
    w = Direction.WEST
    return  [s, s, w, s, w, w, s, w]

def depth_first_search(problem:SearchProblem):
    """Returns a sequence of moves that solves general maze problems with DFS.

    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. To get started, you might leverage your Stack structure and the APIs
    provided in the Problem class:

    print("Start:", problem.get_start())
    print("Is the start a goal?", problem.is_goal(problem.get_start()))
    print("Start's successors:", problem.get_successors(problem.get_start()))
    """
    from util import Stack
    startx,starty=problem.get_start()
    search=Stack()
    search.push([(startx,starty),[]])
    while not search.is_empty():
        now_situation=search.pop()
        now_state=now_situation[0]
        actions=problem.get_successors(now_state)
        for information in actions:
            all_actions=now_situation[1].copy()
            next_state,action,cost=information
            if problem.is_goal(next_state):
                all_actions.append(action)
                return all_actions
            else:
                all_actions.append(action)
                search.push([next_state,all_actions])

    """ YOUR CODE HERE """

    return []

def breadth_first_search(problem):
    """Returns a sequence of moves that solves general maze problems with BFS.

    Search the shallowest nodes in the search tree first.
    """
    from util import Queue
    startx,starty=problem.get_start()
    search=Queue()
    search.push([(startx,starty),[]])
    while not search.is_empty():
        now_situation=search.pop()
        now_state=now_situation[0]
        actions=problem.get_successors(now_state)
        for information in actions:
            all_actions=now_situation[1].copy()
            next_state,action,cost=information
            if problem.is_goal(next_state):
                all_actions.append(action)
                return all_actions
            else:
                all_actions.append(action)
                search.push([next_state,all_actions])

    """ YOUR CODE HERE """

    return []
