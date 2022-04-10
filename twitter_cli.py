from urllib import response
from rich.progress import track
from pyfiglet import Figlet
import random

from rich.console import Console
from rich.table import Table
import pandas as pd
import numpy as np

from twitter.responses import fetch_response
from LSTM.lstm_test import predict_sentiment
from LDA.lda_test import get_topic
from twitter.nrc_lexicon import fetch_nrc, preprocess

def check_response(tweet):
    
    tweet_sentiment = predict_sentiment(tweet)
    preprocess_tweet = preprocess(tweet)
    tweet_emotion = fetch_nrc(preprocess_tweet)
    tweet_topic = get_topic(tweet)
    
    tweet_response = fetch_response(tweet, tweet_sentiment, tweet_topic, tweet_emotion)
    return tweet_response

def example_tweets():
    tweets = pd.read_csv('./data/example_tweets.csv')
    table = Table(title="Example Tweets")
    colour = [ "red", "blue", "green", "yellow", "purple", "white"]

    for column in tweets.columns:
        rand_colours = random.choice(colour)
        table.add_column(column, justify="left", style = rand_colours)

    for ind in tweets.index:
        table.add_row(tweets['Text'][ind], tweets['Response'][ind])

    console = Console()
    console.print(table)

def main():
    response = True
    while response:
        f = Figlet(font='slant')
        print(f.renderText('Twitter Response Tool'))
        print("------------------------------------------")
        print("""
        1. Example Tweets and Responses
        2. Check Tweet Response
        3. Quit
        """)
        print ("------------------------------------------")
        response = input("Please enter your input for menu operation:")
        if response == "1":
            example_tweets()
            enter = input("Press Enter to continue ...")  
            main()
        elif response == "2":
            tweet = input("Please enter a tweet related to airline issue:")
            print(check_response(tweet))
        elif response == "3":
            print("\n Hope it helped you get a proper response!!") 
            response = None
        else:
            print("\n You have not entered a valid menu option")

if __name__ == '__main__':
    main()