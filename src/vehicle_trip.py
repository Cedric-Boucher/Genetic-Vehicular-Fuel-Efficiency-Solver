from datetime import datetime, time

DATE_AND_TIME_S_NORMALIZATION_FACTOR: int = 31557600 # seconds in a year
ODOMETER_M_NORMALIZATION_FACTOR: int = 1000000000 # 1 Gm (1'000'000 Km), a bit more than the lifetime of the car
TRIP_DISTANCE_M_NORMALIZATION_FACTOR: int = 1000000 # 1000 Km, a bit more than a single gas tank could do
VEHICLE_TEMPERATURE_KELVIN_NORMALIZATION_FACTOR: int = 273 # 0C in Kelvin
TRIP_ENGINE_RUNNING_TIME_S_NORMALIZATION_FACTOR: int = 100000 # 100K seconds, a bit more than a single gas tank could do
FUEL_EFFICIENCY_M_PEL_L_NORMALIZATION_FACTOR: int = 100000 # 1 L/100Km (100 Km/L), approximate fuel efficiency of VW XL1
ENGINE_OPERATING_TEMPERATURE_CELSIUS: int = 90
ENGINE_OPERATING_TEMPERATURE_KELVIN: int = 273 + ENGINE_OPERATING_TEMPERATURE_CELSIUS
TEMPERATURE_DIFFERENCE_BETWEEN_VEHICLE_AND_ENGINE_OPERATING_NORMALIZATION_FACTOR: int = ENGINE_OPERATING_TEMPERATURE_CELSIUS + 50 # -50C, surely it'll never be colder than that
TRIP_AVERAGE_SPEED_M_PER_S_NORMALIZATION_FACTOR: int = 40 # equivalent to 144 Km/h
TIME_OF_DAY_S_SINCE_MIDNIGHT_NORMALIZATION_FACTOR: int = 86400 # seconds in a day

t0: datetime = datetime(2024, 7, 26)

