# -*- coding: utf-8 -*-

from settings import TWITTER_OAUTH_INFO
from twython import Twython
from datetime import datetime
from datetime import timedelta

class Twitter:

    """ Class for twitter use """

    query_string = '#севастополь -украина OR катер OR SevastopolBoats OR sevboats :) since:%s lang:ru'

    def __init__(self, auth=TWITTER_OAUTH_INFO):
        self.twitter = Twython(**auth)

    def post_tweet(self, message):
        """ Writes message into twitter stream """
        return self.twitter.update_status(status=message, trim_user=True)

    def delete_tweet(self, tweet_id):
        """ Remove tweet from timeline """
        return self.twitter.destroy_status(id=tweet_id, trim_user=True)

    def post_debug(self, message):
        """ Writes message into console to test """
        print message
        return dict(id=0, id_str='0', text=message)

    def search(self, query=None, count=50):
        """ Search tweet with sevboats ref """
        if query is None:
            since = (datetime.now() - timedelta(days=7)).date().strftime('%Y-%m-%d')
            query = self.query_string % since
        return self.twitter.search(q=query, count=count)

    def follow(self, user_id):
        """ Follow user by id """
        return self.twitter.create_friendship(user_id=user_id, follow=True)

    def unfollow(self, user_id):
        """ Un Follow user by id """
        return self.twitter.destroy_friendship(user_id=user_id)

    def follow_list(self, friends_ids):
        """ Follow user in search result """
        friends = []
        for user_id in friends_ids:
            friends.append(self.follow(user_id)['id_str'])
        return friends

    def unfollow_list(self, friends_ids):
        """ Un Follow user in ids list """
        friends = []
        for user_id in friends_ids:
            friends.append(self.unfollow(user_id)['id_str'])
        return friends

    def search_to_list(self, search_list=None):
        """ Follow user in search result """
        if search_list is None:
            search_list = self.search()
        friends_ids = []
        for tweet in search_list['statuses']:
            friends_ids.append(tweet['user']['id_str'])
        return friends_ids
