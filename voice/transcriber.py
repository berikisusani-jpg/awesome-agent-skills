import whisper

class FridayTranscriber:
    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe(self, audio_path):
        # We add an initial prompt to help Whisper with localization like Nigerian Pidgin
        result = self.model.transcribe(audio_path, initial_prompt="Nigerian Pidgin, how far, oya, abeg")
        return result['text']
