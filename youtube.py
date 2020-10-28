#  Copyright (c) 2020.
#  Written by Hung Vu
import os
import sys

from googleapiclient.discovery import build
from ytmusicapi import YTMusic

DEVELOPER_KEY = os.environ.get("GOOGLE_DEVELOPER_KEY")
ytmusic = YTMusic('headers_auth.json')
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)


def export_all_playlists():
    pass


def add(playlist, song):
    pass


def remove(playlist, song):
    pass


def get_songs(uri):
    pass


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__


export_all_playlists()
