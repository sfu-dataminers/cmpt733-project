import tweepy as tw
import pandas as pd
import config_file as conf


def get_secret_key(conf):
    acess_token = conf.consumer_key 
    access_token_secret = conf.consumer_secret
    bearer_token = conf.bearer_token
    return acess_token,access_token_secret,bearer_token

# Function to fectch twitter data 
def extract_twitter_data(mentions, date, count_tweets):
    
    cols = [ 'tweet_id', 'username', 'description', 'location', 'following',
        'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags']
    
    df = pd.DataFrame(cols)

    tweets = tw.Cursor(api.search_tweets, mentions, lang='en',
                     since_id=date, tweet_mode='extended').items(count_tweets)

    list_tweets = [tweet for tweet in tweets]

    row = 1

    for tw in list_tweets:

        hashtags = tw.entities['hashtags']

        try:
            text = tw.retweeted_status.full_text
        except AttributeError:
            text = tw.full_text
        hashtext = list()

        for hash in range(0, len(hashtags)):
            hashtext.append(hashtags[hash]['text'])

        tweet_row = [ tw.user.id_str, tw.user.screen_name, tw.user.description,
            tw.user.location, tw.user.friends_count, tw.user.followers_count,
            tw.user.statuses_count, tw.retweet_count, hashtext]

        df.loc[len(df)] = tweet_row
        row = row + 1

    filename = 'scraped_tweets_' + mentions + '.csv'
    df.to_csv('/data'+filename)


if __name__ == '__main__':
    
    auth = tw.OAuth2BearerHandler(conf.bearer_token)

    api = tw.API(auth, wait_on_rate_limit=True)

    # Enter mentions like - "United_Airlines"
    mentions = input()

    # Enter the initial date like - 2022-03-01
    date = input()

    # Enter tweets to be fetched like - 10000
    count_tweets = input()

    print('Data Extraction has been completed!!')
    extract_twitter_data(mentions, date, count_tweets)
    print('Data Extraction has been completed!!')
