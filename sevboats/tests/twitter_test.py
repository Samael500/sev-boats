# -*- coding: utf-8 -*-

import unittest
from sevboats.src.twitter import Twitter


class TestTwitter(unittest.TestCase):

    """ Test twitter class """

    def setUp(self):
        self.twitter = Twitter({})


    def test_twitter_post(self):
        """ Test twitter post message """
        res = self.twitter.post_tweet('test')
        print (res)