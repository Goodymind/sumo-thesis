import numpy as np
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.core.problem import Problem
from pymoo.optimize import minimize

rng = np.random.default_rng()  # remove later for SUMO


class TrafficLightProblem(Problem):
    def __init__(self):
        # n_var -> number of elements in the vector
        # n_obj -> number of objectives (our score function only returns 1 number)
        # xl -> lower bound of duration
        # xu -> upper bound of duration
        super().__init__(n_var=4, n_obj=1, xl=0, xu=90)

    def _evaluate(self, x, out, *arg, **kwargs):
        out["F"] = rng.random(x.shape[0])


problem = TrafficLightProblem()

algorithm = PSO()

res = minimize(problem, algorithm, seed=1, verbose=False)

print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
