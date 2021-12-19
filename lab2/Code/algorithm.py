from problem import Direction, SearchProblem
import math


class SearchAlgorithm:
    def __init__(self, algo_name):
        assert algo_name in ["tiny", "bfs", "dfs", "Exercise2_1_1", "Exercise2_1_2", "Exercise2_2_1", "Exercise2_2_2", "Exercise2_3_1"], "Invalid algorithm."

        if algo_name == "tiny":
            self._solver = tiny_maze_search
        elif algo_name == "bfs":
            self._solver = breadth_first_search
        elif algo_name == "dfs":
            self._solver = depth_first_search

        # for Lab 2
        elif algo_name == "Exercise2_1_1":
            self._solver = Exercise2_1_1
        elif algo_name == "Exercise2_1_2":
            self._solver = Exercise2_1_2
        elif algo_name == "Exercise2_2_1":
            self._solver = Exercise2_2_1
        elif algo_name == "Exercise2_2_2":
            self._solver = Exercise2_2_2
        elif algo_name == "Exercise2_3_1":
            self._solver = Exercise2_3_1

    def __call__(self, problem):
        return self._solver(problem)


def tiny_maze_search(problem):
    """Returns a sequence of moves that solves tinyMaze."""
    s = Direction.SOUTH
    w = Direction.WEST
    return  [s, s, w, s, w, w, s, w]

def depth_first_search(problem):
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

    """ YOUR CODE HERE """

    return []

def breadth_first_search(problem):
    """Returns a sequence of moves that solves general maze problems with BFS.

    Search the shallowest nodes in the search tree first.
    """
    from util import Queue

    """ YOUR CODE HERE """

    return []

# ****************************** For Lab 2 ******************************

def Exercise2_1_1(problem:SearchProblem):
    """
    Returns the number of lakes using depth-first graph search (DFGS).

    Please note that some APIs in the environment of Lab 2 are slightly different from them in the environment of Lab 1.
    """
    from util import Stack
    search_position=Stack()
    position=set()
    search_position.push(problem.get_start())
    while not search_position.is_empty():
        now_position=search_position.pop()
        if now_position not in position:
            position.add(now_position)
            reach=problem.get_successors(now_position,2)#search all possible neigbhors
            for item in reach:
                search_position.push(item[0])
    number=0
    arrived=set()
    lake_stack=Stack()
    for item1 in position:
        neighbor_lake=problem.get_successors(item1,1)
        for item_2 in neighbor_lake:
            item2=item_2[0]
            if item2 not in arrived:
                number+=1
                arrived.add(item2)
                lake_stack.push(item2)
                while not lake_stack.is_empty():
                    now_lake_position=lake_stack.pop()
                    linked_lake=problem.get_successors(now_lake_position,1)
                    for item_3 in linked_lake:
                        item3=item_3[0]
                        if item3 not in arrived:
                            arrived.add(item3)
                            lake_stack.push(item3)
    return number
def increase_function1(times:int):
    return times+1
def increase_function2(times:int):
    return 2**times
def Exercise2_1_2(problem:SearchProblem):
    """
    Returns the path from S to G using DFGS with the iterative deepening trick.
    """
    memory=0
    memory1=0
    memory2=0
    time1=0
    time2=0
    depth_list1=[]
    depth_list2=[]
    time_list1=[]
    time_list2=[]
    memory_list1=[]
    memory_list2=[]
    times=0
    from util import Stack
    try:
        while 1:
            depth=increase_function1(times)
            depth_list1.append(depth)
            dfs_stack=Stack()
            memory=0
            dfs_stack.push((0,problem.get_start()))
            memory+=1
            memory1=max(memory1,memory)
            time1+=1
            while not dfs_stack.is_empty():
                position=dfs_stack.pop()
                if problem.is_goal(position[1]):
                    time_list1.append(time1)
                    memory_list1.append(memory1)
                    raise Exception  
                memory-=1
                time1+=1
                if position[0]<depth:
                    neighbor=problem.get_successors(position[1])
                    time1+=4
                    memory+=len(neighbor)
                    memory1=max(memory1,memory)
                    for item in neighbor:
                        dfs_stack.push((position[0]+1,item[0]))
            times+=1
            time_list1.append(time1)
            memory_list1.append(memory1)
    except Exception:
        pass
    times=0
    try:
        while 1:
            depth=increase_function2(times)
            depth_list2.append(depth)
            dfs_stack=Stack()
            memory=0
            dfs_stack.push((0,problem.get_start()))
            memory+=1
            memory2=max(memory2,memory)
            time2+=1
            while not dfs_stack.is_empty():
                position=dfs_stack.pop()
                if problem.is_goal(position[1]):
                    time_list2.append(time2)
                    memory_list2.append(memory2)
                    raise Exception  
                memory-=1
                time2+=1
                if position[0]<depth:
                    neighbor=problem.get_successors(position[1])
                    time2+=4
                    memory+=len(neighbor)
                    memory2=max(memory2,memory)
                    for item in neighbor:
                        dfs_stack.push((position[0]+1,item[0]))
            times+=1
            time_list2.append(time2)
            memory_list2.append(memory2)
    except Exception:
        pass
    # import matplotlib.pyplot as plt

    # # #show time consumption
    # l1,=plt.plot(depth_list1,time_list1,c='red')
    # l2,=plt.plot(depth_list2,time_list2,c='blue')
    # plt.title("Time Consumption of Two Increasing Function", fontdict={'family' : 'Times New Roman', 'size'   : 26})
    # plt.legend(handles = [l1,l2], labels=["$f(x)=x+1$","$f(x)=2^x$"],loc = 'upper left', prop={'family' : 'Times New Roman', 'size'   : 20})
    # plt.xlabel("Depth", fontproperties = 'Times New Roman',fontsize=25)
    # plt.ylabel("Consumption", fontproperties = 'Times New Roman',fontsize=25)
    # for i in range(len(depth_list1)):
    #     plt.scatter(depth_list1[i],time_list1[i],c='red')
    # for i in range(len(depth_list2)):
    #     plt.scatter(depth_list2[i],time_list2[i],c='blue')
    # plt.show()


    # # #show memory consumption    
    # l1,=plt.plot(depth_list1,memory_list1,c='red')
    # l2,=plt.plot(depth_list2,memory_list2,c='blue')
    # plt.title("Memory Consumption of Two Increasing Function", fontdict={'family' : 'Times New Roman', 'size'   : 26})
    # plt.legend(handles = [l1,l2], labels=["$f(x)=x+1$","$f(x)=2^x$"],loc = 'upper left', prop={'family' : 'Times New Roman', 'size'   : 20})
    # plt.xlabel("Depth", fontproperties = 'Times New Roman',fontsize=25)
    # plt.ylabel("Consumption", fontproperties = 'Times New Roman',fontsize=25)
    # for i in range(len(depth_list1)):
    #     plt.scatter(depth_list1[i],memory_list1[i],c='red')
    # for i in range(len(depth_list2)):
    #     plt.scatter(depth_list2[i],memory_list2[i],c='blue')
    # plt.show()

    return [["increasing function1：",["total time consumption",time_list1[-1]],["total memory consumption",memory_list1[-1]]],
    ["increasing function2：",["total time consumption",time_list2[-1]],["total memory consumption",memory_list2[-1]]]]
