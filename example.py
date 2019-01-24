import solvers
import testFunctions as tf
from animation import animation, animation3D


alh = solvers.pso(50, 100, 2, tf.ackley_function, -10, 10)
animation(alh.history(), tf.ackley_function, -10, 10)
animation3D(alh.history(), tf.ackley_function, -10, 10)
