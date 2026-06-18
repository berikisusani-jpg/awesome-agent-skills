import pvporcupine
import pyaudio
import struct
from config.settings import PICOVOICE_ACCESS_KEY

class WakeWordDetector:
    def __init__(self):
        self.porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keywords=['friday']
        )
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def listen(self):
        print("Listening for wake word...")
        try:
            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                result = self.porcupine.process(pcm)
                if result >= 0:
                    print("Wake word detected!")
                    return True
        except KeyboardInterrupt:
            return False

    def close(self):
        self.audio_stream.close()
        self.pa.terminate()
        self.porcupine.delete()
