from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, API_BASE_URL, SECRET_KEY

from flask import Flask, redirect, request, jsonify, session
import requests
from datetime import datetime
from spotify_client import SpotifyClient
import urllib.parse

app = Flask(__name__)
app.secret_key = SECRET_KEY

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

        return redirect('/run-application')

@app.route('/run-application')
def run_application():
    #creating an instance of the SpotifyClient class
    spotify_client = SpotifyClient(
        access_token=session['access_token'],
        refresh_token=session['refresh_token'],
        expires_at=session['expires_at']
    )

    record_music(spotify_client)

    #response = spotify_client.play_album('spotify:album:2iXwKeYYKuXjalgAXtx9sd')
    #return jsonify(response.json() if response.status_code == 200 else {"message": "Playback started successfully."})

def record_music(spotify_client):
    last_update_time = datetime.now().timestamp()
    counter = 0
    update_interval = 0
    while True:
        current_time = datetime.now().timestamp()
        if current_time - last_update_time >= update_interval or counter == 0:
            response = spotify_client.get_current_track()
            print(response)

            last_update_time = current_time
            update_interval = response[2]
            print(update_interval)
            counter += 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
