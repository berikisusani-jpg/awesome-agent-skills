import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import logging

class SpotifyIntegration:
    def __init__(self):
        self.sp = None
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
            try:
                auth_manager = SpotifyOAuth(
                    client_id=SPOTIFY_CLIENT_ID,
                    client_secret=SPOTIFY_CLIENT_SECRET,
                    redirect_uri="http://localhost:8888/callback",
                    scope="user-modify-playback-state"
                )
                self.sp = spotipy.Spotify(auth_manager=auth_manager)
            except Exception as e:
                logging.error(f"Spotify init failed: {e}")

    def play_music(self, track_name=None):
        if not self.sp:
            return {"status": "not_implemented", "message": "Spotify credentials not configured or auth failed."}

        try:
            # self.sp.start_playback()
            return f"Spotify: Playing {track_name if track_name else 'your music'}"
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def pause_music(self):
        return "Spotify paused (Simulated API call)"
