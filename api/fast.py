import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from api.params import path_to_entire_dataset, path_to_models_folder

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
    return {"greeting": "Hello !"}

@app.get("/centroids")
def centroids(activity):
    """
    It returns the activity centroids
    """
    df_centroids = pd.read_csv(os.path.join("api", "centroids",
                                            f"{activity}_playlist.csv"),
                  on_bad_lines='skip', index_col=[0]).T

    print(f"""---------------------------------
          {df_centroids.columns}""")

    df_centroids["centroid_index"] = [i for i in range(len(df_centroids))]
    df_centroids["global_df_index"] = df_centroids.index
    df_centroids.reset_index(drop=True, inplace=True)

    dict_centroids = df_centroids.T.to_dict()

    return dict_centroids


@app.get("/playlist")
def playlistselected(activity, centroid_selected):
    """
    From the centroid selected it returns the playlist derived from the
    KNN of the big dataset
    """

    df_restored = pd.DataFrame(centroids(activity)).T.drop(columns=
                                                           ["global_df_index",
                                                            "centroid_index"])
    df_centroid_selected=df_restored[df_restored.index == int(centroid_selected)]

    X = df_centroid_selected.copy()

    model = joblib.load("KNNmodel.joblib")

    prediction = model.kneighbors(n_neigbours = 10)
    return {"playlist": prediction}
