import streamlit as st
import pandas as pd
import numpy as np
import requests
#from api.params import url_base

url_base = "http://127.0.0.1:8000"

'''
# Playlist project front

'''

st.title('Playlist prediction')

act = ['cooking','running','work','relax','shower']

with st.form(key='my_form'):
    activity = st.selectbox("Pick an activity",act)
    submit_button = st.form_submit_button(label="Let's go !")

st.write('My activity:', activity)


# First predict To display the list with 4 centroids
url = f'{url_base}/centroids'

params_activity = dict(activity = activity)

response = requests.get(url, params=params_activity)

dict_centroids = response.json()

df_restored = pd.DataFrame(dict_centroids).T.drop(
    columns=["global_df_index", "centroid_index"])

df_centroids = df_restored[['artist_name','track_name']]
playlist = df_centroids.copy()

#print(f"...................................{playlist}")

music_choice = st.radio(
     "Choose your favorite music",
     (f'0_{playlist.iloc[0]}', f'1_{playlist.iloc[1]}', f'2_{playlist.iloc[2]}',f'3_{playlist.iloc[3]}'))


st.write('You selected :',music_choice)

# Second predict To display the final playlist

url = f'{url_base}/playlist'

params_playlist = params_activity
print("====================")
print(music_choice.split("_"))
list_split = music_choice.split("_")
print(list_split[0])
print("==================")

params_playlist=params_activity
params_playlist["centroid"] = list_split[0]

response = requests.get(url,params_playlist)

print(response.json())

df_restored = pd.DataFrame(response).T

print(df_restored)
st.dataframe(df_restored)
playlist = response.json()
