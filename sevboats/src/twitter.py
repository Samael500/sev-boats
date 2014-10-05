from twython import Twython
from settings import TWITTER_OAUTH_INFO


class Twitter:

    """ Class for twitter use """

    def __init__(self, auth=TWITTER_OAUTH_INFO):
        self.twitter = Twython(**auth)

    def post_tweet(self, message):
        """ Writes message into twitter stream """
        return self.twitter.update_status(status=message, trim_user=True)

    def delete_tweet(self, tweet_id):
        """ Remove tweet from timeline """
        return self.twitter.destroy_status(id=tweet_id, trim_user=True)

    def post(self, message):
        """ Writes message into console to test """
        print message
        return message
