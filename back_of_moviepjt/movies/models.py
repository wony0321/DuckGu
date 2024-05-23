from django.db import models
from django.conf import settings

# Create your models here.


class Keyword(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    genre = models.CharField(max_length=20)
    origin_country = models.CharField(max_length=20)
    era = models.CharField(max_length=10)


class Movie(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    keywords = models.ManyToManyField(Keyword)
    title = models.CharField(max_length=100)
    poster_path = models.TextField()
    vote_average = models.FloatField()
    release_date = models.DateField()
    over_view = models.TextField()


class Meet(models.Model):
    keywords = models.ManyToManyField('Keyword', related_name='meets_keywords')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='meets_users')
    name = models.CharField(max_length=20)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meet_admin')


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.FloatField()
    content = models.TextField()
