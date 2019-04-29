import numpy as np
from src import *

##### INIT #####
def t_repair_random():
    n_test = 0
    result = 0
    
    n  = np.random.randint(10,100)
    ub = np.random.randint(1,100)
    lb = -ub
    dimension = np.random.randint(1,100)

    X = [op.init_random(lb, ub, dimension) for i in range(n)]
    #does it repair what is within bounds? it should not
    U = [op.repair_random(Xi, lb, ub) for Xi in X]
    result += sum([sum(X[i] == U[i])/dimension for i in range(n)]) == n
    n_test+=1
    
    #does it repair what is out of bounds? it should
    U = [op.repair_random(Xi, lb*5, lb*2) for Xi in X]
    result += sum([sum(X[i] != U[i])/dimension for i in range(n)]) == n
    n_test+=1
    
    return result == n_test
    
def t_repair_truncate():
    n_test = 0
    result = 0
    
    n  = np.random.randint(10,100)
    ub = np.random.randint(1,100)
    lb = -ub
    dimension = np.random.randint(1,100)

    X = [op.init_random(lb, ub, dimension) for i in range(n)]
    #does it repair what is within bounds? it should not
    U = [op.repair_truncate(Xi, lb, ub) for Xi in X]
    result += sum([sum(X[i] == U[i])/dimension for i in range(n)]) == n
    n_test+=1
    
    #does it repair what is out of bounds? it should
    U = [op.repair_truncate(Xi, lb*5, lb*2) for Xi in X]
    result += sum([sum(X[i] != U[i])/dimension for i in range(n)]) == n
    n_test+=1
    
    #is the repaired values correct? it should be equal to lb or ub
    result += sum(sum([U[i] for i in range(n)])/dimension)/n == lb
    n_test+=1
    
    return result == n_test

result = t_repair_random() + t_repair_truncate()    
print(result)