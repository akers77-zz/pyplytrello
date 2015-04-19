__author__ = 'matt'

from trello import TrelloApi

TRELLO_APP_KEY="423732336c6a5ef68c472762809f4607"
TRELLO_APP_SECRET="02d0f16c6056b2d762b111c0c6eaa4b3fd017e23dbae39fbdb4549eb750c9f66"

trello = TrelloApi(TRELLO_APP_KEY)
trello.boards.get('4d5ea62fd76aa1136000000c')
