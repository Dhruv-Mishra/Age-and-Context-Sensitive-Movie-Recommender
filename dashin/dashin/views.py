from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, StreamingHttpResponse
from . import models

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

    template = "results.html"
    print(form)
    # generate and store the final result in the variable movie recoms
    movie_recoms = ["movie1", "movie2", "movie3", "movie4","movie1", "movie2", "movie3", "movie4","movie1", "movie2", "movie3", "movie4","movie1", "movie2", "movie3", "movie4"]

    return render(request,template, context = {'movie_recoms':movie_recoms, 'total_res':str(len(movie_recoms))})

    
