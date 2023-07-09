from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    movie_id = models.CharField(primary_key=True, max_length=200)
    movie_name = models.CharField(max_length=200)
    click_through_rate = models.FloatField(default=0)

    num_of_times_clicked = models.IntegerField(default=0)
    num_of_impressions = models.IntegerField(default=0)

    rating = models.FloatField()
    image_url = models.ImageField()
    description = models.CharField(max_length=1000)
    movie_genre = [] #list of genres


class Search(models.Model):
    keyword = models.CharField(max_length=200)
    results = []
    liked_movies = [] # list of Movie objects
    num_movies_liked = models.IntegerField(default=0)
    time = models.TimeField(auto_now=True) #time of search


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    search_history = [] # list of searches
    wishlist = [] # list of all movies ever liked
