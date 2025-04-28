import config as config

import pygad
import os

from solver_solution import SolverSolution

from chromosome import Chromosome

import matplotlib.pyplot as plt
import numpy

def plot_solution(ga_instance: pygad.GA):
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

    x = numpy.arange(0, 1, 1/1000)
    y = [solver_solution.solver_input_solutions[0].f(float(xi))/1000 for xi in x]
    plt.plot(x, y)
    x = numpy.arange(0, 1, 1/1000)
    y = [solver_solution.solver_input_solutions[1].f(float(xi))/1000 for xi in x]
    plt.plot(x, y)
    x = numpy.arange(0, 1, 1/1000)
    y = [solver_solution.solver_input_solutions[2].f(float(xi*10))/1000 for xi in x]
    plt.plot(x, y)
    x = numpy.arange(0.5, 1.5, 1/1000)
    y = [solver_solution.solver_input_solutions[3].f(float(xi))/1000 for xi in x]
    plt.plot(x, y)
    x = numpy.arange(0, 1, 1/1000)
    y = [solver_solution.solver_input_solutions[4].f(float(xi*10))/1000 for xi in x]
    plt.plot(x, y)
    plt.legend(("Date and Time (years)", "Odometer (Gm)", "Trip Distance (100Km)", "Vehicle Temperature (K/273)", "Trip Engine Running Time (10Ks [2.78 hours])"))
    plt.ylabel("Contribution to Fuel Efficiency (Km/L)")
    plt.ylim((-50, 50))

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
    plot_solution(ga_instance)
    plt.show()
