import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# CLIENT_ID = "362a407b4fc34e7abc359cfc77626479"
# CLIENT_SECRET = "a4c35e2f1a3f4bf285ed264d83f93029"
# REDIRECT_URI = 'http://localhost:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
SECRET_KEY = '2738174-1648172624-1267d'

TS_WRITE_API_KEY = 'Q93TX2FQWU99TCBJ'

#    http://localhost:5000
#    http://100.95.76.119:5000
