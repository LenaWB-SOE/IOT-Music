from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, API_BASE_URL, SECRET_KEY, TS_FEATURES_WRITE_API_KEY, TS_SONGS_WRITE_API_KEY, TS_EVIRON_WRITE_API_KEY
from spotify_client import SpotifyClient
from thingspeak_client import ThingSpeakClient
#from sensor_client import SensorClient
from flask import Flask, redirect, request, jsonify, session
import requests
from datetime import datetime
import time
import urllib.parse
import csv
import statistics as st
import threading
import os
import time

class iot_dj:
    def __init__(self, spotify_client, thingspeak_client, sensor_client):
        #initialising variables for when a new iotdj object is created
        self.spotify_client = spotify_client
        self.thingspeak_client = thingspeak_client
        self.sensor_client = sensor_client
        self.state_playlists = {
            "Dance": "spotify:playlist:1YNBItC3Z8fvWslhJHYFuG",
            "Party background": "spotify:playlist:4TEZDSeweLF2mxg7gmOvaX",
            "Wake up": "spotify:playlist:07US4Vsv0ycWb0hTk0PLrs",
            "Going to sleep": "spotify:playlist:6ZEVixHqMVi9rHtSYP3tfQ", 
            "Evening work": "spotify:playlist:2yffgYM7klV3HkpZMRKPO7", 
            "Morning work": "spotify:playlist:7MqlcNyUCdMhDhWZYhtMYA" 
        }

    def start_recording(self):
        self.music_recording_thread = threading.Thread(target=self.record_music) 
        self.environment_recording_thread = threading.Thread(target=self.ambient_readings)
        self.music_recording_thread.start()
        self.environment_recording_thread.start()

    def record_music(self):
        last_update_time = datetime.now().timestamp()
        last_track = None
        counter = 0
        update_interval = 60

        while True:
            current_time = datetime.now().timestamp()
            
            if current_time - last_update_time >= update_interval or counter == 0:
                current_track = self.spotify_client.get_current_track()
                if current_track != None and (counter == 0 or current_track['song uri'] != last_track['song uri']):
                    print(f"Current Track: {current_track.get('song')}")
                    self.thingspeak_client.update_songs_played_channel(current_track)

                    last_track = current_track

                last_update_time = current_time
                counter += 1

    def ambient_readings(self):

        last_update_time = datetime.now().timestamp()
        update_interval = 60
        radar_data = []

        while True:
            current_time = datetime.now().timestamp()

            self.sensor_client.radar_readings_append(radar_data)

            if current_time - last_update_time >= update_interval:
                if radar_data:
                    radar_avg = st.mean(radar_data)
                    radar_stdev = st.stdev(radar_data)
                    light = self.sensor_client.light_readings()

                    environment_dict = {
                        'Light RAW': light[0],
                        'Light VOLTAGE': light[1],
                        'Radar Mean': radar_avg,
                        'Radar StDev': radar_stdev
                    }
                    self.thingspeak_client.update_environment_channel(environment_dict)
                    print(environment_dict)
                    radar_data = []

                    last_update_time = current_time

    def select_and_queue_song(self, state):
        pass


    def queue_song(self):
        # recommendation = spotify_client.create_recommendation(current_track['song_id'])
        # print(f"Song recommendation: {recommendation['song_name']}")
        waxwing = "spotify:track:4gGh7b3nKa4rlxyPLWcfTd"
        response = self.spotify_client.queue_song(waxwing)
        print(response)

    def fade_in_song(self, song_uri):
        return None


def main():
    print("Don't run this file")

if __name__ == "__main__":
    main()