import os

import pygad

from chromosome import Chromosome

import config

from time import time_ns

from vehicle_trip import VehicleTrip
from solver_solution import SolverSolution
from data_importer import DataImporter
from display_solution import plot_solution
import matplotlib.pyplot as plt

from math import log2

vehicle_trips: list[VehicleTrip] = DataImporter(config.DATA_FILE_PATH).vehicle_trips
start_time_ns: int = time_ns()
NANOSECONDS_IN_ONE_HOUR = 3600000000000

def check_figure_directory():
    if not os.path.exists(config.SOLUTION_FIGURE_SAVE_DIRECTORY):
        os.makedirs(config.SOLUTION_FIGURE_SAVE_DIRECTORY)
    assert os.path.exists(config.SOLUTION_FIGURE_SAVE_DIRECTORY)
    if not os.path.isdir(config.SOLUTION_FIGURE_SAVE_DIRECTORY):
        raise Exception("Could not create the solution figure save directory as a file with the path name exists")

def fitness(ga_instance: pygad.GA, chromosome: Chromosome, solution_idx: int) -> float:
    """test the given chromosome and return a fitness score to be maximized

    Args:
        ga_instance (pygad.GA): pygad.GA instance
        chromosome (Chromosome): chromosome to use for the controller fuzzy system
        solution_idx (int): the solution index from the ga_instance

    Returns:
        float: fitness score to be maximized
    """
    chromosome_list: list[float] = list(chromosome) # type: ignore
    solution_parameters: list[tuple[float, ...]] = list()
    for _ in range(config.NUMBER_OF_VARIABLES):
        solver_input_solution_genes: tuple[float, ...] = tuple([chromosome_list.pop() for _ in range(config.GENES_PER_VARIABLE)])
        solution_parameters.append(solver_input_solution_genes)
    assert len(chromosome_list) == 0
    solver_solution: SolverSolution = SolverSolution(tuple(solution_parameters))

    fitness_scores: list[float] = list()
    differences_m_per_l: list[float] = list()

    for vehicle_trip in vehicle_trips:
        estimated_fuel_efficiency_m_per_l: float = solver_solution.f(vehicle_trip)
        fitness: float = solver_solution.fitness(vehicle_trip)
        fitness_scores.append(fitness)
        difference_m_per_l: float = abs(vehicle_trip.fuel_efficiency_m_per_l - estimated_fuel_efficiency_m_per_l)
        differences_m_per_l.append(difference_m_per_l)

    #average_fitness: float = sum(fitness_scores)/len(fitness_scores)
    average_difference_m_per_l: float = sum(differences_m_per_l)/len(differences_m_per_l)
    average_fitness: float = log2(1 / average_difference_m_per_l)

    fitness_scores.sort()
    #median_fitness: float = fitness_scores[int(len(fitness_scores)/2)]
    differences_m_per_l.sort()
    median_difference_m_per_l: float = differences_m_per_l[int(len(differences_m_per_l)/2)]
    median_fitness: float = log2(1 / median_difference_m_per_l)

    return average_fitness

