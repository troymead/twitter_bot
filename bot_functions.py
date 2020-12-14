import random
import spotipy
from spotipy import oauth2
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from os import environ

SPOTIFY_CLIENT_ID = environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = environ['SPOTIFY_CLIENT_SECRET']
username = 'spotify:user:1250284673'.split(':')[2]
scope = 'playlist-modify-public'
# redirect_uri = REDIRECT_URI
redirect_uri = environ['REDIRECT_URI']

def get_random_song():
    # playlist_id = 'spotify:playlist:4CneB3XScAKgQseSXey2Yx'.split(':')[2]
    # test playlist
    playlist_id = 'spotify:playlist:7B0w4UowILfFDuWJQvwC6c'.split(':')[2]
    at_id = 'spotify:playlist:3b64drC4E4qkcmiOs3cJaQ'.split(':')[2]

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                           client_secret=SPOTIFY_CLIENT_SECRET,
                                                           redirect_uri=redirect_uri,
                                                           scope=scope
                                                           )) # need to test with heroku

    twitter_playlist = sp.playlist_items(playlist_id)
    

    if twitter_playlist['total'] == 0:
        return [False]
    else:
        tracks = twitter_playlist['items']
        song = random.choice(tracks)

        sp.playlist_add_items(at_id, [song['track']['uri']])
        sp.playlist_remove_all_occurrences_of_items(playlist_id, [song['track']['uri']])

        return [True, song['track']]

def get_tweet(song):

    if song[0] == False:
        tweet_string = "[testing] all songs from this playlist have been tweeted! thanks for the good time... \U0001F3FD"
    else:
        tweet_string = "[testing] sotd: {0} by {1}\n{2}".format(song[1]['name'], song[1]['artists'][0]['name'], song[1]['external_urls']['spotify'])
    
    return [song[0], tweet_string]
