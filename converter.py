import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
ytmusic = YTMusic('headers_auth.json')


def get_all_spotify_playlists():
    playlists = sp.current_user_playlists()
    uri = playlists['items'][4]['uri']
    print(uri)
    response = sp.playlist_items(uri)
    for track in response['items']:
        print(track['track']['name'], '-', track['track']['artists'][0]['name'])

def create_playlist():
    ytmusic.create_playlist(title="Test", description="")

get_all_spotify_playlists()
