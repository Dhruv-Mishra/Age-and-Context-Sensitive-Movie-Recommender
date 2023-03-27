from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, StreamingHttpResponse
from . import models
from .search import *
from .recommender import *
import pandas as pd

def indexView(request):
    template = 'index.html'
    return render(request,template)

def loginView(request):
    template = "login.html"
    return render(request,template)

def signupView(request):
    template = "signup.html"
    return render(request,template)

def homeView(request):
    template = 'home.html'
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
    user = models.User.objects.all().filter(username=username, password=password)
    if not user:
        newUser = models.User(name=name, username=username, password=password, email=email)
        newUser.save()
        request.COOKIES['token'] = username+password
        template = 'home.html'        
    else:
        template = 'login.html'
    return render(request,template)

def checkUser(request):
    form = request.POST
    username = form['loginUsername']
    password = form['loginPassword']
    user = models.User.objects.all().filter(username=username, password=password)
    if user:
        newUser = models.User( username=username, password=password)
        newUser.save()
        request.COOKIES['token'] = username+password
        template = 'home.html'        
    else:
        template = 'login.html'
    
    return render(request,template)


def movie_recom(request):
    form = request.GET  
    query = form['query']
   
    movie_recoms = index_recommend(query)
    movie_recoms = movie_recoms[:1]
    recoms_age = []
    for i in movie_recoms:
        recoms_age.append([i[3:],19])
    print(recoms_age)
    movie_recoms = start(recoms_age)
    template = "results.html"
    print(movie_recoms)
    # generate and store the final result in the variable movie recoms
    # movie_recoms = ["movie1", "movie2", "movie3", "movie4","movie1", "movie2", "movie3", "movie4","movie1", "movie2", "movie3", "movie4","movie1", "movie2", "movie3", "movie4"]

    return render(request,template, context = {'movie_recoms':movie_recoms[:10], 'total_res':str(len(movie_recoms))})

    
