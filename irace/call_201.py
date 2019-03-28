import numpy as np
import cocoex, cocopp
import sys, argparse, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solvers import f201, f203, f251, f253
import pickle 

### interface between the target-runner and the solvers for irace ###

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--nfe'  , dest='nfe'  , type=float, help="Integer   : Number of Function Evaluations")
    parser.add_argument('--n'    , dest='n'    , type=float, help="Integer   : Population size")
    parser.add_argument('--w_1'    , dest='w_1'    , type=float, help="Real value: velocity modifier")
    parser.add_argument('--c1_1'   , dest='c1_1'   , type=float, help="Real value: pbest modifier")
    parser.add_argument('--c2_1'   , dest='c2_1'   , type=float, help="Real value: gbest modifier")
    parser.add_argument('--k'    , dest='k'    , type=float, help="Integer   : Tournament size")
    parser.add_argument('--beta' , dest='beta' , type=float, help="Real value: DE-mutation modifier")
    parser.add_argument('--w_2'    , dest='w_2'    , type=float, help="Real value: velocity modifier")
    parser.add_argument('--c1_2'   , dest='c1_2'   , type=float, help="Real value: pbest modifier")
    parser.add_argument('--c2_2'   , dest='c2_2'   , type=float, help="Real value: gbest modifier")
    parser.add_argument('--bbob', dest='bbob'  , type=str  , help="String    : BBOB suite e.g.:function_indices:1 dimensions:2 instance_indices:1")
    args = parser.parse_args()
    
    file = open("bbob_final_target_fvalue1.pkl",'rb')
    targets = pickle.load(file)
    file.close()
    
    suite = cocoex.Suite("bbob", "", args.bbob)
    fitness = 0
    for problem in suite:
        sol = f201(args.n, problem, (problem.lower_bounds[0], problem.upper_bounds[0]), problem.dimension, args.nfe, args.w_1, args.c1_1, args.c2_1, args.k, args.beta, args.w_2, args.c1_2, args.c2_2)
        
        
        fitness += np.abs(sol.best.getFitness() - targets[problem.id])
    print(fitness)
    return 

if __name__ == "__main__":
   np.warnings.filterwarnings('ignore')
   main(sys.argv[1:])