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

    def convertURIsToMetadataString(self, spotifyURIs):
        stringArray = []

        for uri in spotifyURIs:
            r = requests.get('{}{}{}{}'.format(BASE_URL,ECHONEST_API_KEY,POST_URL,uri))
            if r.status_code == 200:
                response = r.json()['response']
                if response['songs']:
                    songs = response['songs']
                    artist = songs[0]['artist_name']
                    title = songs[0]['title']
                    stringArray.append(title + " by " + artist)

        return stringArray

#db = DatabaseUtils()
#uris = db.getCurrentPlaylistURIs("1234")
#strings = db.convertURIsToMetadataString(uris)
#print strings