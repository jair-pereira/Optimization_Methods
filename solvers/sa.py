import numpy as np

class sa():
    """
    Simulated Annealing
    """
    def __init__(self, n, dimension, function, lb, ub, T=[1, 0.1, 0.05]):
        """
        :param n: number of candidate solutions
        :param dimension: space dimension
        :param function: test function
        :param lb: lower bounds
        :param ub: upper bounds
        :param iteration: the number of iterations
        :param T: list of decreasing temperatures
        """
        self._history = []
        
        x = self._generate_initial_solution(lb, ub, n, dimension)
        f = self._evaluate(x, function)
        
        idx_local_best = np.argmax(f)
        self._best_x = x[idx_local_best]
        self._best_f = f[idx_local_best]
        self._history = self._history + [x]
        
        for t in T:
            x_temp = self._move_solution(x, lb, ub)
            f_temp = self._evaluate(x_temp, function)

            x, f = self._select(x, x_temp, f, f_temp, t)
#             f = self._evaluate(x, function)
            
            idx_local_best = np.argmax(f)
            if f[idx_local_best] >= self._best_f:
                self._best_x = x[idx_local_best]
                self._best_f = f[idx_local_best]
            self._history = self._history + [x]
            
        return
    
    def _generate_initial_solution(self, lb, ub, n, dimension):
        return np.random.uniform(lb, ub, (n, dimension))

    def _move_solution(self, x, lb, ub):
        u = np.random.uniform(-1, +1, x.shape)
        return np.clip(x+u, lb, ub)

    def _evaluate(self, x, function):
        return np.array([-function(i) for i in x])

    def _select(self, x, x_temp, f, f_temp, t):
#         r = np.array([x_temp[i] if f_temp[i] > f[i] or np.random.uniform(0, 1) <= np.exp(-((f_temp[i]-f[i]))/t) 
#              else x[i] for i in range(len(f))])
#         return r

        rx = np.empty(x.shape)
        rf = np.empty(x.shape[0])
        for i in range(x.shape[0]):
            acceptance_probability = np.exp(-((f_temp[i]-f[i]))/t)
            if f_temp[i] > f[i] or np.random.uniform(0, 1) <= acceptance_probability:
                rx[i] = x_temp[i]
                rf[i] = f_temp[i]
            else:
                rx[i] = x[i]
                rf[i] = f[i]
        
        return rx, rf


    def temperature_exp(t0, rate, n):
        """
        :param t0: initial temperature
        :param rate: 0<rate<1; rate which the temperature will be decreased
        :param n: size of the curve
        """
        return np.array([t0*(rate**i) for i in range(n)])

    def temperature_lin(t0, rate):
        """
        :param t0: initial temperature
        :param rate: rate which the temperature will be decreased untill 0
        """
        n = int(t0/rate)+1
        return np.array([t0 - (rate*i) for i in range(n)])
    
    def best(self):
        return self._best_x, self._best_f
    
    def history(self):
        return self._history