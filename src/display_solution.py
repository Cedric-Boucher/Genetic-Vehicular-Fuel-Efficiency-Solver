import config as config

import pygad
import os

from solver_solution import SolverSolution

from chromosome import Chromosome

if (os.path.exists(config.GA_MODEL_FILE+".pkl") and os.path.isfile(config.GA_MODEL_FILE+".pkl")):
    ga_instance: pygad.GA = pygad.load(config.GA_MODEL_FILE)
    best_chromosome: Chromosome = ga_instance.last_generation_elitism # type: ignore
    assert best_chromosome is not None

    best_chromosome_list: list[float] = best_chromosome.tolist()[0]
    solver_solution = SolverSolution((
        tuple(best_chromosome_list[0:39]),
        tuple(best_chromosome_list[39:39*2]),
        tuple(best_chromosome_list[39*2:39*3]),
        tuple(best_chromosome_list[39*3:39*4]),
        tuple(best_chromosome_list[39*4:39*5])
    )) # type: ignore
    print(solver_solution)
