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
    while offset < total:
        for track in playlist_tracks['items']:
            offset += 1
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            if track_name == "":
                print("[{}/{}] Skipped".format(offset, total))
                continue
            query = track_name + " " + artist_name

            blockPrint()
            music_songs_search = ytmusic.search(query, filter="songs")
            music_videos_search = ytmusic.search(query, filter="videos")
            enablePrint()

            if len(music_songs_search) > 0:
                searched_type = "Music song"
                searched = music_songs_search[0]
            elif len(music_videos_search) > 0:
                searched_type = "Music video"
                searched = music_songs_search[0]
            else:
                video_search = youtube.search().list(q=query, part="snippet", maxResults=1).execute()
                searched_type = "Video"
                searched = video_search['items'][0]['snippet']

            if searched:
                if searched['videoId'] not in video_ids:
                    video_ids.append(searched['videoId'])
                    print("[{}/{}] {} search: {} | {}".format(offset, total, searched_type, track_name,
                                                              searched['title']))
                else:
                    print("[{}/{}] {} search: {} | {} | DUPLICATED".format(offset, total, searched_type, track_name, searched['title']))
            else:
                print("[{}/{}] Nothing found: {}".format(offset, total, track_name))

        playlist_tracks = sp.playlist_items(playlist_id=uri, offset=offset)
        total += len(playlist_tracks['items'])

    return title, video_ids


def import_playlist(playlist):
    title, video_ids = get_playlist_info(playlist)
    print("Creating playlist: {}, with {} songs...".format(title, len(video_ids)))
    res = ytmusic.create_playlist(title, description="", video_ids=video_ids)
    print("Created playlist: {}, with {} songs.".format(title, len(video_ids)))
    print(res)


def import_all_playlists():
    playlists = sp.current_user_playlists()
    # playlist = playlists['items'][0]
    # import_playlist(playlist)
    for playlist in playlists['items']:
        import_playlist(playlist)


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__


import_all_playlists()
