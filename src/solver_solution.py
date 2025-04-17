from solver_input_solution import SolverInputSolution, SolverFloats
from vehicle_trip import VehicleTrip
from datetime import datetime, timedelta
from math import log2

AllSolverFloats = tuple[SolverFloats, ...]

t0: datetime = datetime(2024, 7, 26)
seconds_in_a_day: int = 86400

class SolverSolution:
    """
    Represents a potential solution that the solver has generated for the entire input space,
    which is to say, all input variables. This consists of a SolverInputSolution for each input.
    """
    def __init__(self, all_solution_parameters: AllSolverFloats):
        self.__solver_input_solutions: tuple[SolverInputSolution, ...] = tuple([
            SolverInputSolution(solution_parameters) for solution_parameters in all_solution_parameters
        ])

    @property
    def all_solution_parameters(self) -> AllSolverFloats:
        return tuple([sis.solution_parameters for sis in self.__solver_input_solutions])

    def f(self, vehicle_trip: VehicleTrip) -> float:
        """
        returns calculated / estimated vehicle trip efficiency
        based on the inputs in the provided vehicle trip and the solver solution parameters
        """
        y: float = (
            self.__solver_input_solutions[0].f((vehicle_trip.date_and_time - t0).total_seconds() / seconds_in_a_day) +
            self.__solver_input_solutions[1].f(vehicle_trip.odometer_m) +
            self.__solver_input_solutions[2].f(vehicle_trip.trip_distance_m) +
            self.__solver_input_solutions[3].f(vehicle_trip.vehicle_temperature_kelvin) +
            self.__solver_input_solutions[4].f(vehicle_trip.trip_engine_running_time_s)
        )

        assert isinstance(y, float)
        return y

    def fitness(self, vehicle_trip: VehicleTrip) -> float:
        """
        returns a fitness score for how well this SolverSolution fits the actual fuel efficiency of this trip,
        higher number means better fit
        """
        estimated_fuel_efficiency_m_per_l: float = self.f(vehicle_trip)
        diff: float = abs(vehicle_trip.fuel_efficiency_m_per_l - estimated_fuel_efficiency_m_per_l)
        try:
            fitness: float = log2(1 / diff) # to make higher number a better fit rather than vice versa
        except ValueError:
            fitness: float = -1000
        return fitness

if __name__ == "__main__":
    from random import random
    test = SolverSolution((
        tuple(random() for _ in range(39)),
        tuple(random() for _ in range(39)),
        tuple(random() for _ in range(39)),
        tuple(random() for _ in range(39)),
        tuple(random() for _ in range(39))
    )) # type: ignore
    vehicle_trip = VehicleTrip()
    vehicle_trip.date_and_time = datetime(2025, 1, 1)
    vehicle_trip.odometer_km = 123456
    vehicle_trip.trip_distance_km = 8.5
    vehicle_trip.vehicle_temperature_celsius = 10
    vehicle_trip.trip_engine_running_time_m = 11.32
    vehicle_trip.fuel_efficiency_l_per_hundred_km = 7.1
    print(test.fitness(vehicle_trip))

# issue: need to normalize "x" for each input to "f(x)"
