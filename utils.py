from google.colab.patches import cv2_imshow
import cv2
import requests


def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
     data=requests.get(url)
     data=data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
     return full_path

def display_image_movie(movie_id):
  tmdbId=link[link['movieId']==movie_id]['tmdbId'].values[0]
  url = fetch_poster(tmdbId)
  data = requests.get(url).content
  f = open('img.jpg','wb')
  f.write(data)
  f.close()
  img = cv2.imread('img.jpg')
  img = cv2.resize(img, (400, 400))
  cv2_imshow(img)

def map_movie_id_title(movie_id):
    return movies[movies['movieId']==movie_id]['title'].values[0]