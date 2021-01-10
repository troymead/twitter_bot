import sys
import os
import time
import random
import tweepy
from datetime import datetime
from os import environ
from bot_functions import get_random_song, get_tweet
from apscheduler.schedulers.blocking import BlockingScheduler

# for heroku integration
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

# Time interval for tweets (one per day - every 24 hours)
# INTERVAL = 60 * 60 * 24
INTERVAL = 60 * 30 # heroku deploy test interval
INTERVAL2 = 60

# set up OAuth and integrate with API; twitter test
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(auth)

# not_empty = True

sched = BlockingScheduler()

# @sched.scheduled_job('cron', day_of_week='', hour=)
# for testing:
@sched.scheduled_job('interval', hours=1, start_date=datetime.now())
def once_day():
    print('Preparing to retrieve song to tweet...')
    song = get_tweet(get_random_song())
    not_empty = song[0]
    print(song[1])

    if (not_empty):
        print(song[1])
        tweepy_api.update_status(song[1]) # for final
        # sched.shutdown(wait=False)
    else:
        print(song[1])
        tweepy_api.update_status(song[1]) # for final
        sched.shutdown(wait=False)

sched.start()

# while not_empty:
#     print('Preparing to retrieve song to tweet...')

#     song = get_tweet(get_random_song())
#     not_empty = song[0]
#     # tweepy_api.update_status(song[1]) # for final



#     if not_empty:
#         time.sleep(INTERVAL)
