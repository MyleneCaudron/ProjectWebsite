import streamlit as st
import pandas as pd
import numpy as np
import requests

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
url = 'http://localhost:8501/centroids'

params = dict(activity = activity)

response = requests.get(url, params=params)

centroids = response.json()

playlist = []
nb = centroids.shape[1]

for i  in range(0,nb):
    playlist.append(centroids['artist_name','track_name'].iloc[[i]])

music_choice = st.radio(
     "Choose your favorite music",
     (f'{playlist[0]}', f'{playlist[1]}', f'{playlist[2]}',f'{playlist[3]}'))

st.write('You selected :',music_choice)

# Second predict To display the final playlist

url = 'http://localhost:8501/playlist'

params = dict(key = music_choice)

response = requests.get(url,params)

playlist = response.json()
