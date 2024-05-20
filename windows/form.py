import streamlit as st
import pandas as pd
import numpy as np
from utils import *


def form(link, movies_df, movies_list, dico):
    default = [(4887, 5.0)]

    user_name = st.text_input("User name :")

    num_subjects = st.number_input("Number of rating :", min_value=1, step=1)

    df = pd.DataFrame(columns=["id", "Movies", "Rate"])

    for i in range(num_subjects):
        selectvalue = st.selectbox(f"Select movie   {i+1}", movies_list["title"])
        movie_id = find_id_per_title(movies_df, selectvalue)
        tmdbId = link[link["movieId"] == movie_id]["tmdbId"].values[0]
        st.image(
            fetch_poster(tmdbId),
            width=200,
            caption=f"{selectvalue} - {map_movie_id_genre(movie_id, movies_df)}",
        )

        subject_grade = st.number_input(
            f"Rate of the movie {i+1} :", min_value=0.0, max_value=5.0, step=0.5
        )
        df.loc[i] = [movie_id, selectvalue, subject_grade]

    st.write("This is your rating :")
    st.write(df)
    if user_name == "":
        user_name = "User"
    if st.button("Save rating"):
        default = save_data(df, dico)

        st.success(f" Dear {user_name}, your movie's ratings, are save with succes 😁!")
    return default, user_name


def save_data(dataframe, dico):
    if (dataframe.shape[0]) > 0:
        liste_lignes = [
            tuple([dico[row[0]], row[2]]) for row in dataframe.to_records(index=False)
        ]
        print(liste_lignes)
        np.save("model/preferences.npy", liste_lignes)
    else:
        liste_lignes = [(4887, 5.0)]
        np.save("model/preferences.npy", liste_lignes)

    return liste_lignes
