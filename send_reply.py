from urllib import response
import tweepy as tw
import pandas as pd

def check_mentions(api,username,comment, tweetId):
    res = api.update_status( status = "@" + username +","+comment,tin_reply_to_status_id = tweetId) 
    return res

def get_api():
    acess_token = 'sGQh43rlmz1ps1r3uOhz4B7IV'
    access_token_secret = \
        'SHRgfYX7aQFxRF1jN1k5MCHocl0q4bUVMXj1aKz71QoxHK5P5O'
    bearer_token = \
        'AAAAAAAAAAAAAAAAAAAAAA8iZQEAAAAA6ONMqX0g7cvq2nGJDbNr%2Fi%2 \
    B8WvM%3DfW1ISUwg4ypLsSNxjjGuTa59w47ky24ia0m4fIIJM5O9KXzYzx'

    auth = tw.OAuth2BearerHandler(bearer_token)
    api = tw.API(auth, wait_on_rate_limit=True)
    return api

if __name__ == '__main__':
    
    api = get_api()
    print(api)
    username = "DataMinersSfu"
    tweet_id = "1497744836635467780"
    comment = "Test reply for Big-Data Project"
    check_mentions(api,username,comment,tweet_id)