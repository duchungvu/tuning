import spotipy
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

load_dotenv()
DEVELOPER_KEY=os.environ.get("GOOGLE_DEVELOPER_KEY")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
ytmusic = YTMusic('headers_auth.json')

youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

def get_tracks_from_playlist(uri):
    videoIds = []

    playlist = sp.playlist_items(uri)
    for track in playlist['items']:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']

        music_search = ytmusic.search(track_name)
        videoId = None
        if len(music_search) > 0:
            videoId = music_search[0]['videoId']
        else:
            query = track_name + " " + artist_name
            print(query)
            video_search = youtube.search().list(q=track_name, part="snippet", maxResults=1).execute()
            # print(video_search['items'])
            videoId = video_search['items'][0]['id']['videoId']

        if videoId:
            videoIds.append(videoId)

    return videoIds

def get_tracks_from_Ids(videoIds):
    for id in videoIds:
        song = ytmusic.get_song(id)
        print(song['title'])

# def get_all_spotify_playlists():
#     playlists = sp.current_user_playlists()
#     uri = playlists['items'][4]['uri']
#     print(uri)
#     response = sp.playlist_items(uri)
#     for track in response['items']:
#         print(track['track']['name'], '-', track['track']['artists'][0]['name'])

uri = sp.current_user_playlists()['items'][0]['uri']

videoIds = get_tracks_from_playlist(uri)

get_tracks_from_Ids(videoIds)