from datetime import datetime

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
