from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, API_BASE_URL, SECRET_KEY, TS_WRITE_API_KEY
from spotify_client import SpotifyClient
from thingspeak_client import ThingSpeakClient
from flask import Flask, redirect, request, jsonify, session
import requests
from datetime import datetime
import time
import urllib.parse
import csv

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

    thingspeak_client = ThingSpeakClient(TS_WRITE_API_KEY)

    record_music(spotify_client, thingspeak_client)

    #response = spotify_client.play_album('spotify:album:2iXwKeYYKuXjalgAXtx9sd')
    #return jsonify(response.json() if response.status_code == 200 else {"message": "Playback started successfully."})

"""def record_music(spotify_client):
    #writing songs to csv file
    last_update_time = datetime.now().timestamp()
    last_response = None
    counter = 0
    update_interval = 60

    fields = ['date', 'time', 'song_name', 'song_id', 'song_duration', 'progress_through_song']
    filename = "Songs_I_Played.csv"

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        while True:
            current_time = datetime.now().timestamp()
            if current_time - last_update_time >= update_interval or counter == 0:
                response = spotify_client.get_current_track()
                print(response)
                if response != None and (counter == 0 or response['song_id'] != last_response['song_id']):
                    print("yes")
                    row = response
                    writer.writerow(row)
                    csvfile.flush()
                    print("successful write")
                    last_response = response
                    #time.sleep(update_interval)

                last_update_time = current_time
                #update_interval = 60
                counter += 1"""

def record_music(spotify_client, thingspeak_client):
    last_update_time = datetime.now().timestamp()
    last_track = None
    counter = 0
    update_interval = 60

    #print(spotify_client.top_songs())

    while True:
        current_time = datetime.now().timestamp()
        if current_time - last_update_time >= update_interval or counter == 0:
            current_track = spotify_client.get_current_track()
            print(current_track)
            if current_track != None:
                track_features = spotify_client.get_track_features(current_track)
                print(track_features)
            if current_track != None and (counter == 0 or current_track['song_id'] != last_track['song_id']):
                print(f"Current Track: {current_track.get('song_name')}")
                thingspeak_client.update_channel(track_features)

                # recommendation = spotify_client.create_recommendation(current_track['song_id'])
                # print(f"Song recommendation: {recommendation['song_name']}")
                # response = spotify_client.queue_song(recommendation['song_uri'])
                # print(response)

                last_track = current_track
                #time.sleep(update_interval)

            last_update_time = current_time
            #update_interval = 60
            counter += 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
