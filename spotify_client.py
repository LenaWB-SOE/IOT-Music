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

    def refresh_token(self):
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

    def get_headers(self):
        if self.is_token_expired():
            self.refresh_token()
        return {'Authorization': f"Bearer {self.access_token}"}

    def play_album(self, album_uri):
        response = requests.put(f"{API_BASE_URL}me/player/play", headers=self.get_headers(), json={'context_uri': album_uri})
        return response

    def get_current_track(self):
        response = requests.get(f"{API_BASE_URL}me/player/currently-playing", headers=self.get_headers())
        if response.status_code == 200:
            current_track = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M'),
                'song_name': response.json()["item"]["name"],
                'artist': response.json()["item"]["artists"]["name"],
                'song_id': response.json()["item"]["id"],
                'song_duration': response.json()["item"]["duration_ms"],
                'progress_through_song': response.json()["progress_ms"]
            }
            return current_track
        return None
    
    def get_track_features(self, track):
        SONG_ID = track['song_id']
        response = requests.get(f"{API_BASE_URL}audio-features/{SONG_ID}", headers=self.get_headers())
        if response.status_code == 200:
            song_features = {
                'song': [track['song_name'], track['artist'], track['song_id']],
                'acousticness': response.json()['acousticness'],
                'danceability': response.json()['danceability'],
                'energy': response.json()['energy'],
                'instrumentalness': response.json()['instrumentalness'],
                'loudness': response.json()['loudness'],
                'tempo': response.json()['tempo'],
                'valence': response.json()['valence']
            }
            return song_features
        return None

