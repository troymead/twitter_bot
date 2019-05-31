# troy_bot.py
import sys
import os
import time
import random
import tweepy
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import *

# set up OAuth and integrate with API; twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Spotify set up
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
uri = 'spotify:user:1250284673:playlist:7nbQBgfMaCgU0R8GyNd350'
username = uri.split(':')[2]
playlist_id = uri.split(':')[4]
results = sp.user_playlist(username, playlist_id)

# file handling - list of already tweeted songs
tweeted_path = os.path.join(os.getcwd(), 'already_tweeted.txt')
if os.path.exists(tweeted_path):
    tweeted_file = open(tweeted_path, 'a')
else:
    tweeted_file = open(tweeted_path, 'w+')


# write tweet to push to twitter account
tweet = 'Song of the Day: '
api.update_status(status=tweet)
already_tweeted = []
tweeted_txt = open('already_tweeted.txt', '')

# time sleep for later use
# time.sleep(86400)

# function to send tweet of a song
# tweets song name, artist, and link to the song on Spotify
def tweet():
    # api.update_status('test')
    print('test')
    # time.sleep(86400)
    return 0

# returns url of a song to tweet
def song_url(song_info):
    return 0

def get_random_song(results):
    item = random.choice(results['items'])
    track = item['track']
    if track in already_tweeted:
        get_random_song(results)
    else:
        already_tweeted.append(track)
        return track['name'] + ' - ' + track['artists'][0]['name']

def get_song(results):
    # need to use random.choice to get random song from playlist
    for item in results['items']:
        track = item['track']
        if track['name'] in already_tweeted:

        # placeholder for tweet - using print for now
        print(track['name'] + ' - ' + track['artists'][0]['name'])
        new_tweet = track['name'] + ' - ' + track['artists'][0]['name']

def main():
    return 0

if __name__ == '__main__':
    main()
