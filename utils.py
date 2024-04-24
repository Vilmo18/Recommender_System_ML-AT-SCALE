from google.colab.patches import cv2_imshow
import cv2
import requests
import matplotlib.pyplot as plt

def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
     data=requests.get(url)
     data=data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
     return full_path

def display_image_title_movie(movie_id,link,movies):
  tmdbId=link[link['movieId']==movie_id]['tmdbId'].values[0]
  url = fetch_poster(tmdbId)
  data = requests.get(url).content
  f = open('img.jpg','wb')
  f.write(data)
  f.close()
  img = cv2.imread('img.jpg')
  img = cv2.resize(img, (350, 350))
  cv2_imshow(img)
  print(map_movie_id_title(movie_id,movies))

def map_movie_id_title(movie_id,movies):
    return movies[movies['movieId']==movie_id]['title'].values[0]


def plot_rating(data):
  user_rating_counts = data.groupby('userId')['rating'].count()
  movie_rating_counts = data.groupby('movieId')['rating'].count()

  user_degrees = user_rating_counts.value_counts().sort_index()
  movie_degrees = movie_rating_counts.value_counts().sort_index()

  plt.figure(figsize=(10, 5))
  plt.scatter(user_degrees.index, user_degrees.values, color='blue', alpha=0.5)
  plt.xscale('log')
  plt.yscale('log')
  plt.xlabel('Degree (log scale)')
  plt.ylabel('Frequency (log scale)')
  plt.grid(True)
  plt.show()

  plt.figure(figsize=(10, 5))
  plt.scatter(movie_degrees.index, movie_degrees.values, color='green', alpha=0.5)
  plt.xscale('log')
  plt.yscale('log')
  plt.xlabel('Degree (log scale)')
  plt.ylabel('Frequency (log scale)')
  plt.grid(True)
  plt.show()
