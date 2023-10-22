from textblob import TextBlob
import random


def get_daily_affirmation():
    affirmations = [
        "I believe in myself and my capabilities.",
        "Challenges are opportunities for growth.",
        "I am deserving of love, peace, and happiness.",
        "By being myself, I bring happiness to others.",
        "Every day, I become stronger."
    ]
    return random.choice(affirmations)

# Function for sentiment analysis
def sentiment_analysis(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'