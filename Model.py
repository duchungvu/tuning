#  Copyright (c) 2020.
#  Written by Hung Vu


class Song:
    def __init__(self, title, artists):
        self._title = title
        self._artists = artists

    def get_title(self):
        return self._title

    def get_artists(self):
        return self._artists

    def __str__(self):
        return "{} - {}".format(self._title, ', '.join(self._artists))


class Playlist:
    def __init__(self, title, songs):
        self._title = title
        self._songs = songs

    def get_title(self):
        return self._title

    def get_songs(self):
        return self._songs
