import os
import logging
# INSTALLATION: pip install textblob nltk
from textblob import TextBlob

# ==========================================
# 🧠 AI ENGINE CONFIGURATION
# ==========================================
# Settings for the Sentiment Analysis Model
# ==========================================
MIN_CONFIDENCE = float(os.getenv("AI_MIN_CONFIDENCE", "0.75"))
ENABLE_LOGGING = os.getenv("AI_LOGGING", "True").lower() == "true"
DEFAULT_LANGUAGE = os.getenv("AI_LANGUAGE", "en")

class SentimentAnalyzer:
    """
    Analyzes customer feedback using Natural Language Processing (NLP).
    """
    
    def __init__(self):
        if ENABLE_LOGGING:
            logging.basicConfig(level=logging.INFO)
            print(f"AI Engine initialized. Language: {DEFAULT_LANGUAGE}")

    def analyze(self, text: str) -> dict:
        """
        Returns sentiment polarity (-1.0 to 1.0) and subjectivity.
        
        Args:
            text (str): The input string to analyze.
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        status = "NEUTRAL"
        if polarity > 0.1:
            status = "POSITIVE"
        elif polarity < -0.1:
            status = "NEGATIVE"
            
        return {
            "status": status,
            "score": round(polarity, 2),
            "is_confident": abs(polarity) >= MIN_CONFIDENCE
        }

if __name__ == "__main__":
    # Test run
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("I love using this Documentation Agent!")
    print(f"Analysis Result: {result}")
