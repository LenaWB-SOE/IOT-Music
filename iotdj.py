from datetime import datetime
import time
import statistics as st
import threading
import time
import joblib
import pandas as pd

class iot_dj:
    def __init__(self, spotify_client, sensor_client):
        #initialising variables for when a new iotdj object is created
        self.spotify_client = spotify_client
        self.sensor_client = sensor_client
        self.state_playlists = {
            "Dance": "spotify:playlist:1YNBItC3Z8fvWslhJHYFuG",
            "Wake up": "spotify:playlist:07US4Vsv0ycWb0hTk0PLrs",
            "Relaxing": "spotify:playlist:6ZEVixHqMVi9rHtSYP3tfQ", 
            "Evening work": "spotify:playlist:2yffgYM7klV3HkpZMRKPO7", 
            "Morning work": "spotify:playlist:7MqlcNyUCdMhDhWZYhtMYA" 
        }

        self.global_radar_data = []
        self.global_light_raw_data = []
        self.global_light_volt_data = []

        # Load the saved model, scaler, and encoder
        self.model = joblib.load("new_ml_models/trained_model.pkl")
        self.encoder = joblib.load("new_ml_models/label_encoder.pkl")

    def play(self):
        self.ambient_readings_thread = threading.Thread(target=self.ambient_readings)
        self.main_dj_thread = threading.Thread(target=self.main)
        self.ambient_readings_thread.start()
        self.main_dj_thread.start()

    def ambient_readings(self):
        # Runs as a thread
        # Appends ambient readings to class-wide lists

        # The light reading is taken every 10 seconds
        
        last_update_time = datetime.now().timestamp()
        light_update_interval = 10
        
        while True:
            current_time = datetime.now().timestamp()
            # The radar readings are being taken continuously
            self.sensor_client.radar_readings_append(self.global_radar_data)

            if current_time - last_update_time >= light_update_interval:
                self.sensor_client.light_raw_append(self.global_light_raw_data)
                self.sensor_client.light_voltage_append(self.global_light_volt_data)
                last_update_time = current_time


    def get_ambient_metrics(self):
        #this runs every time the programme wants to make an assessment of what playlist to play from next
        #it takes the average of all the readings recorded since the last time it was called

        radar_avg = st.mean(self.global_radar_data)
        radar_stdev = st.stdev(self.global_radar_data)
        lightraw_avg = st.mean(self.global_light_raw_data)
        lightvolt_avg = st.mean(self.global_light_volt_data)

        environment_dict = {
                    'Light RAW': [lightraw_avg],
                    'Light VOLTAGE': [lightvolt_avg],
                    'Radar AVG': [radar_avg],
                    'Radar STDEV': [radar_stdev]
                }
        
        # resetting arrays
        self.global_radar_data = []
        self.global_light_raw_data = []
        self.global_light_volt_data = []

        return environment_dict
    
    def determine_state(self, ambient_metrics):
        # This is the function that makes a prediction on the 'state' of the room based on live data
        # Possible states: Dance, Wake up, Relaxing, Evening work, Morning work, Sleeping

        new_data = pd.DataFrame.from_dict(ambient_metrics)

        # # Predict and decode
        # prediction = self.model.predict(new_data)
        # decoded_prediction = self.encoder.inverse_transform(prediction)[0]

        # print("Predicted Label:", decoded_prediction)

        #return decoded_prediction

        # Predict probabilities
        probabilities = self.model.predict_proba(new_data)

        # Get the predicted class and its confidence
        predicted_index = probabilities.argmax(axis=1)[0]  # Index of the highest probability
        confidence = probabilities[0, predicted_index]    # Confidence of the predicted class
        decoded_prediction = self.encoder.inverse_transform([predicted_index])[0]

        print("Predicted Label:", decoded_prediction)
        print("Confidence:", confidence)

        return decoded_prediction, confidence




    def select_song(self):
        read_data = self.get_ambient_metrics()
        state_selection = self.determine_state(read_data)[0]
        if state_selection == "Sleeping":
            self.spotify_client.pause_player()
            return "Paused"
        else:
            playlist_selection = self.state_playlists[state_selection]
            print(f"Playlist selection: {state_selection}")
            song_selection = self.spotify_client.get_random_song_from_playlist(playlist_selection)
        
            return song_selection
    
    def main(self):
        #runs as a thread

        is_playing = self.spotify_client.playback_state()["is_playing"]

        # If no song is playing when the code first starts running it will select and start playing a song (provided there is an active player)
        if not is_playing:
            print("not playing")
            song_selection = self.select_song()
            self.spotify_client.play_song(song_selection)

        while True:
            playback_state = self.spotify_client.playback_state()
            if playback_state["is_playing"]:
                song_duration = playback_state["song_duration"]
                time_into_song = playback_state["time_into_song"]
                time_left_s = (song_duration - time_into_song)/1000
                print(time_left_s)
                time.sleep(time_left_s - 10) #delays until it is 10 seconds until the end of the song

                song_selection = self.select_song()
                self.spotify_client.queue_song(song_selection)
                time.sleep(11)

                #what happens if someone skips a song and doesn't let it play all the way through?
            else:
                print("Paused")