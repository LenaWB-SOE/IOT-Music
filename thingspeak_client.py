import requests
import datetime

class ThingSpeakClient:
    def __init__(self, music_features_write_api_key, songs_played_write_api_key, environ_write_api_key):
        self.music_features_write_api_key = music_features_write_api_key
        self.songs_played_write_api_key = songs_played_write_api_key
        self.environ_write_api_key = environ_write_api_key
        self.base_url = "https://api.thingspeak.com/update.json"

    def update_music_features_channel(self, data_dict):
        """
        Update a ThingSpeak channel with the given data dictionary.
        Args:
            data_dict (dict): Data to be sent to ThingSpeak.

        This is an archived feature and is not used in final IOT system
        """
        payload = {
            'api_key': self.music_write_api_key,
            'field1': data_dict.get('song')[0],
            'field2': data_dict.get('acousticness'),
            'field3': data_dict.get('danceability'),
            'field4': data_dict.get('energy'),
            'field5': data_dict.get('instrumentalness'),
            'field6': data_dict.get('loudness'),
            'field7': data_dict.get('tempo'),
            'field8': data_dict.get('valence')
        }
        
        try:
            response = requests.post(self.base_url, data=payload)
            if response.status_code == 200:
                print("Data successfully updated to ThingSpeak!")
                print(f"Response Content: {response.text}")
            else:
                print(f"Failed to update data. Status code: {response.status_code}")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def update_songs_played_channel(self, data_dict):
        """
        Update a ThingSpeak channel with the given data dictionary.
        Args:
            data_dict (dict): Data to be sent to ThingSpeak.
        """
        payload = {
            'api_key': self.songs_played_write_api_key,
            'field1': data_dict.get('song'),
            'field2': data_dict.get('song uri'),
            'field3': data_dict.get('artist'),
            'field4': data_dict.get('artist uri'),
            'field5': data_dict.get('album'),
            'field6': data_dict.get('album uri'),
            'field7': data_dict.get('context uri')
        }
        
        try:
            response = requests.post(self.base_url, data=payload)
            if response.status_code == 200:
                print("Data successfully updated to ThingSpeak!")
                #print(f"Response Content: {response.text}")
            else:
                print(f"Failed to update data. Status code: {response.status_code}")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def update_environment_channel(self, data_dict):
        """
        Update a ThingSpeak channel with the given data dictionary.
        Args:
            data_dict (dict): Data to be sent to ThingSpeak.
        """
        weekday = datetime.datetime.today().weekday()

        payload = {
            'api_key': self.environ_write_api_key,
            'field1': weekday,
            'field2': data_dict.get('Light RAW'),
            'field3': data_dict.get('Light VOLTAGE'),
            'field4': data_dict.get('Radar AVG'),
            'field5': data_dict.get('Radar STDEV'),
            'field6': data_dict.get('Label')
        }
        
        try:
            response = requests.post(self.base_url, data=payload)
            if response.status_code == 200:
                print("Data successfully updated to ThingSpeak!")
                print(f"Response Content: {response.text}")
            else:
                print(f"Failed to update data. Status code: {response.status_code}")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

