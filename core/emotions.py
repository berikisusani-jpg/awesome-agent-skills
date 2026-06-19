class EmotionsEngine:
    def __init__(self):
        self.current_emotion = "neutral"

    def detect_emotion(self, text):
        # Basic keyword detection for now
        keywords = {
            "happy": ["great", "good", "happy", "awesome"],
            "sad": ["sad", "bad", "unhappy", "sorry"],
            "angry": ["angry", "mad", "annoyed"]
        }
        for emotion, words in keywords.items():
            if any(word in text.lower() for word in words):
                self.current_emotion = emotion
                return emotion
        return "neutral"
