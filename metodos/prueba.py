import tweepy
import time
ckey = "wkRHi7BxWy8OzMNd1vuu9yzUU"
csecret = 'Qt8xwKMTY0VswKg5KRJAvpQxH2Oz2mutmh0FiDSnY40wQjLCHY'
atoken = '1048734440-jJr8ZW7JJycCTMtDl90oRLaQO1uX9hHV6d3eGkJ'
asecret = '5aUjQv5tgwjSkvesoeOeRgiAEUBubLct6MqIZjOrFmnYA'
OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret, 'access_token_key':atoken, 'access_token_secret':asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)


# steps not shown where you set up api
u = api.get_user(screen_name = '@MashiRafael')
print u.location
