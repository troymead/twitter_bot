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

credentials = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)

token = credentials.get_access_token()
sp = spotipy.Spotify(auth=token)

user_uri = 'spotify:user:1250284673' # might not need since I have playlist uri
playlist_uri = 'spotify:playlist:7nbQBgfMaCgU0R8GyNd350'

username = user_uri.split(':')[2]
playlist_id = playlist_uri.split(':')[2]

class SpotifyTwitterBot:

    FIELD_NAMES = ['song_title', 'song_uri']

    def __init__(self, tweeted_file, twitter_playlist):
        self.tweeted_file = tweeted_file
        self.twitter_playlist = twitter_playlist

    def tweeted_check(self, track_name, track_uri):
        if os.path.isfile(self.tweeted_file):
            tweeted_reader = csv.DictReader(open(self.tweeted_file), delimiter=',')
            if track_uri in tweeted_reader:
                return True
            else:
                with open(self.tweeted_file, 'a',newline='') as tweeted_csv:
                    tweeted_writer = csv.DictWriter(tweeted_csv, fieldnames=self.FIELD_NAMES)
                    tweeted_writer.writerow({'song_title' : track_name, 'song_uri' : track_uri})
        else:
            with open(self.tweeted_file, 'w', newline='') as tweeted_csv:
                tweeted_writer = csv.DictWriter(tweeted_csv, fieldnames=self.FIELD_NAMES)
                tweeted_writer.writeheader()
                tweeted_writer.writerow({'song_title' : track_name, 'song_uri' : track_uri})
        return False


    def get_random_song(self):
        tracks = self.twitter_playlist['tracks']
        item = random.choice(tracks['items'])
        while self.tweeted_check(item['track']['name'], item['track']['uri']):
            item = random.choice(tracks['items'])

        print("{0} by {1}".format(item['track']['name'], item['track']['artists'][0]['name'])) # for testing; will replace with tweeting capabilities
        print("Song link: {}".format(item['track']['external_urls']['spotify'])) # need to test printing link
    

def main():
    
    tweeted_file = os.path.join(os.getcwd(), 'already_tweeted_test.csv')
    twitter_playlist = sp.user_playlist(username, playlist_id)
    bot1 = SpotifyTwitterBot(tweeted_file, twitter_playlist)
    bot1.get_random_song() # testing
    


if __name__ == '__main__':
    main()