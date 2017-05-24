from django.db import models

# Create your models here.


class Tweet(models.Model):
    created_at = models.DateTimeField()
    tweet_id = models.IntegerField() # id
    username = models.CharField(max_length=50) # user.screen_name
    fullname = models.CharField(max_length=50) # user.name
    followers = models.IntegerField(blank=True, null=True) #'user.followers_count',
    location = models.CharField(max_length=50, blank=True, null=True) #'user.location',

    #'user.following',
    text = models.CharField(max_length=250)
    retweet_count = models.IntegerField()
    favorite_count = models.IntegerField()

    #retweeted = models.IntegerField()
    #favorited = models.IntegerField()

