import numpy as np

class de():
    """
    Diferencial Evolution
    """
    def __init__(self, n, iteration, dimension, function, lb, ub, beta, pr):
        """
        :param n: number of candidate solutions
        :param iteration: the number of iterations
        :param dimension: space dimension
        :param function: test function
        :param lb: lower bounds
        :param ub: upper bounds
        :param beta: weight for the differential variation during mutation
        :param pr: 0<pr<1; probability of adding an extra allele during exponential crossover
        """
        self._history = []
        
        x = self._generate_initial_solution(lb, ub, n, dimension)
        f = self._evaluate(x, function)
        
        idx_local_best = np.argmax(f)
        self._best_x = x[idx_local_best]
        self._best_f = f[idx_local_best]
        self._history = self._history + [x]
        
        for i in range(iteration):
            x_temp = self._move_solution(x, beta, pr, lb, ub)
            f_temp = self._evaluate(x_temp, function)

            x, f = self._select(x, x_temp, f, f_temp)
            
            idx_local_best = np.argmax(f)
            if f[idx_local_best] >= self._best_f:
                self._best_x = x[idx_local_best]
                self._best_f = f[idx_local_best]
            self._history = self._history + [x]
            
        return
    
    def _generate_initial_solution(self, lb, ub, n, dimension):
        return np.random.uniform(lb, ub, (n, dimension))

    def _move_solution(self, x, beta, pr, lb, ub):
        u = self._mutate(x, beta)
        v = self._exponential_crossover(x, u, pr)
        return np.clip(v, lb, ub)

    def _evaluate(self, x, function):
        return np.array([-function(_) for _ in x])

    def _select(self, x, x_temp, f, f_temp):
        rx = np.empty(x.shape)
        rf = np.empty(x.shape[0])
        for i in range(x.shape[0]):
            if f_temp[i] > f[i]:
                rx[i] = x_temp[i]
                rf[i] = f_temp[i]
            else:
                rx[i] = x[i]
                rf[i] = f[i]
        
        return rx, rf
        
    def _mutate(self, x, beta):
        u = np.empty(x.shape)
        idx = np.arange(x.shape[0])

        for i in range(x.shape[0]):
            j = np.random.choice(np.delete(idx, i), 2, replace=False)
            u[i] = x[i] + beta*(x[j[0]] - x[j[1]])
            
        return u
    
    def _exponential_crossover(self, x, u, pr):
        x_temp = np.empty(x.shape)
        all_points = np.arange(x.shape[1])
        for k in range(x.shape[0]):
            i = np.random.choice(all_points)
            crossover_points = [all_points[i]]

            while pr >= np.random.uniform(0, 1) and len(crossover_points) < x.shape[1]:
                i = (i+1) % x.shape[1]
                crossover_points = crossover_points + [all_points[i]]
                
            x_temp[k] = self._crossover(x[k], u[k], crossover_points)
            
        return x_temp
            
    def _binomial_crossover(self, x, u):
        ## not implemented ##
        return
    
    def _crossover(self, a, b, points):
#         r = [b[i] if i in points else a[i] for i in range(len(a))]
        
        r = [_ for _ in a]
        for i in points:
            r[i] = b[i]

        return r
    
    def best(self):
        return self._best_x, self._best_f
    
    def history(self):
        return self._history