__author__ = 'matt'

from databaseAccess import *
import requests

ECHONEST_API_KEY="S0QUTXZNEZ6GNVKST"
BASE_URL="http://developer.echonest.com/api/v4/song/profile?api_key="
POST_URL="&format=json&bucket=id:spotify&track_id="

class DatabaseUtils:

    def getCurrentPlaylistURIs(self, partyID):
        playlist = Playlist.select().where(Playlist.partyId == partyID).order_by(Playlist.votes.desc())

        spotifyURIs = []

        for song in playlist:
            spotifyURIs.append(song.spotifyId)

        return spotifyURIs

    def convertURIToMetadata(self, spotifyURI):
        artist = ""
        title = ""
        r = requests.get('{}{}{}{}'.format(BASE_URL,ECHONEST_API_KEY,POST_URL,spotifyURI))
        if r.status_code == 200:
            response = r.json()['response']
            if response['songs']:
                artist = response['songs'][0]['artist_name']
                title = response['songs'][0]['title']
        return artist, title

    def convertURIsToMetadataString(self, spotifyURIs):
        songStrings = []
        for uri in spotifyURIs:
            artist, title = self.convertURIToMetadata(uri)
            songStrings.append(title + " by " + artist)
        return songStrings

#db = DatabaseUtils()
#uris = db.getCurrentPlaylistURIs("1234")
#strings = db.convertURIsToMetadataString(uris)
#print strings