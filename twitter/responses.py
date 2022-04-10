import pandas as pd
from numpy import nan

def check_neutral(tweet):
    if tweet.contains('assist | assistance | help'):
        return True

def fetch_response(tweet, tweet_sentiment, classified_topic, nrc_sentiment):
    responses_df = pd.read_csv('../cmpt733-project/data/responses.csv')

    if tweet_sentiment == 'Positive':
        if responses_df.query('@tweet_sentiment == Sentiment and @nrc_sentiment == NRC_sentiment').empty:
            return 'Thank you for your support, we are glad you enjoyed your journey, we wish to serve you even better the next time you fly with us.'

        else:
            return responses_df[(responses_df.Sentiment == tweet_sentiment) & \
                (responses_df.NRC_sentiment == nrc_sentiment)].values[0][3]
    
    elif tweet_sentiment == 'Negative':
        if responses_df.query('@tweet_sentiment == Sentiment and @classified_topic == LDA_topic and @nrc_sentiment == NRC_sentiment').empty:
            return 'We are sorry for your concerns. Our officials will contact you shortly.'

        else:
            return responses_df[(responses_df.Sentiment == tweet_sentiment) & \
                (responses_df.NRC_sentiment == nrc_sentiment) &\
                    (responses_df.LDA_topic == classified_topic)].values[0][3]

    else:
        if any([words in tweet for words in ['help', 'assist', 'assistance']]):
            return "Thank you for your response. Our officials will contact you shortly."
        else:
            return "Thank you for expressing your views to DataMiners. Appreciate your time!"