def Exercise2_2_1(problem:SearchProblem):
    """
    Returns the least-cost path from S to G and its cost using uniform-cost graph search (UCGS)
    """
    from queue import PriorityQueue
    class UCS_item:
        def __init__(self,distance,position,path=[]):
            self.distance=distance
            self.path=path
            self.position=position
        def __lt__(self,other):
            return self.distance<other.distance
    from queue import PriorityQueue
    PQ=PriorityQueue()
    PQ.put(UCS_item(0,problem.get_start()))
    now=PQ.get()
    arrived=set()
    while not problem.is_goal(now.position):
        successor=problem.get_successors(now.position,0)
        for item in successor:
            if item[0] in arrived:continue
            arrived.add(item[0])
            new_path=now.path.copy()
            new_path.append(item[1].name)
            PQ.put(UCS_item(now.distance+item[2],item[0],new_path))
        now=PQ.get()
    return (len(now.path),now.path)
    """ YOUR CODE HERE """

def Heuristic1(state1, state2): # the first heuristic function using Euclidean distance
    return math.sqrt((state1[0]-state2[0])**2+(state1[1]-state2[1])**2)

def Exercise2_2_2(problem:SearchProblem):
    """
    Returns the path from S to G using greedy graph search (GGS).
    """
    from queue import PriorityQueue
    class heuristc_Euclidean_item:
        def __init__(self,distance,position,path=[]):
            self.distance=distance
            self.path=path
            self.position=position
        def __lt__(self,other):
            return self.distance<other.distance
    goal=problem.get_goal()
    begin=problem.get_start()
    PQ=PriorityQueue()
    PQ.put(heuristc_Euclidean_item(Heuristic1(begin,goal),begin))
    now=PQ.get()
    while not problem.is_goal(now.position):
        successor=problem.get_successors(now.position,0)
        for item in successor:
            new_path=now.path.copy()
            new_path.append(item[1].name)
            PQ.put(heuristc_Euclidean_item(Heuristic1(item[0],goal),item[0],new_path))
        now=PQ.get()
    return (len(now.path),now.path)

def Heuristic2(state1, state2): # the second heuristic function
    return abs(state1[0]-state2[0])+abs(state1[1]-state2[1])

def Exercise2_3_1(problem):
    """
    Returns the least-cost path from S to G and its cost using a-star graph search (ASGS)
    """
    from queue import PriorityQueue
    class A_star_item:
        def __init__(self,priority,distance,position,path=[]):
            self.priority=priority
            self.distance=distance
            self.path=path
            self.position=position
        def __lt__(self,other):
            return self.priority<other.priority
    goal=problem.get_goal()
    begin=problem.get_start()
    PQ=PriorityQueue()
    PQ.put(A_star_item(0,0,begin))
    now=PQ.get()
    Heuristic=Heuristic1
    arrived=set()
    while not problem.is_goal(now.position):
        if now.position in arrived:
            now=PQ.get()
            continue
        arrived.add(now.position)
        successor=problem.get_successors(now.position,0)
        for item in successor:
            new_path=now.path.copy()
            new_path.append(item[1].name)
            PQ.put(A_star_item(Heuristic(item[0],goal)+now.distance+item[2], 
            now.distance+item[2], item[0],new_path))
        now=PQ.get()
    return (len(now.path),now.path)
    """ YOUR CODE HERE """
    return []