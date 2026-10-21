
import pandas as pd
from textblob import TextBlob


def analyze_sentiment(text):
    """Return sentiment label, polarity and subjectivity."""

    if pd.isna(text) or not str(text).strip():
        return {
            "Sentiment": "Neutral",
            "Polarity": 0.0,
            "Subjectivity": 0.0
        }

    result = TextBlob(str(text)).sentiment
    polarity = result.polarity
    subjectivity = result.subjectivity

    if polarity > 0.05:
        sentiment = "Positive"
    elif polarity < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "Sentiment": sentiment,
        "Polarity": round(polarity, 3),
        "Subjectivity": round(subjectivity, 3)
    }
