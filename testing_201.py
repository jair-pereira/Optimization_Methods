import numpy as np
import pandas as pd
import sys, pickle, datetime
import cocoex, cocopp
from solvers import ge_190320_01, ge_190320_02, ge_190320_03, ge_190325_01, ge_190325_03

output_folder = "GE190320_01_190327"
nfe_base = 1e+5

observer = cocoex.Observer("bbob", "result_folder: " + output_folder)

suite = cocoex.Suite("bbob", "", "function_indices:1,15 dimensions:10,20,40 instance_indices:1-10")
for problem in suite:
    problem.observe_with(observer)
    max_nfe = nfe_base*problem.dimension
    
    ge_190320_01(100, problem, (problem.lower_bounds[0], problem.upper_bounds[0]), problem.dimension, max_nfe)
    
    print(problem.id, " finished at ",datetime.datetime.now())
    
cocopp.main(observer.result_folder)