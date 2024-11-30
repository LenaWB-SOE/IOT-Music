import requests
from datetime import datetime
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, API_BASE_URL

class SpotifyClient:
    def __init__(self, access_token=None, refresh_token=None, expires_at=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def is_token_expired(self):
        return datetime.now().timestamp() > self.expires_at

    def refresh_token_func(self):
        if not self.refresh_token:
            raise Exception("No refresh token available")

        response = requests.post(TOKEN_URL, data={
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })
        
        token_info = response.json()
        self.access_token = token_info['access_token']
        self.expires_at = datetime.now().timestamp() + token_info['expires_in']
        return self.refresh_token

    def get_headers(self):
        if self.is_token_expired():
            self.refresh_token_func()
        return {'Authorization': f"Bearer {self.access_token}"}

    def get_current_track(self):
        response = requests.get(f"{API_BASE_URL}me/player/currently-playing", headers=self.get_headers())
        if response.status_code == 200:
            current_track = {
                'song': response.json()["item"]["name"],
                'song uri': response.json()["item"]["uri"],
                'artist': response.json()["item"]["artists"][0]["name"],
                'artist uri': response.json()["item"]["artists"][0]["uri"],
                'album': response.json()["item"]["album"]["name"],
                'album uri': response.json()["item"]["album"]["uri"],
                'context uri': response.json()["context"]["uri"]
            }
            return current_track
        return None
    
    def queue_song(self, song_uri):
        response = requests.post(f"{API_BASE_URL}me/player/queue?uri={song_uri}", headers=self.get_headers())
        print(f"Error {response.status_code}: {response.text}")
        if response.status_code == 200:
            print("Song queued")
        return response
    
    def play_album(self, album_uri):
        response = requests.put(f"{API_BASE_URL}me/player/play", headers=self.get_headers(), json={'context_uri': album_uri})
        if response.status_code == 204:
            print("Album/playlist playing")
        else:
            print(f"Error {response.status_code}: {response.text}")
        return response
    
    def play_song(self, song_uri):
        response = requests.put(f"{API_BASE_URL}me/player/play", headers=self.get_headers(), json={'uris': [song_uri]})
        if response.status_code == 204:
            print("Song playing")
        else:
            print(f"Error {response.status_code}: {response.text}")
        return response
    
    def set_volume(self, volume):
        response = requests.put(f"{API_BASE_URL}me/player/volume?volume_percent={volume}", headers=self.get_headers())
        if response.status_code == 204:
            print("volume set")
        else:
            print(f"Error {response.status_code}: {response.text}")
        return response
    
    def top_songs(self):
        response = requests.get(f"{API_BASE_URL}me/top/{'tracks'}/", headers=self.get_headers(), json={'time_range': 'long_term', 'limit': 20})
        return response.json()['items']
