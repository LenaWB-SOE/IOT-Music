from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, API_BASE_URL, SECRET_KEY, TS_FEATURES_WRITE_API_KEY, TS_SONGS_WRITE_API_KEY, TS_EVIRON_WRITE_API_KEY
from spotify_client import SpotifyClient
from thingspeak_client import ThingSpeakClient
from sensor_client import SensorClient
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
import random

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

        self.global_radar_data = []
        self.global_light_raw_data = []
        self.global_light_volt_data = []

    def start_recording(self):
        self.music_recording_thread = threading.Thread(target=self.record_music) 
        self.environment_recording_thread = threading.Thread(target=self.ambient_readings)
        self.music_recording_thread.start()
        self.environment_recording_thread.start()
        #self.current_track = None

    def record_music_data(self):
        # For data collection
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

    def record_ambient_data(self):
        # This is a function for recording the ambient condition data and taking an average at regular intervals
        # This is for the purpose of data collection for data analysis and does not run when the iot_dj is actually playing

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

    def ambient_readings(self):
        # To run as a thread when in playing state
        # Appends readings to class-wide lists

        # The light reading is taken every 10 seconds
        current_time = datetime.now().timestamp()
        last_update_time = datetime.now().timestamp()
        light_update_interval = 10
        
        while True:
            # The radar readings are being taken continuously
            self.sensor_client.radar_readings_append(self.gloabl_radar_data)

            if current_time - last_update_time >= light_update_interval:
                self.sensor_client.light_raw_append(self.gloabl_light_raw_data)
                self.sensor_client.light_voltage_append(self.gloabl_light_volt_data)

    def get_ambient_metrics(self):
        #this runs every time the programme wants to make an assessment of what playlist to play from next
        #it takes the average of all the readings recorded since the last time it was called

        radar_avg = st.mean(self.gloabl_radar_data)
        radar_stdev = st.stdev(self.gloabl_radar_data)
        lightraw_avg = st.mean(self.global_light_raw_data)
        lightvolt_avg = st.mean(self.gloabl_light_volt_data)

        environment_dict = {
                    'Light RAW': lightraw_avg,
                    'Light VOLTAGE': lightvolt_avg,
                    'Radar Mean': radar_avg,
                    'Radar StDev': radar_stdev
                }
        
        # resetting arrays
        self.global_radar_data = []
        self.global_light_raw_data = []
        self.global_light_volt_data = []

        return environment_dict
    
    def determine_state(self):
        # Should take ambient_metrics as parameter eventually
        # This is the function that makes a decision based on data
        possible_states = ["Dance", "Party background", "Wake up", "Going to sleep", "Evening work", "Morning work"]
        state = possible_states[random.randint(0,5)]
        return "Dance"

    def select_song(self):
        #self.get_ambient_metrics
        state_selection = self.determine_state()
        playlist_selection = self.state_playlists[state_selection]
        song_selection = self.spotify_client.get_random_song_from_playlist(playlist_selection)
        
        return song_selection
    
    def main(self):
        #starts running when the code is run

        is_playing = self.spotify_client.playback_state()["is_playing"]

        if not is_playing:
            print("not playing")
            song_selection = self.select_song()
            self.spotify_client.play_song(song_selection)

        while True:
            print("playing")
            playback_state = self.spotify_client.playback_state()
            song_duration = playback_state["song_duration"]
            time_into_song = playback_state["time_into_song"]
            time_left_s = (song_duration - time_into_song)/1000
            print(time_left_s)
            time.sleep(time_left_s - 10) #delays until it is 10 seconds until the end of the song

            song_selection = self.select_song()
            self.spotify_client.queue_song(song_selection)
            time.sleep(11)

            #what happens if someone skips a song and doesn't let it play all the way through?