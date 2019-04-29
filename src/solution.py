import numpy as np
import copy
    
class Solution(object):

    @staticmethod
    def setProblem(function, bounds, dimension, maximize):
        #function related
        Solution.maximize  = maximize
        Solution.function  = function
        Solution.bounds    = bounds
        Solution.dimension = dimension
        Solution.nfe       = 0
        Solution.other_stop_condition = 0
        #common attributes
        Solution.best      = None
        Solution.worst     = None
        Solution.gbest     = None
        
        Solution.sign = 1 if Solution.maximize else -1
        
        #Log
        Solution._log     = None
        Solution.evaluate = Solution._evaluate
        Solution.count_repair = 0
        
    @staticmethod
    def setLogger(Log):
        Solution._log     = Log
        Solution.evaluate = Solution._evaluate_log
        
    @staticmethod
    def closeLogger():
        Solution._log.close()
        Solution._log     = None
        Solution.evaluate = Solution._evaluate
    
    @staticmethod
    def initialize(n):
        return np.array([Solution() for i in range(int(n))])

    def __init__(self):
        #default attributes
        self.x = np.zeros(Solution.dimension)
        self.fitness  = None
        #pso attributes
        self.pbest    = {}#{'x': None, 'fitness': None}
        self.velocity = np.zeros(Solution.dimension)
        
    def setX(self, x):
        self.x        = Solution.repair_x(x, *Solution.bounds)
        if(np.array_equal(self.x, x)):
            Solution.count_repair += 1
            self.velocity = Solution.repair_v(self.velocity, self.x, x, *Solution.bounds)            
        self.clearFitness()
        
    def setVelocity(self, v):
        self.velocity = v

    def getFitness(self):
        if self.fitness == None:
            self.fitness = self.evaluate()
            Solution.updateBest(self)
            Solution.updateWorst(self)
            self.updatePBest()
        return self.fitness
    
    def clearFitness(self):
        self.fitness = None
    
    def _evaluate(self):
        Solution.nfe += 1
        return Solution.function(self.x)
        
    def _evaluate_log(self):
        fitness = self._evaluate()
        Solution._log(Solution.nfe, fitness)
        return fitness
        
    # PSO
    def updatePBest(self):
        if(self.pbest == {} or self.getFitness() >= self.pbest['fitness']):
            self.pbest['x']       = self.x
            # self.pbest['fitness'] = self.getFitness()
            self.pbest['fitness'] = self.fitness
        
    @staticmethod
    def repair_x(x, lb, ub):
        #this method should be replaced on the fly
        return x
        
    @staticmethod
    def repair_v(v, x, x1, lb, ub):
        #this method should be replaced on the fly
        return v
    
    @staticmethod
    def updateBest(Xi):
        if(Solution.best == None or Xi >= Solution.best):
            Solution.best  = copy.deepcopy(Xi)
            Solution.gbest = Solution.best
        return
        
    @staticmethod
    def updateWorst(Xi):
        if(Solution.worst == None or Xi <= Solution.worst):
            Solution.worst  = copy.deepcopy(Xi)
        return    
        
    @staticmethod
    def print(sep="\n"):
        output = "--------------------------------------------"+sep \
        +"FUNCTION:   "+str(Solution.function)         +sep \
        +"MAXIMIZING: "+str(Solution.maximize)         +sep \
        +"BOUNDS:     "+str(Solution.bounds)           +sep \
        +"DIMENSION:  "+str(Solution.dimension)        +sep \
        +"NFE:        "+str(Solution.nfe)              +sep \
        +"BEST FITNESS:  "+str(Solution.best.fitness)  +sep \
        +"WORST FITNESS: "+str(Solution.worst.fitness) +sep \
        +"--------------------------------------------"  
        print(output)
    
    #compare by fitness
    def __lt__(self, other):
        return (Solution.sign) * self.getFitness() < (Solution.sign) * other.getFitness()
        
    def __le__(self, other):
        return (Solution.sign) * self.getFitness() <= (Solution.sign) * other.getFitness()
    
    def __gt__(self, other):
        return (Solution.sign) * self.getFitness() > (Solution.sign) * other.getFitness()
     
    def __ge__(self, other):
        return (Solution.sign) * self.getFitness() >= (Solution.sign) * other.getFitness()