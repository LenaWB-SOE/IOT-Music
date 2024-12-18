from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, API_BASE_URL, SECRET_KEY, TS_FEATURES_WRITE_API_KEY, TS_SONGS_WRITE_API_KEY, TS_EVIRON_WRITE_API_KEY
from spotify_client import SpotifyClient
#from thingspeak_client import ThingSpeakClient
from sensor_client import SensorClient
from flask import Flask, redirect, request, jsonify, session
import requests
from datetime import datetime
import urllib.parse # a module used here for combining components into URLs easily
from iotdj import iot_dj

# Approximately 90% of the code in this file came from the YouTube Tutorial by Imdad Codes: 'Spotify API OAuth - Automate Getting User Playlists (Complete Tutorial)' https://www.youtube.com/watch?v=olY_2MW4Eik
# Flask Quickstart documentation was also referred to: https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application
# This was used as a framework to both understand OAuth 2.0 and Flask and implement it for my own specific use in def run_application

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    #scope = 'user-read-private user-read-email user-modify-playback-state user-read-currently-playing user-read-recently-played user-top-read user-read-playback-state'
    scope = 'user-modify-playback-state user-read-playback-state'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True #forces user to log in every time, for testing
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
    #thingspeak_client = ThingSpeakClient(TS_FEATURES_WRITE_API_KEY, TS_SONGS_WRITE_API_KEY, TS_EVIRON_WRITE_API_KEY)

    #creating an instance of the SensorClient class
    sensor_client = SensorClient()

    #creating an instance of the iot_dj class
    IOT_DJ = iot_dj(spotify_client, sensor_client)

    #creating and instance of the DataAnalysisClass
    #Data_Analysis = DataAnalysisClass("ambient_data.csv")
    #Data_Analysis.pairplot()

    #IOT_DJ.start_recording()
    #IOT_DJ.record_music()
    #IOT_DJ.ambient_readings()
    #spotify_client.play_album("spotify:playlist:37i9dQZF1EQpVaHRDcozEz")
    #song_selection = spotify_client.get_random_song_from_playlist("spotify:playlist:1YNBItC3Z8fvWslhJHYFuG")
    #spotify_client.play_song(song_selection)

    #spotify_client.playback_state()
    #IOT_DJ.main()
    #IOT_DJ.record_ambient_data("Dancing")
    IOT_DJ.play()


    return redirect('/next')
    #return None

@app.route('/next')
def next():
    
    return "The IoT DJ is running!! :D"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)