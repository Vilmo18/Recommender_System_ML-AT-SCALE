import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import random
import pickle
import numpy as np
import requests
from tqdm import tqdm
from form import *
import pandas as pd
from utils import *


def generate_user_vector(
    users_predict,
    movies_vector,
    item_biases,
    lamb=5,
    tau=0.4,
    gamma=2e-1,
    iteration=1500,
    k=10,
):
    user_new = np.random.normal(0, 1 / np.sqrt(k), (k))
    user_bias_new = 0
    for _ in range(iteration):
        biais = 0
        item_counter = 0
        for n, r in users_predict:
            biais += r - np.dot(user_new, movies_vector.T[n]) - item_biases[n]
            item_counter += 1

        biais *= lamb
        biais = biais / (lamb * item_counter + gamma)
        user_bias_new = biais

        left_val = 0
        right_val = 0
        for n, r in users_predict:
            left_val += movies_vector.T[n] * movies_vector.T[n].reshape(-1, 1)
            right_val += movies_vector.T[n] * (r - user_bias_new - item_biases[n])

        left_val *= lamb
        user_new = np.linalg.solve(left_val + tau * np.eye(k), lamb * right_val)

    return user_new, user_bias_new


@st.cache_data
def load_latent():
    movies_vector = np.load("model2/movies.npy")
    item_biases = np.load("model2/m_bias.npy")
    return movies_vector, item_biases


@st.cache_data
def load_data():
    data = pd.read_csv("occurences.csv")
    return data

@st.cache_data
def load_info():
    link = pd.read_csv("links.csv")
    movies_df = pd.read_csv("movies.csv")
    movies = pickle.load(open("movies.pkl", "rb"))
    movies_list = movies
    return link, movies_df, movies, movies_list

@st.cache_data
def load_ressource():
    link = pd.read_csv("links.csv")
    movies_df = pd.read_csv("movies.csv")
    movies_list = pickle.load(open("movies.pkl", "rb"))
    dico = np.load("model2/movies_mapping.npy", allow_pickle=True).item()
    return link, movies_df, movies_list, dico

def prediction(user_new, user_bias_new, movies_vector, item_biases, fact=1):
    def movie_ids_less_than_k_occurrences(rate=50):
        #dataframe = load_data()
        #occurrences = (
        #    dataframe.groupby("movieId").size().reset_index(name="occurrences")
        #)
        occurrences=load_data()
        less_than_30_occurrences = occurrences[occurrences["occurrences"] < rate][
            "movieId"
        ].tolist()
        return less_than_30_occurrences

    n = movies_vector.shape[1]
    predict = []
    for i in range(n):
        predict.append(
            np.dot(user_new, movies_vector.T[i]) + fact * item_biases[i] + user_bias_new
        )
    recommender = np.argsort(predict)[::-1]
    recommender = recommender[:700]
    rec = []
    print(2)
    dico = np.load("model2/movies_mapping.npy", allow_pickle=True).item()
    less_than_k_occurrences_ids = movie_ids_less_than_k_occurrences(rate=130)
    print(4)
    for i in recommender:
        key = find_key_by_values(dico, i)
        if key not in less_than_k_occurrences_ids:
            rec.append(key)
    return rec


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(
        movie_id
    )
    data = requests.get(url)
    data = data.json()

    if not isinstance(data.get("poster_path"), str):
        full_path = "unknown.jpg"
    else:
        poster_path = data["poster_path"]
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


st.set_page_config(
    page_title="MoviesLens Recommender System ",
    page_icon=":rocket:",
    initial_sidebar_state="expanded",
    layout="wide",
)
st.header("MoviesLens Recommender System")
link, movies_df, movies, movies_list = load_info()

link1, movies_df1, movies_list1, dico1 = load_ressource()


imageCarouselComponent = components.declare_component(
    "image-carousel-component", path="frontend/public"
)
link_list = list(link["tmdbId"].unique())
choice = random.sample(link_list, 14)
imageUrls = [fetch_poster(k) for k in choice]

imageCarouselComponent(imageUrls=imageUrls, height=200)


def streamlit_menu(example=1):
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",  # required
            options=["Preferences", "Search", "Recommendation"],  # required
            icons=["house", "search", "list"],  # optional
            # menu_icon="cast",  # optional
            default_index=0,  # optional
        )
    return selected


selected = streamlit_menu()

if selected == "Preferences":
    with st.spinner("Loading..."):
        st.session_state["user_predict"], st.session_state["user"] = form(link1, movies_df1, movies_list1, dico1)
if selected == "Search":
    st.title("Looking for movies")
    selectvalue = st.selectbox("Select movie from dropdown", movies_list["title"])
    movie_id = find_id_per_title(movies_df, selectvalue)
    tmdbId = link[link["movieId"] == movie_id]["tmdbId"].values[0]
    with st.spinner("Loading..."):
        st.image(
            fetch_poster(tmdbId),
            width=200,
            caption=f"{selectvalue} - {map_movie_id_genre(movie_id, movies)}",
        )




if selected == "Recommendation":
    option = st.radio("Choose your way ", ("Popular", "Personalisation"))
    if st.button(f"{st.session_state['user']} could like something like this"):
        with st.spinner("Loading..."):
            users_predict = st.session_state["user_predict"]
            print(users_predict)
            if len(users_predict) == 0:
                users_predict = [(4887, 5.0)]

            index_mapping_movie = np.load(
                "model2/movies_mapping.npy", allow_pickle=True
            ).item()

            movies_vector, item_biases = load_latent()
            user_new, user_bias_new = generate_user_vector(
                users_predict, movies_vector, item_biases
            )

            if option == "Popular":
                value = 1
            else:
                value = 0.05
            index = prediction(
                user_new, user_bias_new, movies_vector, item_biases, fact=value
            )

            cat_images = []
            for i in range(len(index[:20])):
                tmdbId = link[link["movieId"] == index[i]]["tmdbId"].values[0]
                ENDPOINT = fetch_poster(tmdbId)
                cat_images.append((index[i], fetch_poster(tmdbId)))

            n_cols = 4
            n_rows = 1 + len(cat_images) // int(n_cols)
            rows = [st.container() for _ in range(n_rows)]
            cols_per_row = [r.columns(n_cols) for r in rows]
            cols = [column for row in cols_per_row for column in row]

            for image_index, cat_image in enumerate(cat_images):
                cols[image_index].image(
                    cat_image[1],
                    width=250,
                    caption=f"{map_movie_id_title(cat_image[0], movies)} {map_movie_id_genre(cat_image[0], movies)}",
                )
