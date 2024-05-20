import requests
import matplotlib.pyplot as plt
from IPython.display import Image
import random
import numpy as np
from tqdm import tqdm


def train_test_split(data, test=0.1, seed=42):
    user_ids, movie_ids, user_ratings = data.T

    # getting unique user IDs and movie IDs
    unique_user_ids = np.unique(user_ids)
    unique_movie_ids = np.unique(movie_ids)

    # Making Data random
    rng = np.random.default_rng(43)
    rng.shuffle(data)

    test_num = int(test * len(data))

    test = data[: test_num + 1, :]
    train = data[test_num + 1 :, :]

    return train, test, unique_user_ids, unique_movie_ids


def create_UV(rating_arr, unique_user_ids, unique_movie_ids):
    # sorting according to user and movies
    user_sort = rating_arr[rating_arr[:, 0].argsort()]
    movies_sort = rating_arr[rating_arr[:, 1].argsort()]

    # separating user and movie IDs and ratings
    user_ids, user_movie_ids, user_ratings = user_sort.T
    movie_user_ids, movie_movie_ids, movie_ratings = movies_sort.T

    # getting unique user IDs and movie IDs
    # unique_user_ids = np.unique(user_ids)
    # unique_movie_ids = np.unique(movie_movie_ids)

    # mapping Ids to rating map
    user_to_idx = {int(user_id): idx for idx, user_id in enumerate(unique_user_ids)}
    movie_to_idx = {int(movie_id): idx for idx, movie_id in enumerate(unique_movie_ids)}

    # mapping
    user_to_rating = [[] for _ in unique_user_ids]
    movie_to_rating = [[] for _ in unique_movie_ids]

    for user_id, movie_id, rating in tqdm(zip(user_ids, user_movie_ids, user_ratings)):
        user_idx = user_to_idx[int(user_id)]
        movie_idx = movie_to_idx[int(movie_id)]
        user_to_rating[user_idx].append((movie_idx, rating))
        movie_to_rating[movie_idx].append((user_idx, rating))

    return user_to_idx, movie_to_idx, user_to_rating, movie_to_rating


def get_movie_ids_by_category(df, category):
    filtered_df = df[df["genres"].str.contains(category)]
    if filtered_df.empty:
        return "Aucun film trouvé dans cette catégorie"
    return filtered_df["movieId"].tolist()


def get_embedding(X, dico, movies, category):
    emb = []
    movie_ids = get_movie_ids_by_category(movies, category)
    for id in movie_ids:
        value = dico.get(id)
        if value is not None:
            emb.append(value)
    trie = []
    for i in emb[:100]:
        trie.append(X[i])
    return np.array(trie)


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
    plt.figure(figsize=(6, 4))
    plt.scatter(movie_degrees.index, movie_degrees.values, alpha=0.5)
    plt.scatter(user_degrees.index, user_degrees.values, alpha=0.5)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Degree (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.grid(True)
    plt.savefig("law_distribution.pdf", format="pdf")
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


def get_images_urls(link, size=10):
    link_list = list(link["tmdbId"].unique())
    choice = random.sample(link_list, size)
    imageUrls = [fetch_poster(k) for k in choice]
    return imageUrls
