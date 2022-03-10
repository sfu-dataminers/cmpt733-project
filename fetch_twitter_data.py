import tweepy as tw
import pandas as pd
import config_file as conf

def extract_twitter_data(words, date_since, numtweet):
    """
        Function to scrape twitter data and convert
        to a pandas dataframe.
        Return a csv file.
    """
    db = pd.DataFrame(columns=[
        'tweet_id',
        'username',
        'description',
        'location',
        'following',
        'followers',
        'totaltweets',
        'retweetcount',
        'text',
        'hashtags',
        ])

    tweets = tw.Cursor(api.search_tweets, words, lang='en',
                           since_id=date_since, tweet_mode='extended'
                           ).items(numtweet)

    list_tweets = [tweet for tweet in tweets]

    i = 1

    for tweet in list_tweets:
        tweetid = tweet.user.id_str
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']

        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()

        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        ith_tweet = [
            tweetid,
            username,
            description,
            location,
            following,
            followers,
            totaltweets,
            retweetcount,
            text,
            hashtext,
            ]

        db.loc[len(db)] = ith_tweet
        i = i + 1
    filename = 'scraped_tweets_' + words + '.csv'
    db.to_csv('/data'+filename)


if __name__ == '__main__':
    
    acess_token = conf.consumer_key 
    access_token_secret = conf.consumer_secret
    bearer_token = conf.bearer_token
       
    auth = tw.OAuth2BearerHandler(bearer_token)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Enter Hashtag and Initial date
    print('Enter Twitter HashTag to search for')
    words = input()

    # Date since
    date_since = '2022-02-01'

    # Number of tweets to extract
    numtweet = 10000
    extract_twitter_data(words, date_since, numtweet)
    print('Data Extraction has been completed!!')
