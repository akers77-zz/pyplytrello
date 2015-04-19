__author__ = 'matt'

import peewee
from databaseAccess import *

class DatabaseUtils:
    def getCurrentPlaylist(self, partyID):
        playlist = Playlist.select().where(Playlist.partyId == partyID).order_by(Playlist.votes)

        spotifyURIs = []

        for song in playlist:
            spotifyURIs.append(song.spotifyId)

        return spotifyURIs