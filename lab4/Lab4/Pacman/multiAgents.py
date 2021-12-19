# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions, Game
import random, util

from game import Agent
from pacman import GameState
max_range=99999
class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '4'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent
    """

    def getAction(self, gameState:GameState):
        def maxlayer(now_gameState:GameState,layer):
            if layer==self.depth or now_gameState.isWin() or now_gameState.isLose():
                return self.evaluationFunction(now_gameState)
            actions_space=now_gameState.getLegalActions(0)            # best_value=""
            best_value=-max_range #initial
            best_action=[]
            for action in actions_space:
                new_state=now_gameState.generateSuccessor(0,action)
                value=minlayer(new_state,layer,1)
                if best_value<value:
                    best_value=value
                    best_action.clear()
                    best_action.append(action)
                elif best_value==value:
                    best_action.append(action)
            if layer==0:
                return random.choice(best_action)
            else:
                return best_value

                
        def minlayer(now_gameState:GameState,layer,ghost_id):
            if now_gameState.isWin() or now_gameState.isLose():
                return self.evaluationFunction(now_gameState)
            if ghost_id==now_gameState.getNumAgents()-1:
                worst_value=max_range
                actions_space=now_gameState.getLegalActions(ghost_id)
                for action in actions_space:
                    new_state=now_gameState.generateSuccessor(ghost_id,action)
                    value=maxlayer(new_state,layer+1)
                    if worst_value>value:
                        worst_value=value
                return worst_value
            else:
                worst_value=max_range
                actions_space=now_gameState.getLegalActions(ghost_id)
                for action in actions_space:
                    new_state=now_gameState.generateSuccessor(ghost_id,action)
                    value=minlayer(new_state,layer,ghost_id+1)
                    if worst_value>value:
                        worst_value=value
                return worst_value

        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        return maxlayer(gameState,0)
        "*** YOUR CODE HERE ***"
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState):
        def maxlayer(now_gameState:GameState,layer,alpha,beta):
            if layer==self.depth or now_gameState.isWin() or now_gameState.isLose():
                return self.evaluationFunction(now_gameState)
            actions_space=now_gameState.getLegalActions(0)
            best_value=-max_range #initial
            best_action=[]
            for action in actions_space:
                new_state=now_gameState.generateSuccessor(0,action)
                value=minlayer(new_state,layer,1,alpha,beta)
                if value>=beta:return value
                alpha=max(alpha,value)
                if best_value<value:
                    best_value=value
                    best_action=action
            if layer==0:
                return best_action
            else:
                return best_value

                
        def minlayer(now_gameState:GameState,layer,ghost,alpha,beta):
            if now_gameState.isWin() or now_gameState.isLose():
                return self.evaluationFunction(now_gameState)
            if ghost==now_gameState.getNumAgents()-1:
                worst_value=max_range
                actions_space=now_gameState.getLegalActions(ghost)
                for action in actions_space:
                    new_state=now_gameState.generateSuccessor(ghost,action)
                    value=maxlayer(new_state,layer+1,alpha,beta)
                    if value<=alpha:return value
                    beta=min(beta,value)
                    if worst_value>value:
                        worst_value=value
                return worst_value
            else:
                worst_value=max_range
                actions_space=now_gameState.getLegalActions(ghost)
                for action in actions_space:
                    new_state=now_gameState.generateSuccessor(ghost,action)
                    value=minlayer(new_state,layer,ghost+1,alpha,beta)
                    if value<=alpha:return value
                    beta=min(beta,value)
                    if worst_value>value:
                        worst_value=value
                return worst_value
        return maxlayer(gameState,0,-max_range,max_range)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent
    """

    def getAction(self, gameState):
        def maxlayer(now_gameState:GameState,layer):
            if layer==self.depth or now_gameState.isWin() or now_gameState.isLose():
                return self.evaluationFunction(now_gameState)
            actions_space=now_gameState.getLegalActions(0)
            # best_action=""
            # best_value=""
            best_value=-max_range #initial
            best_action=[]
            for action in actions_space:
                new_state=now_gameState.generateSuccessor(0,action)
                value=averagelayer(new_state,layer+1,1)
                if best_value<value:
                    best_value=value
                    best_action.clear()
                    best_action.append(action)
                elif best_value==value:
                    best_action.append(action)
            if layer==0:
                return random.choice(best_action)
            else:
                return best_value

                
        def averagelayer(now_gameState:GameState,layer,ghost):
            if now_gameState.isWin() or now_gameState.isLose():
                return self.evaluationFunction(now_gameState)
            if ghost==now_gameState.getNumAgents()-1:
                average_value=0
                actions_space=now_gameState.getLegalActions(ghost)
                for action in actions_space:
                    new_state=now_gameState.generateSuccessor(ghost,action)
                    average_value+=maxlayer(new_state,layer)
                average_value/=len(actions_space)
                return average_value
            else:
                average_value=0
                actions_space=now_gameState.getLegalActions(ghost)
                for action in actions_space:
                    new_state=now_gameState.generateSuccessor(ghost,action)
                    average_value+=averagelayer(new_state,layer,ghost+1)
                average_value/=len(actions_space)
                return average_value
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return maxlayer(gameState,0)
