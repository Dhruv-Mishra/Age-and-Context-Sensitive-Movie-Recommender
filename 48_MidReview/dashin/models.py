from django.db import models


class User(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=15)
    email = models.CharField(max_length=200)
