import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from matplotlib.transforms import Transform
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
                                            f"cent_{activity}_playlist.csv"),
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
    df_merged_copy = pd.read_csv(path_to_entire_dataset, index_col=0)

    df_merged_copy['Count'] = 1

    df_merged_copy = df_merged_copy.groupby(['genre', 'artist_name', 'track_name', 'track_id', 'popularity',
       'acousticness', 'danceability', 'duration_ms', 'energy',
       'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
       'speechiness', 'tempo', 'time_signature', 'valence'],sort=False)['Count'].agg('sum').reset_index()

    df_merged_copy = df_merged_copy.drop_duplicates()


    dict_centroids = centroids(activity)
    centroids_restored = pd.DataFrame(dict_centroids).T.drop(
        columns=["global_df_index", "centroid_index"])
    print("-------------------------")
    print(centroids_restored.columns)
    print("--------------------------")
    track_selected = centroids_restored.iloc[int(centroid_selected)]
    print("-------------------------")
    print(track_selected["track_name"])
    print("--------------------------")
    print(type(track_selected["track_name"]))


    df_centroid = df_merged_copy[df_merged_copy["track_name"] == track_selected["track_name"]]

    print("-------------------------")
    print(df_centroid.columns)
    print("--------------------------")
    print("-------------------------")
    print(df_centroid.shape)
    print("--------------------------")

    preproc = joblib.load(os.path.join(path_to_models_folder,"preproc.joblib"))

    X = preproc.transform(df_centroid)

    modelKNN = joblib.load(os.path.join(path_to_models_folder,"KNNmodel.joblib"))

    prediction = modelKNN.kneighbors(X, n_neighbors = 10)
    nb_neighbors = 10
    centroids_list = []
    list_tracks = []
    centroid_res_df2 = pd.DataFrame()

    for n in range (0,nb_neighbors):
        centroids_list.append(prediction[1][0][n])

        centroid_res_df2=pd.concat([centroid_res_df2,df_merged_copy.loc[n]], ignore_index=True, axis=1)

    centroid_res_df2 = centroid_res_df2
    print(centroid_res_df2)

    dict_playlist = centroid_res_df2.to_dict()
    return dict_playlist
