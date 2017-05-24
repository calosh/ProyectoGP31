html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story a">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

import HTMLParser
from bs4 import BeautifulSoup


html_doc = BeautifulSoup(open('/home/calosh/Desktop/tweet.html'))

clase_tweet1 = '''tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content
       original-tweet js-original-tweet

       has-cards  has-content
'''


clase_tweet2 = '''tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content
       original-tweet js-original-tweet


'''

clase_tweet3= '''tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content
       original-tweet js-original-tweet

       has-cards
'''

#clase_tweetF = '''tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet has-cards has-forward '''

tweets = html_doc.find_all('div',class_=clase_tweet1)
tweets = tweets + html_doc.find_all('div',class_=clase_tweet2)
tweets = tweets + html_doc.find_all('div',class_=clase_tweet3)





print type(tweets)
print tweets
cont = 0

for i in tweets:

    cont = cont + 1

    print "Tweet: %s" %cont

    print i.find('strong', class_="fullname show-popup-with-id ").get_text()

    print i.find('span', class_="username u-dir").get_text()

    print i.find('p', class_="TweetTextSize js-tweet-text tweet-text").get_text()

    date = i.find('a', class_="tweet-timestamp js-permalink js-nav js-tooltip")

    print date['title']

    valoraciones = i.find_all('span',class_="ProfileTweet-actionCountForAria")


    for valoracion in valoraciones:
        #print valoracion
        #print valoracion.find('span', class_="ProfileTweet-actionCountForAria")
        print valoracion.get_text()



