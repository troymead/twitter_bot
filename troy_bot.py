# troy_bot_test.py
import sys
import os
import time
import random
import tweepy
import spotipy
from spotipy import oauth2
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
# from credentials import *
from os import environ

# for heroku integration
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
SPOTIFY_CLIENT_ID = environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = environ['SPOTIFY_CLIENT_SECRET']

# TODO: figure out spotify authorization thru heroku problem
# TODO: need to clean up code where ever i can

### Global Variables ###
# Time interval for tweets (one per day - every 24 hours)
INTERVAL = 60 * 60 * 24

# set up OAuth and integrate with API; twitter test
redirect_uri = "http://localhost:8080"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(auth)

user_uri = 'spotify:user:1250284673'
username = user_uri.split(':')[2]
scope = 'playlist-modify-public'

sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(
                                                    username=username,
                                                    client_id=SPOTIFY_CLIENT_ID,
                                                    client_secret=SPOTIFY_CLIENT_SECRET,
                                                    redirect_uri=redirect_uri,
                                                    scope='playlist-modify-public'))

# playlist used for final version
# playlist_uri = 'spotify:playlist:2AVp8hX9Xaiqg9xv8qp68v'
# playlist to test if limit condition will be performed
playlist_uri = 'spotify:playlist:4CneB3XScAKgQseSXey2Yx'
at_uri = 'spotify:playlist:3b64drC4E4qkcmiOs3cJaQ'

playlist_id = playlist_uri.split(':')[2]
at_id = at_uri.split(':')[2]

# testing
# def get_token():
#     try:
#         token = util.prompt_for_user_token(username, scope)
#         environ['SPOTIPY_CACHE'] = '.cache-{username}'
#         if token:
#             sp = spotipy.Spotify(auth=token)
#             sp.trace = False
#             return sp
#         else:
#             print("Can't get token for", username)
#     except:
#         os.remove(f".cache-{username}")
#         token = util.prompt_for_user_token(username, scope)
#         if token:
#             sp = spotipy.Spotify(auth=token)
#             sp.trace = False
#             return sp
#         else:
#             print("Can't get token for", username)

class SpotifyTwitterBot:

    # sp = get_token()

    def __init__(self):
        self.twitter_playlist = sp.user_playlist(username,playlist_id)
        self.at_playlist = sp.user_playlist(username,at_id)

    def tweeted_check2(self, item):
        if any(song['track']['uri'] == item['track']['uri'] for song in self.at_playlist['tracks']['items']):
            return True
        else:
            print("Adding song to Tweeted playlist...")
            print(item['track']['uri'])
            sp.user_playlist_add_tracks(username, at_id, [item['track']['uri']]) # need to test
        return False

    # retrieves random song from playlist to send to tweet
    def get_random_song(self):
        sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(
                                                    username=username,
                                                    client_id=SPOTIFY_CLIENT_ID,
                                                    client_secret=SPOTIFY_CLIENT_SECRET,
                                                    redirect_uri=redirect_uri,
                                                    scope='playlist-modify-public'))

        # sp = get_token()

        self.twitter_playlist = sp.user_playlist(username, playlist_id) # retrieve most recent version of playlist
        self.at_playlist = sp.user_playlist(username, at_id) # retrieve most recent version of TWEETED playlist
        tracks = self.twitter_playlist['tracks']

        item = random.choice(tracks['items'])

        # need to test using already tweeted playlist
        while self.tweeted_check2(item):
            print("Already tweeted. Searching again...")
            item = random.choice(tracks['items'])
        
        # composes string to send for tweet
        tweet_string = "sotd: {0} by {1}\n{2}".format(item['track']['name'], item['track']['artists'][0]['name'], item['track']['external_urls']['spotify'])
        print(tweet_string)
        self.at_playlist = sp.user_playlist(username, at_id)
        print("number of songs already tweeted: {0} out of {1} songs".format(self.at_playlist['tracks']['total'], tracks['total']))

        tweepy_api.update_status(status=tweet_string)

        # return tweet_string

def main():

    bot1 = SpotifyTwitterBot()
    # test_interval = 60 # 60 sec interval (for testing w heroku to see behavior)
    test_interval = 60 * 10 # 10 minute interval
    # test_interval2 = 60 * 60 * 6 # 6 hour interval

    while bot1.at_playlist['tracks']['total'] <= bot1.twitter_playlist['tracks']['total']:
        bot1.get_random_song()
        # time.sleep(test_interval)
        time.sleep(test_interval) # time interval to test with heroku deployment
        # time.sleep(INTERVAL)
        if bot1.at_playlist['tracks']['total'] == bot1.twitter_playlist['tracks']['total']:
            break

    if bot1.at_playlist['tracks']['total'] >= bot1.twitter_playlist['tracks']['total']:
        tweet_string = "all songs from this playlist have been tweeted! thanks for the good time... \U0000270C"
    
    print(tweet_string)
    tweepy_api.update_status(tweet_string)

if __name__ == '__main__':
    main()