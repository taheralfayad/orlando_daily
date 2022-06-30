import tweepy
import requests
import json
import http.client, urllib.parse
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

twitter_consumer = os.getenv('twitter_consumer')
twitter_secret = os.getenv('twitter_secret')
twitter_access = os.getenv('twitter_access')
twitter_access_secret = os.getenv('twitter_access_secret')

weather_key = os.getenv('weather_key')

mediastack_access_key= os.getenv('mediastack_access_key')

mediastack =  http.client.HTTPConnection('api.mediastack.com')

params_mediastack = urllib.parse.urlencode({
    'access_key': mediastack_access_key,
    'categories': 'general',
    'countries': 'us',
    'limit': 3,
    'keywords': "florida",
    'date': datetime.today().strftime('%Y-%m-%d'),
    })

mediastack = requests.get("http://api.mediastack.com/v1/news?{}".format(params_mediastack))

headlinesDirty = mediastack.json()

headlines = ["", "", ""]

for i in range(len(headlinesDirty['data'])):
   headlines[i] = headlinesDirty['data'][i]['title']

weather = requests.get("http://api.weatherapi.com/v1/current.json?key={}&q=Orlando".format(weather_key))

weather_request_jsonify = weather.json()

temperature = weather_request_jsonify['current']['temp_f']

condition = weather_request_jsonify['current']['condition']

auth = tweepy.OAuthHandler(twitter_consumer, twitter_secret)

auth.set_access_token(twitter_access, twitter_access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

api.update_status("Hello Orlando,\n\n" + f"Expect it to be {condition['text']} with temp: {temperature}f\n\n" + "Latest headlines:\n" + headlines[1] + "\n" + headlines[2])

