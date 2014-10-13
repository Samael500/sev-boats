# -*- coding: utf-8 -*-

from settings import TWITTER_OAUTH_INFO
from twython import Twython, TwythonError

import datetime
import time


class Twitter(object):

    """ Class for twitter use """

    query_string = '#севастополь -украина OR северная OR катер OR SevastopolBoats OR sevboats :) since:%s lang:ru'
    timelimit = 90

    def __init__(self, auth=TWITTER_OAUTH_INFO):
        self.twitter = Twython(**auth)

    def post_tweet(self, message):
        """ Writes message into twitter stream """
        try:
            return self.twitter.update_status(status=message, trim_user=True)
        except TwythonError:
            return None

    def delete_tweet(self, tweet_id):
        """ Remove tweet from timeline """
        return self.twitter.destroy_status(id=tweet_id, trim_user=True)

    def post_debug(self, message):
        """ Writes message into console to test """
        print message
        return dict(id=0, id_str='0', text=message)

    def search(self, query=None, count=10):
        """ Search tweet with sevboats ref """
        if query is None:
            since = (datetime.datetime.now() - datetime.timedelta(days=7)).date().strftime('%Y-%m-%d')
            query = self.query_string % since if 'since:%s' in self.query_string else self.query_string
        return self.twitter.search(q=query, count=count)

    def follow(self, user_id):
        """ Follow user by id """
        try:
            return self.twitter.create_friendship(user_id=user_id, follow=True)
        except TwythonError:
            return dict(status='error', id_str=None)

    def unfollow(self, user_id):
        """ Un Follow user by id """
        try:
            return self.twitter.destroy_friendship(user_id=user_id)
        except TwythonError:
            return dict(status='error', id_str=None)

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
        users_ids = []
        for tweet in search_list['statuses']:
            users_ids.append(tweet['user']['id_str'])
        return users_ids

    def my_followers(self):
        """ Get list of my followers """
        followers_ids = []
        next_cursor = -1
        while True:
            cursor = next_cursor
            fids = self.twitter.get_followers_ids(cursor=cursor, stringify_ids=True, count=1000)
            followers_ids += fids['ids']
            next_cursor = fids['next_cursor_str']
            if next_cursor == '0':
                break
            time.sleep(self.timelimit)
        return followers_ids

    def follow_search(self):
        """ Follow for all user in search results """
        users_ids = self.search_to_list()
        self.follow_list(users_ids)
        return users_ids

    def follow_followers(self):
        """ Follow for all followers """
        users_ids = self.my_followers()
        self.follow_list(users_ids)
        return users_ids
