# -*- coding: utf-8 -*-

import unittest
from sevboats.src.twitter import Twitter


class TestTwitter(unittest.TestCase):

    """ Test twitter class """

    def setUp(self):
        self.twitter = Twitter()

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
