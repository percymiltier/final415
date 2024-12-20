# myTeam.py
# ---------
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

import random

import util
from capture import GameState
from captureAgents import CaptureAgent
from game import Action
from game import Directions

#################
# Team creation #
#################

# Team 2 Members:
# Percy Miltier
#
#
#

def createTeam(firstIndex, secondIndex, isRed,
               first = 'offensiveAgent', second = 'defensiveAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class agentBase(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState: GameState) -> None:
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    # get the agent position
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState: GameState) -> Action:
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)

  def nullHeuristic(state, problem=None):
      """
      A heuristic function estimates the cost from the current state to the nearest
      goal in the provided SearchProblem.  This heuristic is trivial.
      """
      return 0

  def aStarSearch(problem, heuristic=nullHeuristic):
      """
      Search the node that has the lowest combined cost and heuristic first.
      """
      "*** YOUR CODE HERE ***"
      #print("Start:", problem.getStartState())
      #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
      #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
      
      # Initialization: Frontier is a priority queue, add start state
      frontier = util.PriorityQueue()
      frontier.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem))
      
      visited = {}
      
      while not frontier.isEmpty():
          state, path, currentCost = frontier.pop()
          
          if problem.isGoalState(state):
              return path
          
          if state not in visited or currentCost < visited[state]:
              visited[state] = currentCost
              
              for successor, action, stepCost in problem.getSuccessors(state):
                  newCost = currentCost + stepCost
                  heuristicCost = newCost + heuristic(successor, problem)
                  
                  frontier.push((successor, path+[action], newCost), heuristicCost)
      
      return []

class offensiveAgent(agentBase):
  def chooseAction(self, gameState: GameState) -> Action:
    # placeholder for defensive implementation of choosing an action
    actions = gameState.getLegalActions(self.index)
    return random.choice(actions)

class defensiveAgent(agentBase):
  def chooseAction(self, gameState: GameState) -> Action:
    # placeholder for defensive implementation of choosing an action
    actions = gameState.getLegalActions(self.index)

    # Get current position of the agent
    myPos = gameState.getAgentPosition(self.index)

    # Get opponent positions
    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    invaders = [enemy for enemy in enemies if enemy.isPacman and enemy.getPosition() is not None]

    # If there are invaders, target the closest one
    if invaders:
        invader_positions = [invader.getPosition() for invader in invaders]
        closest_invader = min(invader_positions, key=lambda pos: self.getMazeDistance(myPos, pos))
        return self.moveToTarget(gameState, closest_invader)

    # If no invaders, patrol the defensive zone
    else:
        foodDefending = self.getFoodYouAreDefending(gameState).asList()
        if foodDefending:
            # Patrol the closest food in the defensive zone
            closest_food = min(foodDefending, key=lambda pos: self.getMazeDistance(myPos, pos))
            return self.moveToTarget(gameState, closest_food)

    # Default: Choose a random action if no other goal
    return random.choice(actions)

  def moveToTarget(self, gameState: GameState, target: tuple) -> Action:
      """
      Moves towards a specified target using a basic greedy approach.
      """
      actions = gameState.getLegalActions(self.index)
      best_action = None
      shortest_distance = float('inf')

      for action in actions:
          successor = self.getSuccessor(gameState, action)
          newPos = successor.getAgentPosition(self.index)
          distance = self.getMazeDistance(newPos, target)

          if distance < shortest_distance:
              shortest_distance = distance
              best_action = action

      return best_action

  def getSuccessor(self, gameState: GameState, action: Action) -> GameState:
      """
      Finds the next successor which is a grid position (location tuple).
      """
      return gameState.generateSuccessor(self.index, action)
