import streamlit as st
import pandas as pd
import numpy as np


#url = 'url'

#if url == 'url':

st.title('Playlist prediction')

act = ['cooking','running','work','relax','shower']

with st.form(key='my_form'):
    option = st.selectbox("Pick an activity",act)
    submit_button = st.form_submit_button(label="Let's go !")

st.write('My activity:', option)
