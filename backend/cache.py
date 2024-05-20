import streamlit as st
import pickle
import numpy as np
import pandas as pd


@st.cache_data
def load_latent():
    movies_vector = np.load("model/movies.npy")
    item_biases = np.load("model/m_bias.npy")
    return movies_vector, item_biases


@st.cache_data
def load_ressource():
    link = pd.read_csv("data/links.csv")
    movies_df = pd.read_csv("data/movies.csv")
    movies_list = pickle.load(open("model/movies.pkl", "rb"))
    dico = np.load("model/movies_mapping.npy", allow_pickle=True).item()
    occurrences = pd.read_csv("data/occurences.csv")
    return link, movies_df, movies_list, dico, occurrences
