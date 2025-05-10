import config as config

import pygad
import os

from solver_solution import SolverSolution

from chromosome import Chromosome
from vehicle_trip import VehicleTrip

import matplotlib.pyplot as plt
import numpy
from collections.abc import Callable

def plot_solution(ga_instance: pygad.GA):
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
    y = [solver_solution.solver_input_solutions[4].f(float(xi))/1000 for xi in x]
    plt.plot(x, y)
    x = numpy.arange(0, 1, 1/1000)
    y = [solver_solution.solver_input_solutions[5].f(float(xi))/1000 for xi in x]
    plt.plot(x, y)
    x = numpy.arange(0, 1, 1/1000)
    y = [solver_solution.solver_input_solutions[6].f(float(xi))/1000 for xi in x]
    plt.plot(x, y)
    x = numpy.arange(0, 1, 1/1000)
    y = [solver_solution.solver_input_solutions[7].f(float(xi))/1000 for xi in x]
    plt.plot(x, y)
    x = numpy.arange(0, 1, 1/1000)
    y = [solver_solution.solver_input_solutions[7].f(float(xi))/1000 for xi in x]
    plt.plot(x, y)
    plt.title("Contribution to Fuel Efficiency from Each Independent Variable")
    plt.legend((
        "Date and Time (years)",
        "Odometer (Gm)",
        "Trip Distance (100Km)",
        "Vehicle Temperature (K/273)",
        "Trip Engine Running Time (10Ks [2.78 hours])",
        "Temperature Difference Between Vehicle and Engine Operating (140K)",
        "Average Speed (40m/s)",
        "Time of Day (days)",
        "Time of Year (years)"
    ))
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

def plot_histogram(ga_instance: pygad.GA, vehicle_trips: list[VehicleTrip], number_of_bins: int, calculation: Callable[[SolverSolution, VehicleTrip], float]):
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

    deviations_from_calculation: list[float] = list()
    for vehicle_trip in vehicle_trips:
        deviations_from_calculation.append(calculation(solver_solution, vehicle_trip))

    plt.figure(figsize=config.SOLUTION_FIGURE_SIZE_INCHES)
    plt.hist(deviations_from_calculation, bins=number_of_bins, edgecolor="black")
    plt.ylabel("Frequency")
    plt.grid(True)

def plot_histogram_m_per_l(ga_instance: pygad.GA, vehicle_trips: list[VehicleTrip], number_of_bins: int):

    def calculation(solver_solution: SolverSolution, vehicle_trip: VehicleTrip) -> float:
        estimated_fuel_efficiency_m_per_l: float = solver_solution.f(vehicle_trip)
        deviation_from_calculation: float = estimated_fuel_efficiency_m_per_l - vehicle_trip.fuel_efficiency_m_per_l
        return deviation_from_calculation

    plot_histogram(ga_instance, vehicle_trips, number_of_bins, calculation)

    plt.title("Histogram of Deviations of GA Solution Estimation From Real Trip Fuel Efficiency")
    plt.xlabel("Deviation (m/L)")

def plot_histogram_error_m_per_l(ga_instance: pygad.GA, vehicle_trips: list[VehicleTrip], number_of_bins: int):

    def calculation(solver_solution: SolverSolution, vehicle_trip: VehicleTrip) -> float:
        estimated_fuel_efficiency_m_per_l: float = solver_solution.f(vehicle_trip)
        deviation_from_calculation: float = abs(estimated_fuel_efficiency_m_per_l - vehicle_trip.fuel_efficiency_m_per_l)
        return deviation_from_calculation

    plot_histogram(ga_instance, vehicle_trips, number_of_bins, calculation)

    plt.title("Histogram of Absolute Deviations of GA Solution Estimation From Real Trip Fuel Efficiency")
    plt.xlabel("Absolute Deviation (m/L)")

def plot_histogram_percent_error_m_per_l(ga_instance: pygad.GA, vehicle_trips: list[VehicleTrip], number_of_bins: int):

    def calculation(solver_solution: SolverSolution, vehicle_trip: VehicleTrip) -> float:
        estimated_fuel_efficiency_m_per_l: float = solver_solution.f(vehicle_trip)
        deviation_from_calculation: float = abs(estimated_fuel_efficiency_m_per_l / vehicle_trip.fuel_efficiency_m_per_l) * 100
        return deviation_from_calculation

    plot_histogram(ga_instance, vehicle_trips, number_of_bins, calculation)

    plt.title("Histogram of Absolute Deviations of GA Solution Estimation From Real Trip Fuel Efficiency")
    plt.xlabel("Absolute Deviation (% m/L)")

