#  Copyright (c) 2020.
#  Written by Hung Vu
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from Model import Song, Playlist

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth())


def export_all_playlists():
    playlists = []
    spotify_playlists = sp.current_user_playlists()

    for spotify_playlist in spotify_playlists['items']:
        title = spotify_playlist['name']
        uri = spotify_playlist['uri']
        songs = get_songs(uri)
        print(title, len(songs))
        playlists.append(Playlist(title, songs))

    return playlists


def add(playlist, song):
    pass


def remove(playlist, song):
    pass


def get_songs(uri):
    songs = []

    offset = 0
    playlist_tracks = sp.playlist_items(playlist_id=uri, offset=offset)
    total_tracks = len(playlist_tracks['items'])
    while offset < total_tracks:
        # Create a Song object and it to the list
        for track in playlist_tracks['items']:
            offset += 1
            title = track['track']['name']
            artists = []
            for artist in track['track']['artists']:
                artists.append(artist['name'])
            songs.append(Song(title, artists))

        # Query the next 100 songs in the playlist
        playlist_tracks = sp.playlist_items(playlist_id=uri, offset=offset)
        total_tracks += len(playlist_tracks['items'])

    return songs


export_all_playlists()
