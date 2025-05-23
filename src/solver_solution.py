from solver_input_solution import SolverInputSolution, SolverFloats
from vehicle_trip import VehicleTrip
from datetime import datetime
from math import log2
import config

AllSolverFloats = tuple[SolverFloats, ...]

class SolverSolution:
    """
    Represents a potential solution that the solver has generated for the entire input space,
    which is to say, all input variables. This consists of a SolverInputSolution for each input.
    """
    def __init__(self, all_solution_parameters: AllSolverFloats):
        assert len(all_solution_parameters) == config.NUMBER_OF_VARIABLES
        self.__solver_input_solutions: tuple[SolverInputSolution, ...] = tuple([
            SolverInputSolution(solution_parameters) for solution_parameters in all_solution_parameters
        ])

    @property
    def all_solution_parameters(self) -> AllSolverFloats:
        return tuple([sis.solution_parameters for sis in self.__solver_input_solutions])

    @property
    def solver_input_solutions(self) -> tuple[SolverInputSolution, ...]:
        return self.__solver_input_solutions

    def f(self, vehicle_trip: VehicleTrip) -> float:
        """
        returns calculated / estimated vehicle trip efficiency
        based on the inputs in the provided vehicle trip and the solver solution parameters
        """
        y: float = (
            self.__solver_input_solutions[0].f(vehicle_trip.normalized_time_since_t0) +
            self.__solver_input_solutions[1].f(vehicle_trip.normalized_odometer) +
            self.__solver_input_solutions[2].f(vehicle_trip.normalized_trip_distance) +
            self.__solver_input_solutions[3].f(vehicle_trip.normalized_vehicle_temperature) +
            self.__solver_input_solutions[4].f(vehicle_trip.normalized_trip_engine_running_time) +
            self.__solver_input_solutions[5].f(vehicle_trip.normalized_temperature_difference_between_vehicle_and_engine_operating) +
            self.__solver_input_solutions[6].f(vehicle_trip.normalized_trip_average_speed) +
            self.__solver_input_solutions[7].f(vehicle_trip.normalized_time_of_day) +
            self.__solver_input_solutions[8].f(vehicle_trip.normalized_time_of_year)
        )

        assert isinstance(y, float)
        return y

    def fitness(self, vehicle_trip: VehicleTrip) -> float:
        """
        returns a fitness score for how well this SolverSolution fits the actual fuel efficiency of this trip,
        higher number means better fit
        """
        estimated_fuel_efficiency_m_per_l: float = self.f(vehicle_trip)
        diff: float = abs(vehicle_trip.fuel_efficiency_m_per_l - estimated_fuel_efficiency_m_per_l) # FIXME: compare to normalized fuel efficiency instead?
        try:
            fitness: float = log2(1 / diff) # to make higher number a better fit rather than vice versa
        except ValueError:
            fitness: float = -1000
        return fitness

    def difference_in_l_per_hundred_km(self, vehicle_trip: VehicleTrip) -> float:
        estimated_fuel_efficiency_m_per_l: float = self.f(vehicle_trip)
        estimated_fuel_efficiency_l_per_hundred_km: float = 100000/estimated_fuel_efficiency_m_per_l
        diff: float = abs(vehicle_trip.fuel_efficiency_l_per_hundred_km - estimated_fuel_efficiency_l_per_hundred_km)
        return diff

    def __str__(self) -> str:
        display: str = str(
            "Date and Time:\n"
            "{}\n"
            "Odometer:\n"
            "{}\n"
            "Trip Distance:\n"
            "{}\n"
            "Vehicle Temperature:\n"
            "{}\n"
            "Trip Engine Running Time:\n"
            "{}\n"
            "Temperature Difference Between Vehicle and Engine Operating:\n"
            "{}\n"
            "Trip Average Speed:\n"
            "{}\n"
            "Time of Day:\n"
            "{}\n"
            "Time of Year:\n"
            "{}"
        ).format(
            str(self.__solver_input_solutions[0]),
            str(self.__solver_input_solutions[1]),
            str(self.__solver_input_solutions[2]),
            str(self.__solver_input_solutions[3]),
            str(self.__solver_input_solutions[4]),
            str(self.__solver_input_solutions[5]),
            str(self.__solver_input_solutions[6]),
            str(self.__solver_input_solutions[7]),
            str(self.__solver_input_solutions[8])
        )

        return display

if __name__ == "__main__":
    from random import random
    test = SolverSolution((
        tuple(random() for _ in range(config.GENES_PER_VARIABLE)),
        tuple(random() for _ in range(config.GENES_PER_VARIABLE)),
        tuple(random() for _ in range(config.GENES_PER_VARIABLE)),
        tuple(random() for _ in range(config.GENES_PER_VARIABLE)),
        tuple(random() for _ in range(config.GENES_PER_VARIABLE)),
        tuple(random() for _ in range(config.GENES_PER_VARIABLE)),
        tuple(random() for _ in range(config.GENES_PER_VARIABLE)),
        tuple(random() for _ in range(config.GENES_PER_VARIABLE)),
        tuple(random() for _ in range(config.GENES_PER_VARIABLE))
    )) # type: ignore
    vehicle_trip = VehicleTrip()
    vehicle_trip.date_and_time = datetime(2025, 1, 1)
    vehicle_trip.odometer_km = 123456
    vehicle_trip.trip_distance_km = 8.5
    vehicle_trip.vehicle_temperature_celsius = 10
    vehicle_trip.trip_engine_running_time_m = 11.32
    vehicle_trip.fuel_efficiency_l_per_hundred_km = 7.1
    print(test.fitness(vehicle_trip))
