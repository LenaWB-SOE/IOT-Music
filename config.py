import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
SECRET_KEY = '2738174-1648172624-1267d'

TS_MUSIC_WRITE_API_KEY = 'Q93TX2FQWU99TCBJ'
TS_SONGS_WRITE_API_KEY = 'HPTCUKDI4S81NS5S'
TS_EVIRON_WRITE_API_KEY = '3GJFOHYMTI621JM1'


#Things to copy
#    http://localhost:5000
#    http://100.95.76.119:5000
#    https://raspberrypi.tail4f3c46.ts.net
#    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
