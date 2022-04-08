from cgitb import text
from nrclex import NRCLex
from pre_processing import preprocess

def fetch_nrc(tweet):
    # Preprocessing the raw twitter data
    processed_tweet = preprocess(tweet)

    # Fetching NRC Sentiment and frequencies
    text_object = NRCLex(' '.join(processed_tweet))
    sentiment_frequencies = text_object.affect_frequencies

    # Filtering granular sentiment based on polarity
    granular_sentiment = {k: v for k, v in sentiment_frequencies.items() \
        if k != 'positive' and k != 'negative' and k != 'surprise'}
    max_polarity = max(granular_sentiment.values())
    granular_emotion = [k for k, v in granular_sentiment.items() if v == max_polarity]
    return granular_emotion[0]