class VehicleTrip:
    def __init__(self):
        self.__date_and_time: datetime | None = None
        self.__odometer_m: int | None = None
        self.__trip_distance_m: int | None = None
        self.__vehicle_temperature_kelvin: float | None = None
        self.__trip_engine_running_time_s: int | None = None
        self.__fuel_efficiency_m_per_l: int | None = None

    @property
    def date_and_time(self) -> datetime:
        assert self.__date_and_time is not None
        return self.__date_and_time

    @date_and_time.setter
    def date_and_time(self, date_and_time: datetime):
        assert isinstance(date_and_time, datetime)
        self.__date_and_time = date_and_time

    @property
    def seconds_since_t0(self) -> float:
        assert isinstance(t0, datetime)
        assert self.__date_and_time is not None
        return (self.__date_and_time - t0).total_seconds()

    @property
    def normalized_time_since_t0(self) -> float:
        return self.seconds_since_t0 / DATE_AND_TIME_S_NORMALIZATION_FACTOR

    @property
    def odometer_m(self) -> int:
        assert self.__odometer_m is not None
        return self.__odometer_m

    @odometer_m.setter
    def odometer_m(self, odometer_m: int):
        assert isinstance(odometer_m, int)
        self.__odometer_m = odometer_m

    @property
    def odometer_km(self) -> float:
        assert self.__odometer_m is not None
        return self.__odometer_m / 1000

    @odometer_km.setter
    def odometer_km(self, odometer_km: float | int):
        assert isinstance(odometer_km, (float, int))
        self.__odometer_m = int(odometer_km * 1000)

    @property
    def normalized_odometer(self) -> float:
        return self.odometer_m / ODOMETER_M_NORMALIZATION_FACTOR

    @property
    def trip_distance_m(self) -> int:
        assert self.__trip_distance_m is not None
        return self.__trip_distance_m

    @trip_distance_m.setter
    def trip_distance_m(self, trip_distance_m: int):
        assert isinstance(trip_distance_m, int)
        self.__trip_distance_m = trip_distance_m

    @property
    def trip_distance_km(self) -> float:
        assert self.__trip_distance_m is not None
        return self.__trip_distance_m / 1000

    @trip_distance_km.setter
    def trip_distance_km(self, trip_distance_km: float | int):
        assert isinstance(trip_distance_km, (float, int))
        self.__trip_distance_m = int(trip_distance_km * 1000)

    @property
    def normalized_trip_distance(self) -> float:
        return self.trip_distance_m / TRIP_DISTANCE_M_NORMALIZATION_FACTOR

    @property
    def vehicle_temperature_kelvin(self) -> float:
        assert self.__vehicle_temperature_kelvin is not None
        return self.__vehicle_temperature_kelvin

    @vehicle_temperature_kelvin.setter
    def vehicle_temperature_kelvin(self, vehicle_temperature_kelvin: float | int):
        assert isinstance(vehicle_temperature_kelvin, (float, int))
        self.__vehicle_temperature_kelvin = float(vehicle_temperature_kelvin)

    @property
    def vehicle_temperature_celsius(self) -> float:
        assert self.__vehicle_temperature_kelvin is not None
        return self.__vehicle_temperature_kelvin - 273.15

    @vehicle_temperature_celsius.setter
    def vehicle_temperature_celsius(self, vehicle_temperature_celsius: float | int):
        assert isinstance(vehicle_temperature_celsius, (float, int))
        self.__vehicle_temperature_kelvin = float(vehicle_temperature_celsius) + 273.15

    @property
    def normalized_vehicle_temperature(self) -> float:
        return self.vehicle_temperature_kelvin / VEHICLE_TEMPERATURE_KELVIN_NORMALIZATION_FACTOR

    @property
    def trip_engine_running_time_s(self) -> int:
        assert self.__trip_engine_running_time_s is not None
        return self.__trip_engine_running_time_s

    @trip_engine_running_time_s.setter
    def trip_engine_running_time_s(self, trip_engine_running_time_s: int):
        assert isinstance(trip_engine_running_time_s, int)
        self.__trip_engine_running_time_s = trip_engine_running_time_s

    @property
    def trip_engine_running_time_m(self) -> float:
        assert self.__trip_engine_running_time_s is not None
        return self.__trip_engine_running_time_s / 60

    @trip_engine_running_time_m.setter
    def trip_engine_running_time_m(self, trip_engine_running_time_m: float | int):
        assert isinstance(trip_engine_running_time_m, (float, int))
        self.__trip_engine_running_time_s = int(trip_engine_running_time_m * 60)

    @property
    def normalized_trip_engine_running_time(self) -> float:
        return self.trip_engine_running_time_s / TRIP_ENGINE_RUNNING_TIME_S_NORMALIZATION_FACTOR

    @property
    def fuel_efficiency_m_per_l(self) -> int:
        assert self.__fuel_efficiency_m_per_l is not None
        return self.__fuel_efficiency_m_per_l

    @fuel_efficiency_m_per_l.setter
    def fuel_efficiency_m_per_l(self, fuel_efficiency_m_per_l: int):
        assert isinstance(fuel_efficiency_m_per_l, int)
        self.__fuel_efficiency_m_per_l = fuel_efficiency_m_per_l

    @property
    def fuel_efficiency_l_per_hundred_km(self) -> float:
        assert self.__fuel_efficiency_m_per_l is not None
        return 100000 / self.__fuel_efficiency_m_per_l

    @fuel_efficiency_l_per_hundred_km.setter
    def fuel_efficiency_l_per_hundred_km(self, fuel_efficiency_l_per_hundred_km: float):
        assert isinstance(fuel_efficiency_l_per_hundred_km, float)
        self.__fuel_efficiency_m_per_l = int(100000 / fuel_efficiency_l_per_hundred_km)

    @property
    def normalized_fuel_efficiency(self) -> float:
        return self.fuel_efficiency_m_per_l / FUEL_EFFICIENCY_M_PEL_L_NORMALIZATION_FACTOR

    @property
    def temperature_difference_between_vehicle_and_engine_operating_kelvin(self) -> float:
        return ENGINE_OPERATING_TEMPERATURE_KELVIN - self.vehicle_temperature_kelvin

    @property
    def normalized_temperature_difference_between_vehicle_and_engine_operating(self) -> float:
        return self.temperature_difference_between_vehicle_and_engine_operating_kelvin / TEMPERATURE_DIFFERENCE_BETWEEN_VEHICLE_AND_ENGINE_OPERATING_NORMALIZATION_FACTOR

    @property
    def trip_average_speed_m_per_s(self) -> float:
        return self.trip_distance_m / self.trip_engine_running_time_s

    @property
    def trip_average_speed_s_per_km(self) -> int:
        return int(self.trip_engine_running_time_s / self.trip_distance_km)

    @property
    def normalized_trip_average_speed(self) -> float:
        return self.trip_average_speed_m_per_s / TRIP_AVERAGE_SPEED_M_PER_S_NORMALIZATION_FACTOR

    @property
    def time_of_day_s_from_midnight(self) -> int:
        return int((self.date_and_time - datetime.combine(self.date_and_time.date(), time.min)).total_seconds())

    @property
    def normalized_time_of_day(self) -> float:
        return self.time_of_day_s_from_midnight / TIME_OF_DAY_S_SINCE_MIDNIGHT_NORMALIZATION_FACTOR

    @property
    def time_of_year_s_from_new_year(self) -> int:
        return int((self.date_and_time - datetime(self.date_and_time.year, 1, 1)).total_seconds())

    @property
    def normalized_time_of_year(self) -> float:
        return self.time_of_year_s_from_new_year / TIME_OF_YEAR_S_SINCE_NEW_YEAR_NORMALIZATION_FACTOR
