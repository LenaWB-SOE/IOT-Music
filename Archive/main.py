import requests
import urllib.parse

from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session


app = Flask(__name__)
app.secret_key = '2738174-1648172624-1267d'

CLIENT_ID = '362a407b4fc34e7abc359cfc77626479'
CLIENT_SECRET = 'a4c35e2f1a3f4bf285ed264d83f93029'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-modify-playback-state user-read-currently-playing user-read-recently-played user-top-read'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True #forces them to log in every time, for testing
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in'] #creating a timestamp of when the token will expire

        return redirect('/play-album')
    
@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/play-album')
    
@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()

    return jsonify(playlists)
    
@app.route('/play-album')
def play_album():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    req_body = {
        'context_uri': 'spotify:album:2iXwKeYYKuXjalgAXtx9sd'
    }
    # Romance by Fontaines: spotify:album:287QQ922OsJYh8aFNGdJG5
    # Clouds in the sky they will all by Porridge Radio: spotify:album:2iXwKeYYKuXjalgAXtx9sd

    response = requests.put(API_BASE_URL + 'me/player/play', headers=headers, json=req_body)

    # Handle response based on content presence and status code
    if response.status_code == 204:
        # 204 No Content means playback started successfully
        player = {"message": "Playback started successfully."}
    elif response.status_code == 200:
        try:
            player = response.json()
        except requests.exceptions.JSONDecodeError:
            player = {"message": "Playback started, but no JSON response."}
    else:
        # Handle unexpected responses
        player = {"error": response.status_code, "message": response.text}

    return jsonify(player)

recording_interval = 120

@app.route('/record-music')
def music_recording ():
    last_update_time = datetime.now().timestamp()
    counter = 0

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    while True:
        current_time = datetime.now().timestamp()
        if current_time - last_update_time >= recording_interval or counter == 0:
            response = requests.get(API_BASE_URL + 'me/player/currently-playing', headers=headers)
            current_track_name = response.json()["item"]["name"]
            current_track_id = response.json()["item"]["id"]
            print(current_track_name, current_track_id)

            last_update_time = current_time
            counter += 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    