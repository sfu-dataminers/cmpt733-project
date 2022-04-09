import pandas as pd
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from pre_processing import preprocess

def fetch_grandular_sentiments(text):

    emotions_dict = {'anger': [], 'anticipation': [], 'disgust': [], 'fear': [], 'joy': [], 'negative': [],
                  'positive': [], 'sadness': [], 'surprise': [], 'trust': []}

    emotions = pd.read_csv('emotions.csv')
    
    emotions_words = emotions.pivot(index='word', columns='emotion', values='association').reset_index()
    
    emotions_words = emotions_words.drop(emotions_words.index[0])

    emotions = emotions_words.drop(['word'],axis=1)

    rows_list = []
    
    for word in word_tokenize(text):
        word = SnowballStemmer("english").stem(word.lower())
        emotions_score = (emotions_words[emotions_words.word == word])
        rows_list.append(emotions_score)

    df = pd.concat(rows_list)
    df.reset_index(drop=True)

    for emotion in list(emotions):
        emotions_dict[emotion] = df[emotion].sum() / len(word_tokenize(text))

    return emotions_dict
    
def fetch_nrc(tweet):
    
    # Preprocessing the raw twitter data
    processed_tweet = preprocess(tweet)

    # Fetching NRC Sentiment and frequencies
    sentiment_frequencies = fetch_grandular_sentiments(' '.join(tweet))
    
    # Filtering granular sentiment based on polarity
    granular_sentiment = {k: v for k, v in sentiment_frequencies.items() \
        if k != 'positive' and k != 'negative' and k != 'surprise'}
    max_polarity = max(granular_sentiment.values())
    granular_emotion = [k for k, v in granular_sentiment.items() if v == max_polarity]
    return granular_emotion[0]
