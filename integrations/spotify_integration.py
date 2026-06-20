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
            # FIXED: Real call logic
            if track_name:
                results = self.sp.search(q=track_name, type='track', limit=1)
                if results['tracks']['items']:
                    track_uri = results['tracks']['items'][0]['uri']
                    self.sp.start_playback(uris=[track_uri])
                    return f"Spotify: Playing {track_name}"
                return {"status": "error", "message": f"Track {track_name} not found."}
            else:
                self.sp.start_playback()
                return "Spotify: Resuming playback."
        except Exception as e:
            logging.error(f"Spotify play failed: {e}")
            return {"status": "error", "message": str(e)}

    def pause_music(self):
        if not self.sp:
            return {"status": "not_implemented", "message": "Spotify credentials not configured."}
        try:
            # FIXED: Real call logic
            self.sp.pause_playback()
            return "Spotify paused."
        except Exception as e:
            logging.error(f"Spotify pause failed: {e}")
            return {"status": "error", "message": str(e)}