def plot_histogram_l_per_hundred_km(ga_instance: pygad.GA, vehicle_trips: list[VehicleTrip], number_of_bins: int):

    def calculation(solver_solution: SolverSolution, vehicle_trip: VehicleTrip) -> float:
        estimated_fuel_efficiency_m_per_l: float = solver_solution.f(vehicle_trip)
        estimated_fuel_efficiency_l_per_hundred_km: float = 100000/estimated_fuel_efficiency_m_per_l
        deviation_from_calculation: float = estimated_fuel_efficiency_l_per_hundred_km - vehicle_trip.fuel_efficiency_l_per_hundred_km
        return deviation_from_calculation

    plot_histogram(ga_instance, vehicle_trips, number_of_bins, calculation)

    plt.title("Histogram of Deviations of GA Solution Estimation From Real Trip Fuel Efficiency")
    plt.xlabel("Deviation (L/100Km)")

def plot_histogram_error_l_per_hundred_km(ga_instance: pygad.GA, vehicle_trips: list[VehicleTrip], number_of_bins: int):

    def calculation(solver_solution: SolverSolution, vehicle_trip: VehicleTrip) -> float:
        estimated_fuel_efficiency_m_per_l: float = solver_solution.f(vehicle_trip)
        estimated_fuel_efficiency_l_per_hundred_km: float = 100000/estimated_fuel_efficiency_m_per_l
        deviation_from_calculation: float = abs(estimated_fuel_efficiency_l_per_hundred_km - vehicle_trip.fuel_efficiency_l_per_hundred_km)
        return deviation_from_calculation

    plot_histogram(ga_instance, vehicle_trips, number_of_bins, calculation)

    plt.title("Histogram of Absolute Deviations of GA Solution Estimation From Real Trip Fuel Efficiency")
    plt.xlabel("Absolute Deviation (L/100Km)")

def plot_histogram_percent_error_l_per_hundred_km(ga_instance: pygad.GA, vehicle_trips: list[VehicleTrip], number_of_bins: int):

    def calculation(solver_solution: SolverSolution, vehicle_trip: VehicleTrip) -> float:
        estimated_fuel_efficiency_m_per_l: float = solver_solution.f(vehicle_trip)
        estimated_fuel_efficiency_l_per_hundred_km: float = 100000/estimated_fuel_efficiency_m_per_l
        deviation_from_calculation: float = abs(estimated_fuel_efficiency_l_per_hundred_km / vehicle_trip.fuel_efficiency_l_per_hundred_km) * 100
        return deviation_from_calculation

    plot_histogram(ga_instance, vehicle_trips, number_of_bins, calculation)

    plt.title("Histogram of Absolute Deviations of GA Solution Estimation From Real Trip Fuel Efficiency")
    plt.xlabel("Absolute Deviation (% L/100Km)")


if __name__ == "__main__":
    if (os.path.exists(config.GA_MODEL_FILE+".pkl") and os.path.isfile(config.GA_MODEL_FILE+".pkl")):
        from data_importer import DataImporter

        ga_instance: pygad.GA = pygad.load(config.GA_MODEL_FILE)
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
        print(solver_solution)
        plot_solution(ga_instance)
        vehicle_trips: list[VehicleTrip] = DataImporter(config.DATA_FILE_PATH).vehicle_trips
        plot_histogram_m_per_l(ga_instance, vehicle_trips, 40)
        plot_histogram_error_m_per_l(ga_instance, vehicle_trips, 40)
        plot_histogram_percent_error_m_per_l(ga_instance, vehicle_trips, 40)
        plot_histogram_l_per_hundred_km(ga_instance, vehicle_trips, 40)
        plot_histogram_error_l_per_hundred_km(ga_instance, vehicle_trips, 40)
        plot_histogram_percent_error_l_per_hundred_km(ga_instance, vehicle_trips, 40)
        plt.show()
