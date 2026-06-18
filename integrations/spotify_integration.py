class SpotifyIntegration:
    def play_music(self, track_name=None):
        if track_name:
            return f"Playing {track_name} on Spotify."
        return "Resuming your favorite playlist."

    def pause_music(self):
        return "Spotify paused."
