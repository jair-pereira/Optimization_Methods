import numpy as np
import cocoex, cocopp
import sys, argparse, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solvers import f281
import pickle 

### interface between the target-runner and the solvers for irace ###

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--nfe'  , dest='nfe'  , type=float, help="Integer   : Number of Function Evaluations")
    parser.add_argument('--n'    , dest='n'    , type=float, help="Integer   : Population size")
    parser.add_argument('--k_1'    , dest='k_1'    , type=float, help="Integer   : Tournament size")
    parser.add_argument('--k_2'    , dest='k_2'    , type=float, help="Integer   : Tournament size")
    parser.add_argument('--beta' , dest='beta' , type=float, help="Real value: DE-mutation modifier")
    parser.add_argument('--bbob', dest='bbob'  , type=str  , help="String    : BBOB suite e.g.:function_indices:1 dimensions:2 instance_indices:1")
    args = parser.parse_args()
    
    file = open("bbob_final_target_fvalue1.pkl",'rb')
    targets = pickle.load(file)
    file.close()
    
    suite = cocoex.Suite("bbob", "", args.bbob)
    fitness = 0
    for problem in suite:
        sol = f281(int(args.n), problem, (problem.lower_bounds[0], problem.upper_bounds[0]), problem.dimension, int(args.nfe), args.k_1, args.k_2, args.beta)
        fitness += np.abs(sol.best.getFitness() - targets[problem.id])
    print(fitness)
    return 

if __name__ == "__main__":
   np.warnings.filterwarnings('ignore')
   main(sys.argv[1:])