from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, StreamingHttpResponse
from . import models
from .search import *
from .recommender import *
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd


def indexView(request):
    template = 'index.html'
    return render(request,template)

def loginView(request):
    if request.user.is_authenticated:
        template = 'home.html'
    else:
        template = "login.html"
        
    return render(request,template)

def signupView(request):
    if request.user.is_authenticated:
        template = 'home.html'
    else:
        template = "signup.html"

    return render(request,template)

def homeView(request):
    if request.user.is_authenticated:
        template = 'home.html'
    else:
        template = 'login.html'
    return render(request,template)


def logoutView(request):
    template = 'login.html'
    if request.user.is_authenticated:
        logout(request)

    return render(request,template)
    

# def resultsView(request):
#     template = 'results.html'
#     return render(request, template)

def addUser(request):
    form = request.POST
    name = form['registerName']
    username = form['registerUsername']
    email = form['registerEmail']
    password = form['registerPassword']
    new_user = User(username = username, password = password, first_name = name, email=email)
    new_user.save()
    user = authenticate(request,username=username, password=password)
    if user is not None:
        login(request,user)
        template = 'home.html'
    else:
        template = 'login.html'

    new_profile = models.Profile(user = new_user)
    new_profile.save()
    # user = models.User.objects.all().filter(username=username, password=password)
    # if not user:
    #     newUser = models.User(name=name, username=username, password=password, email=email)
    #     newUser.save()
    #     request.COOKIES['token'] = username+password
    #     template = 'home.html'
    # else:
    #     template = 'login.html'

    return render(request,template)

def checkUser(request):
    template = 'login.html'

    if request.method == "POST":
        form = request.POST
        username = form['loginUsername']
        password = form['loginPassword']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
    
            template = 'home.html'
        
        return render(request,template)

# user = models.User.objects.all().filter(username=username, password=password)
    # if user:
    #     newUser = models.User( username=username, password=password)
    #     newUser.save()
    #     request.COOKIES['token'] = username+password

@csrf_exempt
def movie_recom(request):
    if(request.method == 'GET'):
        form = request.GET  
        query = form['query']
        
        user = request.user
        profile = models.Profile.objects.get(user=user)
        search = models.Search(user = user, keyword = query)
        


        movie_recoms = index_recommend(query)
        movie_recoms = movie_recoms[:5]
        recoms_age = []
        # for i in movie_recoms:
        #     recoms_age.append([i[3:],19])
        # print(recoms_age)
        # movie_recoms = start(recoms_age)
        template = "results.html"
        print(movie_recoms)
        
        # generate and store the final result in the variable movie recoms
        # movie_recoms = ["movie1", "movie2", "movie3", "movie4","movie1", "movie2", "movie3", "movie4","movie1", "movie2", "movie3", "movie4","movie1", "movie2", "movie3", "movie4"]
        search.results = movie_recoms # change to list of movie objecs
        search.save()
        search_history = profile.search_history
        search_history.append(search)


        return render(request,template, context = {'movie_recoms':movie_recoms, 'movies':json.dumps(movie_recoms), 'total_res':str(len(movie_recoms))})

    elif(request.method == 'POST'):
        user = request.user
        profile = models.Profile.objects.get(user=user)

        data = request.POST

        movies_list = data['movies_list']
        search = models.Search.objects.filter(data['keyword']).order_by('time').values().first()
        liked_mov = []
        for movie in movies_list:
            cur_mov = models.Movies.objects.filter.first()
            if movie[1] == 'true':
                cur_mov.click_through_rate +=1
                cur_mov.save()
                liked_mov.append(cur_mov)
            
            
        search.liked_movies = liked_mov
        search.save()


# def movieInfo(models.Model):
    
