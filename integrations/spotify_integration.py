import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from integrations.base import BaseIntegration
import logging
import datetime

class SpotifyIntegration(BaseIntegration):
    @property
    def name(self): return "Spotify"

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

    def available(self):
        return self.sp is not None

    async def execute(self, action, params=None):
        if not self.available():
            return {"status": "not_implemented", "message": "Spotify credentials not configured."}

        try:
            if action == "play":
                track = (params or {}).get("track_name")
                if track:
                    # Real call to search and play
                    results = self.sp.search(q=track, type='track', limit=1)
                    if results['tracks']['items']:
                        track_uri = results['tracks']['items'][0]['uri']
                        resp = self.sp.start_playback(uris=[track_uri])
                        return {
                            "status": "success",
                            "message": f"Playing {track}",
                            "receipt": {
                                "type": "api_response",
                                "data": resp,
                                "timestamp": datetime.datetime.now().isoformat()
                            }
                        }
                    return {"status": "error", "message": f"Track {track} not found."}
                else:
                    resp = self.sp.start_playback()
                    return {
                        "status": "success",
                        "message": "Spotify: Resuming playback.",
                        "receipt": {
                            "type": "api_response",
                            "data": resp,
                            "timestamp": datetime.datetime.now().isoformat()
                        }
                    }
            elif action == "pause":
                resp = self.sp.pause_playback()
                return {
                    "status": "success",
                    "message": "Spotify paused.",
                    "receipt": {
                        "type": "api_response",
                        "data": resp,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                }
        except Exception as e:
            logging.error(f"Spotify execution failed: {e}")
            return {"status": "error", "message": str(e)}

        return {"status": "not_implemented", "message": f"Action {action} not found."}
