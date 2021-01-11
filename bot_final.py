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

# set up OAuth and integrate with API; twitter test
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(auth)

sched = BlockingScheduler()

# for testing:
# @sched.scheduled_job('interval', minutes=5, start_date=datetime.now())
@sched.scheduled_job('cron',  hour='10,22')
def once_day():
    print('Preparing to retrieve song to tweet...')
    song = get_tweet(get_random_song())
    not_empty = song[0]

    tweepy_api.update_status(song[1])

    if (not_empty == False):
        sched.shutdown(wait=False)

sched.start()
