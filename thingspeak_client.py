import requests

class ThingSpeakClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.thingspeak.com/update.json"

    def update_channel(self, data_dict):
        """
        Update a ThingSpeak channel with the given data dictionary.
        Args:
            data_dict (dict): Data to be sent to ThingSpeak. Should contain keys like 'song_name', 'artist', etc.
        """
        payload = {
            'api_key': self.api_key,
            'field1': data_dict.get('date'),
            'field2': data_dict.get('time'),
            'field3': data_dict.get('song_name'),
            'field4': data_dict.get('song_id'),
            'field5': data_dict.get('song_duration'),
            'field6': data_dict.get('progress_through_song')
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

