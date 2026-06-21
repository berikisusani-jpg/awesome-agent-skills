class EmotionsEngine:
    def __init__(self):
        self.current_emotion = "neutral"

    def detect_emotion(self, text):
        """
        Improved emotion detection that handles simple negation.
        """
        text = text.lower()

        # Simple negation handling
        is_negated = any(word in text for word in ["not", "never", "no ", "don't", "wasn't"])

        keywords = {
            "happy": ["great", "good", "happy", "awesome", "perfect", "pleased"],
            "sad": ["sad", "bad", "unhappy", "sorry", "terrible", "disappointed"],
            "angry": ["angry", "mad", "annoyed", "frustrated", "hate"]
        }

        found_emotion = "neutral"
        for emotion, words in keywords.items():
            if any(word in text for word in words):
                found_emotion = emotion
                break

        if is_negated:
            if found_emotion == "happy": return "sad"
            if found_emotion == "sad": return "happy"

        self.current_emotion = found_emotion
        return found_emotion
