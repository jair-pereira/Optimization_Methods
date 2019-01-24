import solvers
import testFunctions as tf
from animation import animation, animation3D

func = tf.ackley_function
alh = solvers.pso(50, 300, 2, func, -10, 10)
animation(alh.history(), func, -10, 10)
# animation3D(alh.history(), func, -10, 10)
