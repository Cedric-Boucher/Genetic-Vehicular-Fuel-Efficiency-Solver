import os
from typing import Self
import csv
from vehicle_trip import VehicleTrip
from datetime import datetime
import pandas as pd

class HeaderMap:
    def __init__(self,
                 date_and_time_index: int,
                 odometer_km_index: int,
                 trip_distance_km_index: int,
                 vehicle_temperature_celsius_index: int,
                 trip_engine_running_time_m_index: int,
                 fuel_efficiency_l_per_hundred_km_index: int):
        self.date_and_time_index: int = date_and_time_index
        self.odometer_km_index: int = odometer_km_index
        self.trip_distance_km_index: int = trip_distance_km_index
        self.vehicle_temperature_celsius_index: int = vehicle_temperature_celsius_index
        self.trip_engine_running_time_m_index: int = trip_engine_running_time_m_index
        self.fuel_efficiency_l_per_hundred_km_index: int = fuel_efficiency_l_per_hundred_km_index

class DataImporter:
    def __init__(self, file_path: str):
        self.__file_path: str = str(file_path)
        assert os.path.exists(self.__file_path)
        assert os.path.isfile(self.__file_path)
        self.__file_date_modified: None | float = None
        self.__data: None | list[VehicleTrip] = None

    def __import_data(self) -> Self:
        assert os.path.exists(self.__file_path)
        assert os.path.isfile(self.__file_path)
        file_date_modified: float = os.stat(self.__file_path).st_mtime
        if self.__file_date_modified == file_date_modified:
            # no need to re-import data, as it has not changed
            return self
        self.__file_date_modified = file_date_modified
        headers: tuple[str, ...] | None = None
        header_map: None | HeaderMap = None
        data: None | list[VehicleTrip] = None
        with open(self.__file_path, "r") as file:
            reader = csv.reader(file)
            first_row: bool = True
            for row in reader:
                if first_row:
                    headers = tuple(row)
                    header_map = self.__verify_headers(headers)
                    data = list()
                    first_row = False
                else:
                    assert header_map is not None
                    assert data is not None # data should be a list, whether empty or not
                    try:
                        row_vehicle_trip: VehicleTrip = VehicleTrip()
                        row_vehicle_trip.date_and_time = datetime.strptime(row[header_map.date_and_time_index], "%Y-%m-%d %H:%M:%S")
                        row_vehicle_trip.odometer_km = float(row[header_map.odometer_km_index])
                        row_vehicle_trip.trip_distance_km = float(row[header_map.trip_distance_km_index])
                        row_vehicle_trip.vehicle_temperature_celsius = float(row[header_map.vehicle_temperature_celsius_index])
                        row_vehicle_trip.trip_engine_running_time_m = float(row[header_map.trip_engine_running_time_m_index])
                        row_vehicle_trip.fuel_efficiency_l_per_hundred_km = float(row[header_map.fuel_efficiency_l_per_hundred_km_index])
                        data.append(row_vehicle_trip)
                    except ValueError:
                        # skip rows that have missing information
                        pass

        assert headers is not None
        assert data is not None

        self.__data = data

        return self

    @staticmethod
    def __verify_headers(headers: tuple[str, ...]) -> HeaderMap:
        header_map: HeaderMap = HeaderMap(
            date_and_time_index = headers.index("Date and Time (YYYY/MM/DD HH:MM:SS)"),
            odometer_km_index = headers.index("Odometer (Km)"),
            trip_distance_km_index = headers.index("Trip Distance (Km)"),
            vehicle_temperature_celsius_index = headers.index("Reported Vehicle Temperature At Departure (C)"),
            trip_engine_running_time_m_index = headers.index("Reported Engine Running Time (Minutes)"),
            fuel_efficiency_l_per_hundred_km_index = headers.index("Reported Fuel Efficiency of Trip (L/100Km)")
        )
        return header_map

    @property
    def vehicle_trips(self) -> list[VehicleTrip]:
        data = self.__import_data().__data
        assert data is not None
        return data

    @property
    def vehicle_trip_dataframe(self) -> pd.DataFrame:
        data = self.__import_data().__data
        assert data is not None
        df: pd.DataFrame = pd.DataFrame([
            {
                "seconds_since_purchase": int(trip.seconds_since_t0),
                "odometer_m": trip.odometer_m,
                "trip_distance_m": trip.trip_distance_m,
                "vehicle_temperature_k": int(trip.vehicle_temperature_kelvin),
                "temperature_difference_vehicle_operating_k": int(trip.temperature_difference_between_vehicle_and_engine_operating_kelvin),
                "trip_engine_running_time_s": trip.trip_engine_running_time_s,
                "trip_average_speed_s_per_km": trip.trip_average_speed_s_per_km,
                "time_of_day_seconds_from_midnight": trip.time_of_day_s_from_midnight,
                "time_of_year_seconds_from_new_year": trip.time_of_year_s_from_new_year,
                "fuel_efficiency_m_per_l": trip.fuel_efficiency_m_per_l
            }
            for trip in data
        ])

        return df


if __name__ == "__main__":
    vehicle_trips: list[VehicleTrip] = DataImporter("K:/Downloads/Toyota Corolla Automatic 2009.csv").vehicle_trips
    print([trip.trip_distance_m for trip in vehicle_trips])
