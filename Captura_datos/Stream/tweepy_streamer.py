# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:43:17 2020

Code source:
    - Author: Vincent Russo
    - YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
    - Github repository: https://github.com/vprusso/youtube_tutorials/tree/master/twitter_python/part_1_streaming_tweets

Modified by: Marta Martin Llambes
"""

# Import necessary libraries. 
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Import file with personal API credentials.
import twitter_credentials_stream
 
# # # # TWITTER AUTHENTICATOR # # # #
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials_stream.CONSUMER_KEY, twitter_credentials_stream.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials_stream.ACCESS_TOKEN, twitter_credentials_stream.ACCESS_TOKEN_SECRET)
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API.
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filters Twitter Streams to capture data by the keywords. 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout, and to the specified file.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

 
if __name__ == '__main__':
 
    # Define the list of hashtags you are interested in.
    hash_tag_list = ["#8M", "#8M2020", "#8deMarzo", "#8marzo2020", "#DiaInternacionalDeLaMujer", "#DiaDeLaMujer", "#8Marzo"]
	# Define the file name where the tweets will be printed.
    fetched_tweets_filename ='tweets'+'_'+time.strftime('%Y%m%d-%H%M%S')+'.json'
	# Authenticate, and start collecting tweets in real time.
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)