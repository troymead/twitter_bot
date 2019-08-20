# troy_bot_test.py
import sys
import os
import time
import random
import csv
import tweepy
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import *

### Global Variables ###
# set up OAuth and integrate with API; twitter test
auth = tweepy.OAuthHandler(test_consumer_key, test_consumer_secret)
auth.set_access_token(test_access_token, test_access_token_secret)
api = tweepy.API(auth)

# Spotify set up
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# uri = 'spotify:user:1250284673:playlist:7nbQBgfMaCgU0R8GyNd350'
user_uri = 'spotify:user:1250284673'
playlist_uri = 'spotify:playlist:7nbQBgfMaCgU0R8GyNd350'

username = user_uri.split(':')[2]
playlist_id = playlist_uri.split(':')[2]
results = sp.user_playlist(username, playlist_id)
fieldnames = ['song_title', 'song_artist', 'song_album']

def tweeted_check(track, tweeted_file):
    if track['name'] in tweeted_file:
        return True
    else:
        return False

# function to retrieve random song from playlist
def get_random_song(results):
    for item in results['items']:
        track = item['track']
        # need already_tweeted check

def print_song(song):
    return 0

def main():
    # file handling - list of already tweeted songs contained in .csv file
    tweeted_path = os.path.join(os.getcwd(), 'already_tweeted_test.csv')
    if os.path.exists(tweeted_path):
        tweeted_file = open(tweeted_path, 'a')
    else:
        tweeted_file = open(tweeted_path, 'w+')


if __name__ == '__main__':
    main()