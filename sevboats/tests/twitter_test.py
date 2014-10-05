# -*- coding: utf-8 -*-

import unittest
from sevboats.src.twitter import Twitter


class TestTwitter(unittest.TestCase):

    """ Test twitter class """

    def setUp(self):
        self.twitter = Twitter()

    def test_twitter_post_delete(self):
        """ Test twitter post and delete message """
        # post tweet with tet unittest
        tweet = self.twitter.post_tweet('unittest')
        self.assertEquals(tweet['text'], 'unittest')
        # remove it from timeline
        delete = self.twitter.delete_tweet(tweet['id_str'])
        self.assertEquals(tweet['id_str'], delete['id_str'])
        self.assertEquals(tweet['text'], delete['text'])
