import pandas as pd
from numpy import nan

def fetch_response(tweet_sentiment, classified_topic, nrc_sentiment):
    responses_df = pd.read_csv('../data/responses.csv')

    if nrc_sentiment != '':
        if responses_df.query('@tweet_sentiment == Sentiment and @classified_topic == LDA_topic and @nrc_sentiment == NRC_sentiment').empty:
            return 'We are currently experiencing high volume of requests, we will reach out to you as soon as possible!'
            
        else:
            return responses_df[(responses_df.Sentiment == tweet_sentiment) & \
                (responses_df.NRC_sentiment == nrc_sentiment) &\
                    (responses_df.LDA_topic == classified_topic)].values[0][3]

    else:
        if responses_df.query('@tweet_sentiment == Sentiment and @classified_topic == LDA_topic').empty:
            return 'We are currently experiencing high volume of requests, we will reach out to you as soon as possible!'

        else:
            return responses_df[(responses_df.Sentiment == tweet_sentiment) & \
                (responses_df.LDA_topic == classified_topic)].values[0][3]
            