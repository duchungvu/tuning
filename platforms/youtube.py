#  Copyright (c) 2020.
#  Written by Hung Vu
import os
import re
import sys
import Levenshtein
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

STOP_RATIO = 0.8
MIN_RATIO = 0.5


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
        print(youtube_playlist)
        if title == 'Your Likes':
            continue
        songs = get_songs(playlist_id)
        print(title, len(songs))
        playlists.append(Playlist(title, songs))

    return playlists


def import_playlist(playlist):
    print("Creating playlist: {}...".format(playlist.get_title()))
    title, video_ids = create_playlist(playlist)
    res = ytmusic.create_playlist(title, description="", video_ids=video_ids)
    print("Created playlist: {}, with {} songs.".format(title, len(video_ids)))
    print(res)
    print()


def create_playlist(playlist):
    video_ids = []
    for song in playlist.get_songs():
        title = re.sub(r'\([^)]*\)', '', song.get_title())
        query = str(song)
        blockPrint()
        music_songs = ytmusic.search(query, filter="songs")
        music_videos = ytmusic.search(query, filter="videos")
        youtube_videos = youtube.search().list(q=query, part="snippet", maxResults=10).execute()['items']
        enablePrint()

        res_title, ratio, video_id = get_best_song(title, music_songs, music_videos, youtube_videos)

        print(title, '|', res_title, '|', ratio)
        if ratio >= MIN_RATIO:
            video_ids.append(video_id)

    print(len(video_ids), len(playlist.get_songs()))
    return playlist.get_title(), video_ids


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


def get_best_song(title, music_songs, music_videos, youtube_videos):
    video_id = ""
    max_ratio = 0
    res_title = ""

    for music_song in music_songs:
        t = re.sub(r'\([^)]*\)', '', music_song['title'])
        ratio = Levenshtein.ratio(title, t)
        if max_ratio < ratio:
            max_ratio = ratio
            video_id = music_song['videoId']
            res_title = t
        if max_ratio >= STOP_RATIO:
            return res_title, max_ratio, video_id

    for music_video in music_videos:
        t = re.sub(r'\([^)]*\)', '', music_video['title'])
        ratio = Levenshtein.ratio(title, t)
        if max_ratio < ratio:
            max_ratio = ratio
            video_id = music_video['videoId']
            res_title = t
        if max_ratio >= STOP_RATIO:
            return res_title, max_ratio, video_id

    for youtube_video in youtube_videos:
        snippet = youtube_video['snippet']
        t = re.sub(r'\([^)]*\)', '', snippet['title'])
        ratio = Levenshtein.ratio(title, t)
        if max_ratio < ratio:
            max_ratio = ratio
            video_id = snippet['videoId']
            res_title = t
        if max_ratio >= STOP_RATIO:
            return res_title, max_ratio, video_id

    return res_title, max_ratio, video_id


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__