def on_generation(ga_instance: pygad.GA):
    ga_instance.save(config.GA_MODEL_FILE)
    generations_per_hour: float = ga_instance.generations_completed / ((time_ns() - start_time_ns) / NANOSECONDS_IN_ONE_HOUR)
    print("Generation {:d} completed ({:.2f} generations / hour)".format(ga_instance.generations_completed, generations_per_hour))
    print("Fitness of best solution: {:.2f}".format(ga_instance.best_solution(ga_instance.last_generation_fitness)[1]))

    best_chromosome: Chromosome = ga_instance.last_generation_elitism # type: ignore
    assert best_chromosome is not None
    best_chromosome_list: list[float] = best_chromosome.tolist()[0]
    solver_solution = SolverSolution((
        tuple(best_chromosome_list[0:config.GENES_PER_VARIABLE]),
        tuple(best_chromosome_list[config.GENES_PER_VARIABLE:config.GENES_PER_VARIABLE*2]),
        tuple(best_chromosome_list[config.GENES_PER_VARIABLE*2:config.GENES_PER_VARIABLE*3]),
        tuple(best_chromosome_list[config.GENES_PER_VARIABLE*3:config.GENES_PER_VARIABLE*4]),
        tuple(best_chromosome_list[config.GENES_PER_VARIABLE*4:config.GENES_PER_VARIABLE*5]),
        tuple(best_chromosome_list[config.GENES_PER_VARIABLE*5:config.GENES_PER_VARIABLE*6]),
        tuple(best_chromosome_list[config.GENES_PER_VARIABLE*6:config.GENES_PER_VARIABLE*7]),
        tuple(best_chromosome_list[config.GENES_PER_VARIABLE*7:config.GENES_PER_VARIABLE*8]),
        tuple(best_chromosome_list[config.GENES_PER_VARIABLE*8:config.GENES_PER_VARIABLE*9])
    )) # type: ignore
    fitness_scores: list[float] = list()
    for vehicle_trip in vehicle_trips:
        fitness: float = solver_solution.difference_in_l_per_hundred_km(vehicle_trip)
        fitness_scores.append(fitness)
    average_fitness: float = sum(fitness_scores)/len(fitness_scores)
    print("Average difference in L/100Km of best solution {:.2f}".format(average_fitness))
    plot_solution(ga_instance)
    check_figure_directory()
    figure_save_path: str = os.path.join(config.SOLUTION_FIGURE_SAVE_DIRECTORY, "{}{:08d}.png".format(config.SOLUTION_FIGURE_SAVE_NAME_PREFIX, ga_instance.generations_completed-1))
    assert not os.path.exists(figure_save_path)
    plt.savefig(figure_save_path, dpi=config.SOLUTION_FIGURE_RESOLUTION_DPI)
    plt.close("all")

    if check_stop_flag():
        print("Detected change in stop flag file, ending")
        ga_instance.plot_fitness()
        exit(1)

def create_stop_flag_file():
    """creates the flag file or empties it if it exists
    this file can be used to safely stop the genetic learner once the current generation completes,
    simply by adding any text into the file
    """
    with open(config.GA_STOP_FLAG_FILE, "w"):
        pass
    assert (os.stat(config.GA_STOP_FLAG_FILE).st_size == 0)
    
    return

def check_stop_flag() -> bool:
    if (
        not os.path.exists(config.GA_STOP_FLAG_FILE)
        or os.stat(config.GA_STOP_FLAG_FILE).st_size > 0
    ):
        # if flag file was deleted or modified
        return True
    return False

def run_genetic_algorithm():
    create_stop_flag_file()
    if (
        os.path.exists(config.GA_MODEL_FILE+".pkl")
        and os.path.isfile(config.GA_MODEL_FILE+".pkl")
    ):
        print("Continuing training from saved state")
        ga_instance: pygad.GA = pygad.load(config.GA_MODEL_FILE)
        # reset functions to prevent pickling error
        ga_instance.fitness_func = fitness
        ga_instance.on_generation = on_generation
        print("Saved state loaded from file")
    else:
        print("Save file not found,\nRestarting training from scratch")
        ga_instance: pygad.GA = pygad.GA(
            num_generations=config.GA_GENERATION_GOAL,
            num_parents_mating=config.GA_NUMBER_OF_PARENTS,
            fitness_func=fitness,
            sol_per_pop=config.GA_POPULATION_SIZE,
            num_genes=config.GA_CHROMOSOME_LENGTH,
            on_generation=on_generation,
            mutation_num_genes=config.GA_NUMBER_OF_GENES_TO_MUTATE,
            gene_type=float,
            gene_space={"low": 0, "high": 1},
            parallel_processing=["process", config.GA_NUMBER_OF_THREADS] if config.GA_NUMBER_OF_THREADS > 1 else None
        )

    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
    print(f"Parameters of the best solution : {solution}")
    print(f"Fitness value of the best solution = {solution_fitness}")
    print(f"Index of the best solution : {solution_idx}")
    ga_instance.save(config.GA_MODEL_FILE)
    ga_instance.plot_fitness()


if __name__ == "__main__":
    run_genetic_algorithm()

# TODO: split dataset into chunks, train 
