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

# TODO: need to add check to see if all songs have been tweeted
# TODO: check to see if correct statement is printed when end of playlist is reached
# might test above with short playlist (2-3 songs max)
# TODO: figure out if script needs to be hosted or in venv to run continuously
# TODO: finish this damn bot...

### Global Variables ###
# set up OAuth and integrate with API; twitter test
auth = tweepy.OAuthHandler(test_consumer_key, test_consumer_secret)
auth.set_access_token(test_access_token, test_access_token_secret)
tweepy_api = tweepy.API(auth)

credentials = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)

token = credentials.get_access_token()
sp = spotipy.Spotify(auth=token)

user_uri = 'spotify:user:1250284673'
playlist_uri = 'spotify:playlist:2AVp8hX9Xaiqg9xv8qp68v'

username = user_uri.split(':')[2]
playlist_id = playlist_uri.split(':')[2]

class SpotifyTwitterBot:

    # this counter will keep track of number of songs that have already been tweeted
    # will be compared to number of songs in playlist to know when bot will stop running
    song_counter = 0

    FIELD_NAMES = ['song_title', 'song_uri']

    def __init__(self, tweeted_file, twitter_playlist):
        self.tweeted_file = tweeted_file
        self.twitter_playlist = twitter_playlist
            
    # method to check if song has been tweeted
    # checks with csv that contains list of already tweeted songs
    def tweeted_check(self, track_name, track_uri):
        if os.path.isfile(self.tweeted_file):
            tweeted_reader = csv.DictReader(open(self.tweeted_file), delimiter=',')
            values = []
            for row in tweeted_reader: # going to test getting just values of dict for tweeted check
                values.append(row['song_uri']) # only retrieves uris of previously tweeted songs
                self.song_counter += 1
            if track_uri in values:
                self.song_counter = 0
                return True
            else:
                print("Writing to already_tweeted_test.csv...")
                with open(self.tweeted_file, 'a',newline='') as tweeted_csv:
                    tweeted_writer = csv.DictWriter(tweeted_csv, fieldnames=self.FIELD_NAMES)
                    tweeted_writer.writerow({'song_title' : track_name, 'song_uri' : track_uri})
                self.song_counter += 1
        else:
            print("Creating already_tweeted_test.csv...")
            with open(self.tweeted_file, 'w', newline='') as tweeted_csv:
                tweeted_writer = csv.DictWriter(tweeted_csv, fieldnames=self.FIELD_NAMES)
                tweeted_writer.writeheader()
                tweeted_writer.writerow({'song_title' : track_name, 'song_uri' : track_uri})
            self.song_counter = 1
        return False


    # retrieves random song from playlist to send to tweet
    def get_random_song(self):
        tracks = self.twitter_playlist['tracks']
        item = random.choice(tracks['items'])

        # retrieves different song until song has not been found in already_tweeted file
        while self.tweeted_check(item['track']['name'], item['track']['uri']):
            print("Already tweeted. Searching again...") # need to test if this is working correctly
            item = random.choice(tracks['items'])
        
        # composes string to send for tweet
        tweet_string = "sotd: {0} by {1}\n{2}".format(item['track']['name'], item['track']['artists'][0]['name'], item['track']['external_urls']['spotify'])
        print(tweet_string)
        print("number of songs already tweeted: {0} out of {1} songs".format(self.song_counter, tracks['total'])) # need to test
        # need this length to include in while loop
        # while loop will also check to see if length of already_tweeted file is same as playlist length
        # if lengths are equal, then bot will tweet an end message to account

        # tweepy_api.update_status(status=tweet_string) # need to test if this will tweet...

        # return tweet_string
    

def main():
    
    tweeted_file = os.path.join(os.getcwd(), 'already_tweeted_test.csv')
    twitter_playlist = sp.user_playlist(username, playlist_id)
    bot1 = SpotifyTwitterBot(tweeted_file, twitter_playlist)
    # interval = 60 * 60 * 24

    bot1.get_random_song()
    # print(twitter_playlist)

    # hopefully this will be the loop that allows the bot to tweet once per day
    # until all songs have been tweeted
    # while bot1.song_counter < twitter_playlist['tracks']['total']:
    #     bot1.get_random_song() # testing
    #     time.sleep(interval)
    


if __name__ == '__main__':
    main()