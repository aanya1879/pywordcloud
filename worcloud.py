from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import json
import pandas as pd
#from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from flask import Flask
app = Flask(__name__)

@app.route('/<string:movie>')
def genwordcloud(movie):
    CONSUMER_KEY = 'RPZlYpV6oRbgr5QSQGNB6Ry1k'
    CONSUMER_SECRET = 'cbu85sg4TBTwLMG6nK1zM6a7q5ahTGw70WoCgqb4OBgmN2ZYQD'
    ACCESS_TOKEN = '3859620913-teEDnofOluMZIi8DNjniUmIqFtN8hxMINJ952WT'
    ACCESS_TOKEN_SECRET = 'TIijDGRetuTj5LD5hMwwMgimPvNylwmMbwTJoh4HClNTU'
    USER_NAME = 'aanyakhan1879'

    MAX_TWEETS = 111


    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth, wait_on_rate_limit=True)

    data = Cursor(api.search, q= movie).items(MAX_TWEETS)

    edu_data = []
    for tweet in data:
        edu_data.append(json.loads(json.dumps(tweet._json)))
    tweets = pd.DataFrame()
    tweets['text'] = map(lambda tweet: tweet['text'].encode('utf-8'), edu_data)
    text = " ".join(tweets['text'].values.astype(str))
    no_urls_no_tags = " ".join([word for word in text.split()
                                if 'http' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                                ])
    # edu_mask = imread("tweety_mask.png", flatten=True)

    w = WordCloud(background_color="black", max_words=50, prefer_horizontal=0.5, scale=3)  # ,mask=edu_mask)
    w.generate(no_urls_no_tags)
    w.to_file('movie.png')
    image = w.to_image()
    image.show()
    
 @app.route('/')
def index():
    print 'Hello world'
    return

if __name__ == '__main__':
    app.run(debug= True)
