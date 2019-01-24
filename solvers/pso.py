import numpy as np

class pso():
    """
    Particle Swarm Optmization
    """
    def __init__(self, n, iteration, dimension, function, lb, ub, w=0.5, c1=1, c2=1):
        """
        :param n: number of candidate solutions
        :param iteration: the number of iterations
        :param dimension: space dimension
        :param function: test function
        :param lb: lower bounds
        :param ub: upper bounds
        :param w: inertia weight, balances exploration (large values) and exploitation (small values)
        :param c1: cognitive component, tendency of a particle to go towards its own best
        :param c2: social component, tendency of a particle to go towards the swarms best
        """
        self._history = []
        
        x = self._generate_initial_solution(lb, ub, n, dimension)
        f = self._evaluate(x, function)
        
        idx_local_best = np.argmax(f)
        self._best_x = x[idx_local_best]
        self._best_f = f[idx_local_best]
        self._history = self._history + [x]
        
        #local best
        pbest_x = np.array([i for i in x])
        pbest_f = np.array([i for i in f])
        
        velocity = np.zeros(x.shape)
        
        for i in range(iteration):
            x = self._move_solution(x, f, pbest_x, pbest_f, lb, ub, velocity, w, c1, c2)
            f = self._evaluate(x, function)
            
            #update gbest
            idx_local_best = np.argmax(f)
            if f[idx_local_best] >= self._best_f:
                self._best_x = x[idx_local_best]
                self._best_f = f[idx_local_best]
            self._history = self._history + [x]
            
        return
    
    def _generate_initial_solution(self, lb, ub, n, dimension):
        return np.random.uniform(lb, ub, (n, dimension))

    def _move_solution(self, x, f, pbest_x, pbest_f, lb, ub, velocity, w, c1, c2):
        pbest_x, pbest_f = self._update_pbest(x, f, pbest_x, pbest_f)
        
        velocity = self._update_velocity(x, f, pbest_x, pbest_f, velocity, w, c1, c2)
        
        #update position
        u = velocity + x
        
        return np.clip(u, lb, ub)

    def _evaluate(self, x, function):
        return np.array([-function(i) for i in x])
   
    def _update_pbest(self, x, f, pbest_x, pbest_f):
        idx = [i for i in range(f.shape[0]) if f[i] >= pbest_f[i]]

        pbest_x[idx] = x[idx]
        pbest_f[idx] = f[idx]
    
        return pbest_x, pbest_f
    
    def _update_velocity(self, x, f, pbest_x, pbest_f, v, w, c1, c2):
        r1 = np.random.random(x.shape)
        r2 = np.random.random(x.shape)

        return w*v + c1*r1*(pbest_x - x) + c2*r2*(self._best_x - x)
    
    
    def best(self):
        return self._best_x, self._best_f
    
    def history(self):
        return self._history