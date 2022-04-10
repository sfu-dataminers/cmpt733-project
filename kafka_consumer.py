from kafka import KafkaConsumer
from pyspark import SparkConf, SparkContext
from pyspark.sql.functions import from_json, get_json_object, col, udf
from pyspark.sql.types import StructField, StructType, StringType
from pyspark.sql import SparkSession
import sys

from pyspark.sql import functions as F
import tweepy as tw
import config_file as cf
from time import sleep
import logging

from LSTM.lstm_test import predict_sentiment
from LDA.lda_test import get_topic
from twitter.nrc_lexicon import fetch_nrc, preprocess
from twitter.responses import fetch_response

def get_api(row):
    # Fetching tweet response based on Sentiment, Topic and NRC_Sentiment
    text = fetch_response(row.text, row.Sentiment, row.Topic, row.NRC_Sentiment)
    
    # Twitter authentication
    auth = tw.OAuthHandler(cf.consumer_key, cf.consumer_secret)
    auth.set_access_token(cf.access_token, cf.access_token_secret)

    api = tw.API(auth)
    try:
        if id is not None:
            logging.error("PREPARING TO REPLY............")
            # Tweeting the response to the user
            api.update_status(status = "@" + row.user + " " + text, 
    in_reply_to_status_id = row.id , auto_populate_reply_metadata=True)
        else:
            logging.error("ELSE CONDITION............")
    except tw.TweepError as e:
        logging.error(f"EXCEPTION {e.reason}")
    sleep(2)


def main(topic):
    logging.error("START OF MAIN!!!!!!!!!!!!!!")

    # Initializing kafka readStream
    messages = spark.readStream.format('kafka') \
        .option('kafka.bootstrap.servers', 'localhost:9092') \
        .option('subscribe', topic).load()

    values = messages.selectExpr("CAST(value AS STRING)")

    # Tweet Schema for raw data
    schema = StructType(
            [
                    StructField("id", StringType()),
                    StructField("text", StringType()),
                    StructField("user", StringType())
            ]
    )

    # Fetching required data from twitter
    raw_df = values.withColumn("value", from_json("value", schema))\
        .select(col('value.*'))

    new_df = raw_df.select(raw_df.id, raw_df.text,\
         get_json_object(raw_df.user, '$.screen_name').alias("user"))

    # Creating udf functions for predicting sentiment, fetching topic and nrc emotion
    predict_sentiment_udf = udf(predict_sentiment,StringType())
    get_topic_udf = udf(get_topic, StringType())
    preprocess_udf = udf(preprocess, StringType())
    nrc_sentiment_udf = udf(fetch_nrc, StringType())

    new_df = new_df.withColumn('Sentiment',predict_sentiment_udf(raw_df.text))
    new_df = new_df.withColumn('Topic',get_topic_udf(raw_df.text))
    tokenized_text = preprocess_udf(raw_df.text)
    new_df = new_df.withColumn('NRC_Sentiment',nrc_sentiment_udf(tokenized_text))

    # Passing kafka data to get_api function
    stream = new_df.writeStream.format('console').foreach(
        get_api
    ).start()
    logging.error("After starting stream")
    sleep(10000)
    stream.stop()

if __name__ == '__main__':
    topic = sys.argv[1]
    spark = SparkSession.builder.appName('dataminers').getOrCreate()
    # Make sure we have Spark 3.0+
    assert spark.version >= '3.0' 
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main(topic)
