from databaseUtils import DatabaseUtils
from trello import TrelloApi
from time import sleep
import requests
import json

#print trello.boards.get(BOARD_ID)
#print trello.boards.get_list(BOARD_ID)

#https://trello.com/1/connect?key=423732336c6a5ef68c472762809f4607&name=PyPly&response_type=token&scope=read,write
TRELLO_APP_KEY="423732336c6a5ef68c472762809f4607"
TRELLO_APP_SECRET="02d0f16c6056b2d762b111c0c6eaa4b3fd017e23dbae39fbdb4549eb750c9f66"
PARTY_ID = "1234"
BOARD_ID = "FjPBXUmk"
LIST_ID = "5533396ec0a0183d4f85dd72"
TOKEN = "c37a7594c6fb62d9794e9160e13f899808fd879bb74c751b15c9e4b175f95087"

databaseUtils = DatabaseUtils()

song1 = {"title": "Song Name 1",
         "artist": "Artist 1",
         "trelloId": "aaa",
         "spotifyId": "bbb",
         "order": 0}

def makeTrelloPlaylist(spotifyIds):
    trelloPlaylist = []
    playlistDict = {}
    for i, spotifyID in enumerate(spotifyIds):
        song = {"spotifyId": spotifyID, "order": i, "title": "", "artist": "", "trelloId": ""}
        trelloPlaylist.append(song)
        playlistDict[spotifyID] = song
    return trelloPlaylist, playlistDict

def addMetaDataTrelloPlaylist(trelloPlaylist):
    for song in trelloPlaylist:
        if not song["title"] or not song["artist"]:
            song["artist"], song["title"] = databaseUtils.convertURIToMetadata(song["spotifyId"])

def clearList(listID):
    for card in trello.lists.get_card(listID):
        trello.cards.delete(card['id'])

def updateCardPosition(cardId, position):
    resp = requests.put("https://trello.com/1/cards/%s/pos" % (cardId), params=dict(key=TRELLO_APP_KEY, token=TOKEN), data=dict(value=position))
    #resp.raise_for_status()
    #print json.loads(resp.content)

trello = TrelloApi(TRELLO_APP_KEY, token=TOKEN)


clearList(LIST_ID)
spotifyIds = databaseUtils.getCurrentPlaylistURIs(PARTY_ID)
trelloPlaylist, playlistDict = makeTrelloPlaylist(spotifyIds)
addMetaDataTrelloPlaylist(trelloPlaylist)
for song in trelloPlaylist:
    resp = trello.cards.new("{} by {}".format(song["title"], song["artist"]), LIST_ID)
    song["trelloId"] = resp["id"]


while True:
    spotifyIds = databaseUtils.getCurrentPlaylistURIs(PARTY_ID)
    for i, spotifyID in enumerate(spotifyIds):
        if not playlistDict.has_key(spotifyID):
            song = {"spotifyId": spotifyID, "order": i, "title": "", "artist": "", "trelloId": ""}
            song["artist"], song["title"] = databaseUtils.convertURIToMetadata(song["spotifyId"])
            resp = trello.cards.new("{} by {}".format(song["title"], song["artist"]), LIST_ID)
            song["trelloId"] = resp["id"]
            updateCardPosition(song["trelloId"], i)
            playlistDict[spotifyID] = song
            trelloPlaylist.append(song)
        if playlistDict.has_key(spotifyID):
            song = playlistDict.get(spotifyID)
            if song["order"] != i:
                updateCardPosition(song["trelloId"], i)
                song["order"] = i
    sleep(5)
