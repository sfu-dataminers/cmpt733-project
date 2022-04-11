from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import config_file as conf 
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic_name = "dataminers"


class twitterAuth():
    """SET UP TWITTER AUTHENTICATION"""

    def authenticateTwitterApp(self):
        auth = OAuthHandler(conf.consumer_key,conf.consumer_secret)
        auth.set_access_token(conf.access_token,conf.access_token_secret)

        return auth

class TwitterStreamer():

    """SET UP STREAMER"""
    def __init__(self):
        self.twitterAuth = twitterAuth()

    def stream_tweets(self):
        while True:
            listener = ListenerTS() 
            auth = self.twitterAuth.authenticateTwitterApp()
            stream = Stream(auth, listener)
            stream.filter(track=["@himalyabachwani"], stall_warnings=True, languages= ["en"])


class ListenerTS(StreamListener):

    def on_data(self, raw_data):
            producer.send(topic_name, str.encode(raw_data))
            return True


if __name__ == "__main__":
    TS = TwitterStreamer()
    TS.stream_tweets()