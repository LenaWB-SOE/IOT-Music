import requests
from datetime import datetime, timedelta
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
        response1 = requests.get(f"{API_BASE_URL}me/player/currently-playing", headers=self.get_headers())
        #response2 = requests.get(f"{API_BASE_URL}me/player", headers=self.get_headers())
        #print(response2.json)
        #print(response2.json()["progress_ms"])
        if response1.status_code == 200:
            return response1.json()["item"]["name"], response1.json()["item"]["id"], response1.json()["item"]["duration_ms"]
        # if response2.status_code == 200:
        #     return response2.json()["item"]["TrackObject"]["name"], response2.json()["item"]["TrackObject"]["id"], response2.json()["item"]["TrackObject"]["duration_ms"]
        return None
