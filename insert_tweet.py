#!/usr/bin/env python

import tweepy
import json
import requests
import chiavi
import sys
consumer_key= chiavi.consumer_key
consumer_secret= chiavi.consumer_secret
access_token= chiavi.access_token
access_token_secret= chiavi.access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

tweet_url = sys.argv[1]

tweet_id = tweet_url.split("/")[-1]

tweet = api.get_status(tweet_id, tweet_mode='extended')

data_str = json.dumps(tweet._json, indent=4)
payload = {'data': data_str} 
response = requests.post('http://127.0.0.1:5000/add_block', json=payload)

if response.status_code == 200:
    block = response.json()
    print(f"Block {block} added to the blockchain")
else:
    print('Errore nella richiesta')