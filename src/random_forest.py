from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import shap
import pandas as pd

import config
from data_importer import DataImporter

features: list[str] = [
    "seconds_since_purchase",
    "odometer_m",
    "trip_distance_m",
    "vehicle_temperature_k",
    "temperature_difference_vehicle_operating_k",
    "trip_engine_running_time_s",
    "trip_average_speed_s_per_km",
    "time_of_day_seconds_from_midnight",
    "time_of_year_seconds_from_new_year"
]
target: str = "fuel_efficiency_m_per_l"

df: pd.DataFrame = DataImporter(config.DATA_FILE_PATH).vehicle_trip_dataframe

x = df[features]
y = df[target]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(x_train, y_train)

print(f"Score (R^2): {model.score(x_test, y_test)}")

explainer = shap.Explainer(model, x_train)
shap_values = explainer(x_test)

shap.summary_plot(shap_values, x_test)

print("Prediction: {} L/100Km".format(
    100000 /
    model.predict(pd.DataFrame([{
        "seconds_since_purchase": 0,
        "odometer_m": 134000,
        "trip_distance_m": 22100,
        "vehicle_temperature_k": 310,
        "temperature_difference_vehicle_operating_k": 90 + 273 - 310,
        "trip_engine_running_time_s": 1800,
        "trip_average_speed_s_per_km": 80,
        "time_of_day_seconds_from_midnight": 3600 * 8,
        "time_of_year_seconds_from_new_year": 3600 * 24 * 182
    }])))
)
