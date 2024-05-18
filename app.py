import streamlit as st
import streamlit.components.v1 as components
from windows.form import *
from windows.menu import *
from utils import *
from cache import *
from recommendation import *


st.set_page_config(
    page_title="MoviesLens Recommender System ",
    page_icon=":rocket:",
    initial_sidebar_state="expanded",
    layout="wide",
)
st.header("MoviesLens Recommender System")


## Load Ressource
link, movies_df, movies_list, dico, occurrences = load_ressource()

imageCarouselComponent = components.declare_component(
    "image-carousel-component", path="frontend/public"
)


## Display carrousel

imageUrls = get_images_urls(link=link, size=7)
imageCarouselComponent(imageUrls=imageUrls, height=200)


menu = streamlit_menu()

if menu == "Preferences":
    st.title("User Preferences")
    st.session_state["user_predict"], st.session_state["user"] = form(
        link, movies_df, movies_list, dico
    )

if menu == "Search":
    st.title("Looking for movies")
    selectvalue = st.selectbox("Select movie from dropdown", movies_list["title"])
    movie_id = find_id_per_title(movies_df, selectvalue)
    tmdbId = link[link["movieId"] == movie_id]["tmdbId"].values[0]
    with st.spinner("Loading..."):
        st.image(
            fetch_poster(tmdbId),
            width=200,
            caption=f"{selectvalue} - {map_movie_id_genre(movie_id, movies_list)}",
        )

if menu == "Recommendation":
    option = st.radio("Choose your way ", ("Popular", "Personalisation"))
    if st.button(f"{st.session_state['user']} could like something like this"):
        with st.spinner("Loading..."):
            users_predict = st.session_state["user_predict"]
            print(users_predict)
            if len(users_predict) == 0:
                users_predict = [(4887, 5.0)]

            movies_vector, item_biases = load_latent()
            user_new, user_bias_new = generate_user_vector(
                users_predict, movies_vector, item_biases
            )

            if option == "Popular":
                value = 1
            else:
                value = 0.05
            index = prediction(
                user_new,
                user_bias_new,
                movies_vector,
                item_biases,
                dico,
                occurrences,
                fact=value,
            )

            recom_images = []
            for i in range(len(index[:20])):
                tmdbId = link[link["movieId"] == index[i]]["tmdbId"].values[0]
                recom_images.append((index[i], fetch_poster(tmdbId)))
            n_cols = 4
            n_rows = 1 + len(recom_images) // int(n_cols)
            rows = [st.container() for _ in range(n_rows)]
            cols_per_row = [r.columns(n_cols) for r in rows]
            cols = [column for row in cols_per_row for column in row]

            for image_index, cat_image in enumerate(recom_images):
                cols[image_index].image(
                    cat_image[1],
                    width=250,
                    caption=f"{map_movie_id_title(cat_image[0], movies_list)} {map_movie_id_genre(cat_image[0], movies_list)}",
                )
