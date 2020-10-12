import spotipy
import os
from dotenv import load_dotenv
import sys
from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

load_dotenv()
DEVELOPER_KEY = os.environ.get("GOOGLE_DEVELOPER_KEY")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
ytmusic = YTMusic('headers_auth.json')
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)


def get_playlist_info(playlist):
    title = playlist['name']
    uri = playlist['uri']
    video_ids = []

    print("Finding songs for {}...".format(title))
    offset = 0
    playlist_tracks = sp.playlist_items(playlist_id=uri, offset=offset)
    total = len(playlist_tracks['items'])
    while total > 0:
        for track in playlist_tracks['items']:
            offset += 1
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            if track_name == "":
                continue
            query = track_name + " " + artist_name

            blockPrint()
            music_songs_search = ytmusic.search(query, filter="songs")
            music_videos_search = ytmusic.search(query, filter="videos")
            enablePrint()

            if len(music_songs_search) > 0:
                print("[{}/{}] Music song search: {} | {}".format(offset, total, music_songs_search[0]['title'],
                                                                  track_name))
                video_id = music_songs_search[0]['videoId']
            elif len(music_videos_search) > 0:
                print("[{}/{}] Music video search: {} | {}".format(offset, total, music_songs_search[0]['title'],
                                                                   track_name))
                video_id = music_songs_search[0]['videoId']
            else:
                video_search = youtube.search().list(q=query, part="snippet", maxResults=1).execute()
                print("[{}/{}] Video search: {}".format(offset, total, video_search['items'][0]['snippet']['title'],
                                                        track_name))
                video_id = video_search['items'][0]['id']['videoId']

            if video_id:
                video_ids.append(video_id)

        playlist_tracks = sp.playlist_items(playlist_id=uri, offset=offset)
        total = len(playlist_tracks['items'])

    return title, video_ids


def import_playlist(playlist):
    title, video_ids = get_playlist_info(playlist)
    print("Creating playlist: {}, with {} songs...".format(title, len(video_ids)))
    ytmusic.create_playlist(title, description="", video_ids=video_ids)
    print("Created playlist: {}, with {} songs.".format(title, len(video_ids)))


def import_all_playlists():
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        import_playlist(playlist)


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__


import_all_playlists()
