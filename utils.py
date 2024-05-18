import requests
import matplotlib.pyplot as plt
from IPython.display import Image
import random

def find_id_per_title(dataframe, titre_recherche):
    row = dataframe[dataframe["title"] == titre_recherche]
    if not row.empty:
        return row.iloc[0]["movieId"]
    else:
        return None

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(
        movie_id
    )
    data = requests.get(url).json()
    if not isinstance(data.get("poster_path"), str):
        full_path = "images/unknown.jpg"
    else:
        poster_path = data["poster_path"]
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



def map_movie_id_title(movie_id, movies):
    return movies[movies["movieId"] == movie_id]["title"].values[0]


def map_movie_id_genre(movie_id, movies):
    return movies[movies["movieId"] == movie_id]["genres"].values[0]


def plot_rating(data):
    user_rating_counts = data.groupby("userId")["rating"].count()
    movie_rating_counts = data.groupby("movieId")["rating"].count()
    user_degrees = user_rating_counts.value_counts().sort_index()
    movie_degrees = movie_rating_counts.value_counts().sort_index()
    plt.figure(figsize=(10, 5))

    plt.scatter(user_degrees.index, user_degrees.values, color="blue", alpha=0.5)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Degree (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.scatter(movie_degrees.index, movie_degrees.values, color="green", alpha=0.5)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Degree (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.grid(True)
    plt.show()


def find_key_by_values(dictionnaire, valeur_recherchee):
    for cle, valeur in dictionnaire.items():
        if valeur == valeur_recherchee:
            return cle
    raise ValueError("La valeur spécifiée n'existe pas dans le dictionnaire")


def display_image_title_movie(movie_id, link, movies):
    tmdbId = link[link["movieId"] == movie_id]["tmdbId"].values[0]
    url = fetch_poster(tmdbId)
    reponse = requests.get(url)

    image_url = f"image_{movie_id}.jpg"

    if reponse.status_code == 200:
        with open(image_url, "wb") as local_file:
            local_file.write(reponse.content)
        print("succes")
        local_file.close()
    else:
        print("failed!")

    display(Image(url=image_url, width=300, height=300))  # noqa: F821
    print(map_movie_id_title(movie_id, movies))


def get_images_urls(link, size=6):
    link_list = list(link["tmdbId"].unique())
    choice = random.sample(link_list, size)
    imageUrls = [fetch_poster(k) for k in choice]
    return imageUrls
