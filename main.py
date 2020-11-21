from platforms import spotify, youtube


def test():
    print("Exporting Spotify playlists...")
    playlists = spotify.export_all_playlists()
    print("Exported Spotify {} playlist.".format(len(playlists)))
    for playlist in playlists:
        youtube.import_playlist(playlist)


test()
