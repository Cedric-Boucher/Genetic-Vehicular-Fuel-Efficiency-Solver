import os

import pygad

from chromosome import Chromosome

import config

from time import time_ns

from vehicle_trip import VehicleTrip
from solver_solution import SolverSolution
from data_importer import DataImporter

vehicle_trips: list[VehicleTrip] = DataImporter(config.DATA_FILE_PATH).vehicle_trips
start_time_ns: int = time_ns()
NANOSECONDS_IN_ONE_MINUTE = 60000000000

def fitness(ga_instance: pygad.GA, chromosome: Chromosome, solution_idx: int) -> float:
    """test the given chromosome and return a fitness score to be maximized

    Args:
        ga_instance (pygad.GA): pygad.GA instance
        chromosome (Chromosome): chromosome to use for the controller fuzzy system
        solution_idx (int): the solution index from the ga_instance

    Returns:
        float: fitness score to be maximized
    """
    solver_solution = SolverSolution((
        tuple(chromosome[0:39]),
        tuple(chromosome[39:39*2]),
        tuple(chromosome[39*2:39*3]),
        tuple(chromosome[39*3:39*4]),
        tuple(chromosome[39*4:39*5])
    ))

    fitness_scores: list[float] = list()

    for vehicle_trip in vehicle_trips:
        fitness: float = solver_solution.fitness(vehicle_trip)
        fitness_scores.append(fitness)

    average_fitness: float = sum(fitness_scores)/len(fitness_scores)

    return average_fitness

def on_generation(ga_instance: pygad.GA):
    ga_instance.save(config.GA_MODEL_FILE)
    generations_per_minute: float = ga_instance.generations_completed / ((time_ns() - start_time_ns) / NANOSECONDS_IN_ONE_MINUTE)
    print("Generation {:d} completed ({:.2f} generations / minute)".format(ga_instance.generations_completed, generations_per_minute))
    print("Fitness of best solution: {:.2f}".format(ga_instance.best_solution(ga_instance.last_generation_fitness)[1]))
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
