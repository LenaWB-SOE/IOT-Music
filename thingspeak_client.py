import requests
import datetime

class ThingSpeakClient:
    def __init__(self, music_write_api_key, environ_write_api_key):
        self.music_write_api_key = music_write_api_key
        self.environ_write_api_key = environ_write_api_key
        self.base_url = "https://api.thingspeak.com/update.json"

    def update_music_channel(self, data_dict):
        """
        Update a ThingSpeak channel with the given data dictionary.
        Args:
            data_dict (dict): Data to be sent to ThingSpeak. Should contain keys like 'song_name', 'artist', etc.
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
            'field4': data_dict.get('Radar'),
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

