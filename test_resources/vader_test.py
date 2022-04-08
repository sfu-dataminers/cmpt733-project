import pandas as pd
import glob, re, nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
nltk.download('punkt')

def clean_tweet(tweet):
    clean_tweet = re.sub("@[A-Za-z0-9_]+","", tweet)
    clean_tweet = re.sub("#[A-Za-z0-9_]+","", clean_tweet)
    return clean_tweet

def sentiment_scores(sentence):
    
    ngram_sentence = tokenize.sent_tokenize(clean_tweet(sentence))

    # Create a SentimentIntensityAnalyzer object.
    sent_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    sentiment_dict = sent_obj.polarity_scores(ngram_sentence)
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
 
    print("Sentence Overall Rated As", end = " ")
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        return 'Positive'
 
    elif sentiment_dict['compound'] <= - 0.05 :
        return "Negative"
 
    else :
        return "Neutral"

if __name__ == "__main__" :
    input_tweet = input('Please input an example tweet to check NRC lexicon:')
    print(sentiment_scores(input_tweet))
    