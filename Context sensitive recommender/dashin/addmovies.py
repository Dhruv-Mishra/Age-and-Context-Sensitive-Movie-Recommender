from models import models
import pandas as pd
df = pd.read_csv('/Users/cloud9xpress/Desktop/codeCloud/dashin_front-end/48_MidReview/Datasets/unclean_dataset.csv')
df.shape
df = df.dropna()
df.shape

#  dataset
movies = []
for i in df.index:
    movie = models.Movie(name=movie[i].name)
    movie.movie_name = df['Movie Title'][i]
    movie.description = df['Plot'][i]
    movie.image_url = df['Poster_URL'][i]
    movie.rating = df['Imdb rating'][i]
    movie.save()
    movies.append(movie)