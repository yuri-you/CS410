# ghostAgents.py
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


from game import Agent
from game import Actions
from game import Directions
import random
from pacman import GameState
from util import manhattanDistance
import util
max_range=99999

class GhostAgent(Agent):
    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()


class RandomGhost(GhostAgent):
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, state):
        dist = util.Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist


class DirectionalGhost(GhostAgent):
    "A ghost that prefers to rush Pacman, or flee when scared."

    def __init__(self, index, prob_attack=0.8, prob_scaredFlee=0.8):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution(self, state):
        # Read variables from state
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        pos = state.getGhostPosition(self.index)
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared:
            speed = 0.5

        actionVectors = [Actions.directionToVector(
            a, speed) for a in legalActions]
        newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance(
            pos, pacmanPosition) for pos in newPositions]
        if isScared:
            bestScore = max(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip(
            legalActions, distancesToPacman) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1-bestProb) / len(legalActions)
        dist.normalize()
        return dist

def scoreEvaluationFunctionGhost(currentGameState):
    return currentGameState.getScore()

class MinimaxGhost(GhostAgent):
    def __init__(self, index, evalFn = 'scoreEvaluationFunctionGhost', depth = '2'):
        self.index = index # Ghosts are always with index > 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getAction(self, gameState):
        def maxlayer(now_gameState:GameState,layer):
            if layer==self.depth or now_gameState.isWin() or now_gameState.isLose():
                return self.evaluationFunction(now_gameState)
            actions_space=now_gameState.getLegalActions(0)
            best_value=-max_range #initial
            for action in actions_space:
                new_state=now_gameState.generateSuccessor(0,action)
                value=minlayer(new_state,layer+1,1)
                if best_value<value:
                    best_value=value
            return best_value
        def minlayer(now_gameState:GameState,layer,ghost):
            if now_gameState.isWin() or now_gameState.isLose():
                return self.evaluationFunction(now_gameState)
            elif ghost==now_gameState.getNumAgents()-1:
                worst_value=max_range
                actions_space=now_gameState.getLegalActions(ghost)
                worst_action=[]
                for action in actions_space:
                    new_state=now_gameState.generateSuccessor(ghost,action)
                    value=maxlayer(new_state,layer)
                    if worst_value>value:
                        worst_action.clear()
                        worst_action.append(action)
                        worst_value=value
                    elif worst_value==value:
                        worst_action.append(action)
                if ghost==self.index and layer==0: 
                    return random.choice(worst_action)
                else: return worst_value
            else:
                worst_value=max_range
                actions_space=now_gameState.getLegalActions(ghost)
                worst_action=[]
                for action in actions_space:
                    new_state=now_gameState.generateSuccessor(ghost,action)
                    value=minlayer(new_state,layer,ghost+1)
                    if worst_value>value:
                        worst_action.clear()
                        worst_action.append(action)
                        worst_value=value
                    elif worst_value==value:
                        worst_action.append(action)
                if ghost==self.index and layer==0: 
                    return random.choice(worst_action)
                else: return worst_value
        """
        Returns the minimax action using self.depth, self.index and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return minlayer(gameState,0,self.index)
        
