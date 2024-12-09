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

TS_FEATURES_WRITE_API_KEY = os.getenv('TS_FEATURES_WRITE_API_KEY')
TS_SONGS_WRITE_API_KEY = os.getenv('TS_SONGS_WRITE_API_KEY')
TS_EVIRON_WRITE_API_KEY = os.getenv('TS_EVIRON_WRITE_API_KEY')
