# -*- coding: utf-8 -*-

import unittest
from sevboats.src.twitter import Twitter
from settings import DEBUG


class TestTwitter(unittest.TestCase):

    """ Test twitter class """

    @unittest.skipIf(DEBUG or True, "Don't test when debug")
    def setUp(self):
        self.twitter = Twitter()
        # set query string
        self.twitter.query_string = '"#test"'
        # no timelimit
        self.twitter.timelimit = 0

    def test_twitter_post_delete(self):
        """ Test twitter post and delete message """
        # post tweet with text unittest
        tweet = self.twitter.post_tweet('unittest')
        self.assertEquals(tweet['text'], 'unittest')
        # remove it from timeline
        delete = self.twitter.delete_tweet(tweet['id_str'])
        self.assertEquals(tweet['id_str'], delete['id_str'])
        self.assertEquals(tweet['text'], delete['text'])

    def test_twitter_post_debug(self):
        """ Test twitter post message to console """
        # post tweet with text unittest
        tweet = self.twitter.post_debug('unittest')
        self.assertEquals(tweet['text'], 'unittest')
        self.assertEquals(tweet['id'], 0)
        self.assertEquals(tweet['id_str'], '0')

    def test_twitter_follow(self):
        """ Follow to user and unfollow now """
        user_id = '123456789'
        # follow user with id 123456789
        follows = self.twitter.follow(user_id)
        self.assertEquals(follows['id_str'], user_id)
        # unfollow this user
        unfollows = self.twitter.unfollow(user_id)
        self.assertEquals(unfollows['id_str'], user_id)
        self.assertEquals(follows['id_str'], unfollows['id_str'])
        # test follow/unfollow error
        follows = self.twitter.follow(0)
        self.assertEquals(follows['status'], 'error')
        unfollows = self.twitter.unfollow(0)
        self.assertEquals(unfollows['status'], 'error')

    def test_twitter_follow_list(self):
        """ Follow to users list and unfollow now """
        users_ids = ('123456789', )
        # follow users
        follows = self.twitter.follow_list(users_ids)
        for user_id in follows:
            self.assertIn(user_id, users_ids)
        # unfollow this users
        unfollows = self.twitter.unfollow_list(users_ids)
        for user_id in unfollows:
            self.assertIn(user_id, users_ids)
        self.assertEquals(len(follows), len(unfollows))

    def test_twitter_search(self):
        """ Test search tweets """
        search_list = self.twitter.search()
        for tweet in search_list['statuses']:
            self.assertIn(u'test', tweet['text'].lower())

    def test_twitter_search_to_list(self):
        """ Test search tweets """
        search_list = self.twitter.search()
        users_ids = self.twitter.search_to_list()
        for tweet in search_list['statuses']:
            self.assertIn(tweet['user']['id_str'], users_ids)

    def test_twitter_follow_search(self):
        """ Follow to users in search and unfollow now """
        # follow users
        users_ids = self.twitter.follow_search()
        # unfollow this users
        unfollows = self.twitter.unfollow_list(users_ids)
        for user_id in unfollows:
            self.assertIn(user_id, users_ids)
        self.assertEquals(len(users_ids), len(unfollows))

    def test_twitter_follow_followers(self):
        """ Follow to followers and unfollow now """
        # follow users
        users_ids = self.twitter.follow_followers()
        # unfollow this users
        unfollows = self.twitter.unfollow_list(users_ids)
        for user_id in unfollows:
            self.assertIn(user_id, users_ids)
        self.assertEquals(len(users_ids), len(unfollows))
