import numpy as np
import pandas as pd
import sys, pickle
import cocoex, cocopp
from solvers import pso, de, cs, ga

output_folder = "PSO_190326"
nfe_base = 1e+6

observer = cocoex.Observer("bbob", "result_folder: " + output_folder)

suite = cocoex.Suite("bbob", "", "function_indices:1,15 dimensions:10,20,40 instance_indices:1-10")
for problem in suite:
    problem.observe_with(observer)
    max_nfe = nfe_base*problem.dimension
    
    pso(200, problem, (problem.lower_bounds[0], problem.upper_bounds[0]), problem.dimension, max_nfe, w=0.32, c1=0.01, c2=1.54)
    
cocopp.main(observer.result_folder)