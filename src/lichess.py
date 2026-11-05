import berserk
import requests

session = requests.Session()
session.headers.update({
    "User-Agent": "ChessProfileStats/1.0" #This client identifies it self as "ChessProfileStats"
})
client = berserk.Client(session=session)


