from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, API_BASE_URL, SECRET_KEY, TS_MUSIC_WRITE_API_KEY, TS_EVIRON_WRITE_API_KEY
from spotify_client import SpotifyClient
from thingspeak_client import ThingSpeakClient
from flask import Flask, redirect, request, jsonify, session
import requests
from datetime import datetime
import time
import urllib.parse
import csv
from iotdj import iot_dj

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

        return redirect('/run-application')

@app.route('/run-application')
def run_application():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        print("refresh token")
        return redirect('/refresh-token')
    
    #creating an instance of the SpotifyClient class
    spotify_client = SpotifyClient(
        access_token=session['access_token'],
        refresh_token=session['refresh_token'],
        expires_at=session['expires_at']
    )

    #creating an instance of the ThingSpeakClient class
    thingspeak_client = ThingSpeakClient(TS_MUSIC_WRITE_API_KEY, TS_EVIRON_WRITE_API_KEY)

    #creating an instance of the iot_dj class
    IOT_DJ = iot_dj(spotify_client, thingspeak_client)

    IOT_DJ.record_music()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)