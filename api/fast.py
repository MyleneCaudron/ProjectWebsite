from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from TaxiFareModel.utils import pickup_datetime_conversion
from predict import get_model
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello spotifier !"}

@app.get("/centroids")
def centroids(activity):
    """
    It returns the activity centroids
    """


    return {"fare": "result_model"}

def centroids(activity):

    key = f"{pickup_datetime}.0{passenger_count}.0000001"

    pickup_datetime = pickup_datetime_conversion(pickup_datetime)
    pickup_longitude = float(pickup_longitude)
    pickup_latitude = float(pickup_latitude)
    dropoff_longitude = float(dropoff_longitude)
    dropoff_latitude = float(dropoff_latitude)
    passenger_count = int(passenger_count)

    dict_values = { "key": [key],
                    "pickup_datetime": [pickup_datetime],
                    "pickup_longitude": [pickup_longitude],
                    "pickup_latitude": [pickup_latitude],
                    "dropoff_longitude": [dropoff_longitude],
                    "dropoff_latitude": [dropoff_latitude],
                    "passenger_count": [passenger_count]}
    X_test = pd.DataFrame(dict_values)

    model = joblib.load("model.joblib")

    prediction = model.predict(X_test)
    return {"fare": prediction[0]}
