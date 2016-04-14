from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

from settings import TWITTER_CREDENTIALS

class TwitterStreamListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status.text)

    def on_status(self, status):
        print(data)
        return True

def get_tweets():
    """
    These handle Twitter authetification and the connection to Twitter Streaming API.
    Keys taken from settings which is not publically available within this project.
    To get your owns please visit: https://apps.twitter.com
    """
    listener = TwitterStreamListener()
    auth = OAuthHandler(TWITTER_CREDENTIALS.get("consumer_key"),
                        TWITTER_CREDENTIALS.get("consumer_secret"))
    auth.set_access_token(TWITTER_CREDENTIALS.get("access_token"),
                        TWITTER_CREDENTIALS.get("access_token_secret"))
    stream = Stream(auth, listener)

    stream.filter(track=['#sarcasm'])
