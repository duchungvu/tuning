#  Copyright (c) 2020.
#  Written by Hung Vu
import os
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build
from ytmusicapi import YTMusic

from Model import Song, Playlist

load_dotenv()
DEVELOPER_KEY = os.environ.get("GOOGLE_DEVELOPER_KEY")
ytmusic = YTMusic('headers_auth.json')
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

# Number of maximum songs in a playlist
MAX_SONGS = 1000


def export_all_playlists():
    """
    Get all YouTube Music playlists and convert them to standard playlist model
    :return: A list of available playlists
    """
    playlists = []
    youtube_playlists = ytmusic.get_library_playlists()

    for youtube_playlist in youtube_playlists:
        title = youtube_playlist['title']
        playlist_id = youtube_playlist['playlistId']
        # Skip 'Your Likes' playlist
        if title == 'Your Likes':
            continue
        songs = get_songs(playlist_id)
        print(title, len(songs))
        playlists.append(Playlist(title, songs))

    return playlists


def add(playlist, song):
    """
    Add a song to the playlist
    :param playlist: The playlist to be added
    :param song: The song to be added
    """
    pass


def remove(playlist, song):
    """
    Remove a song from the playlist
    :param playlist: The playlist to be removed
    :param song: The song to be removed
    """
    pass


def get_songs(playlist_id):
    """
    Get all songs from a specific playlist and convert them to standard song model
    :param playlist_id: The ID of the playlist
    :return: A list of the songs in the playlist
    """
    songs = []

    playlist_tracks = ytmusic.get_playlist(playlist_id, MAX_SONGS)["tracks"]
    for track in playlist_tracks:
        title = track['title']
        artists = []
        for artist in track['artists']:
            artists.append(artist['name'])
        song = Song(title, artists)
        songs.append(song)

    return songs


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__


export_all_playlists()
