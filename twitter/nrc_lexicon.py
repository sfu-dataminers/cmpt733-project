import pandas as pd
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer

import re
import pandas as pd
from bs4 import BeautifulSoup
import string

import nltk
from nltk.stem import WordNetLemmatizer

from wordcloud import STOPWORDS


stopwords_lstm = pd.read_csv('./LSTM/LSTM_details/stopwords_lstm.csv')

def preprocess(text):
    
    stopwords = set(STOPWORDS)
    
    # Appending new airline related stop-words
    stopwords.update([str(i).lower() for i in stopwords_lstm.name]) 
    
    # Filter for mentions
    mentions_filter = re.compile(r'(?<=\@)(\w+)')
    
    # Filter for hash-tags
    hashtags_filter = re.compile(r'(?<=\#)(\w+)')
    
    # Filter for flights numbers
    flight_numbers = re.compile(r'(flt\d*)')
    
    # Finding all mentions
    all_mentions = mentions_filter.findall(text.lower())
    
    # Finding all hash-tags
    all_hashtag = hashtags_filter.findall(text.lower())
    
    # Finding all hash-tags
    all_flights = flight_numbers.findall(text.lower())

    word_lemmatize = WordNetLemmatizer()

    # Stemming 
    def lemm_tokens(tokens, word_lemmatize):
        lemmatized = []
        for item in tokens:
            lemmatized.append(word_lemmatize.lemmatize(item,'v'))
        return lemmatized
    
    # De-emojify tweets to text
    def deEmojify(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')
    
    text = deEmojify(text)
    soup = BeautifulSoup(text)
    text = soup.get_text()
    
    # Removing punctuation
    punc_text = [x.lower() for x in text if x not in string.punctuation]
    text = "".join(punc_text)
    
    # Tokenize words
    word_tokens = nltk.word_tokenize(text)
    
    # Keeping the words with length between 4 and 15
    filtered_tokens = [x for x in word_tokens if len(x)>2 and len(x)<15]
    
    # Filter tokens
    tokens = lemm_tokens(filtered_tokens, word_lemmatize)
    all_tokens = [i for i in tokens if (i not in stopwords) and (i not in all_mentions) 
                  and (i not in all_hashtag) and (i not in all_flights) and (not i.isdigit())]
    
    return all_tokens


def fetch_granular_sentiments(text):

    emotions_dict = {'anger': [], 'anticipation': [], 'disgust': [], 'fear': [], 'joy': [], 'negative': [],
                  'positive': [], 'sadness': [], 'surprise': [], 'trust': []}

    emotions = pd.read_csv('./data/emotions.csv')
    
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
    sentiment_frequencies = fetch_granular_sentiments(' '.join(tweet))
    # Filtering granular sentiment based on polarity
    granular_sentiment = {k: v for k, v in sentiment_frequencies.items() \
        if k != 'positive' and k != 'negative' and k != 'surprise'}
    max_polarity = max(granular_sentiment.values())
    if max_polarity == 0.0:
        return []
    else:
        granular_emotion = [k for k, v in granular_sentiment.items() if v == max_polarity]
        return granular_emotion[0]
