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
        tuple(best_chromosome_list[0:40]),
        tuple(best_chromosome_list[40:40*2]),
        tuple(best_chromosome_list[40*2:40*3]),
        tuple(best_chromosome_list[40*3:40*4]),
        tuple(best_chromosome_list[40*4:40*5])
    )) # type: ignore

    plt.figure(figsize=config.SOLUTION_FIGURE_SIZE_INCHES)
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
    plt.xticks(numpy.arange(0, 1.5, 0.2), minor = False)
    plt.xticks(numpy.arange(0, 1.5, 0.1), minor = True)
    plt.yticks(numpy.arange(-50, 51, 10), minor = False)
    plt.yticks(numpy.arange(-50, 51, 5), minor = True)
    plt.grid(True, "major", "y", linewidth = 2, alpha = 0.5)
    plt.grid(True, "minor", "y", linewidth = 2, alpha = 0.1)
    plt.grid(True, "major", "x", linewidth = 2, alpha = 0.5)
    plt.grid(True, "minor", "x", linewidth = 2, alpha = 0.1)


if __name__ == "__main__":
    if (os.path.exists(config.GA_MODEL_FILE+".pkl") and os.path.isfile(config.GA_MODEL_FILE+".pkl")):
        ga_instance: pygad.GA = pygad.load(config.GA_MODEL_FILE)
        best_chromosome: Chromosome = ga_instance.last_generation_elitism # type: ignore
        assert best_chromosome is not None

        best_chromosome_list: list[float] = best_chromosome.tolist()[0]
        solver_solution = SolverSolution((
            tuple(best_chromosome_list[0:40]),
            tuple(best_chromosome_list[40:40*2]),
            tuple(best_chromosome_list[40*2:40*3]),
            tuple(best_chromosome_list[40*3:40*4]),
            tuple(best_chromosome_list[40*4:40*5])
        )) # type: ignore
        print(solver_solution)
        plot_solution(ga_instance)
        plt.show()
