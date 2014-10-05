# -*- coding: utf-8 -*-

from settings import MESSAGES_DIR
import os
import yaml
import random


class Messenger(object):

    """ Base Messenger class to get message from file """

    filename = ''
    filename_suffix = '.yaml'

    @property
    def get_messages_path(self):
        """ Return file path to self message file """
        return os.path.join(MESSAGES_DIR, self.filename + self.filename_suffix)

    def get_messages(self):
        """ Return messages as array if available file path, else - None """
        try:
            with open(self.get_messages_path, 'r') as messages_file:
                messages = yaml.load(messages_file)
            return messages
        except IOError:
            return None

    def get_message(self):
        """ Get random message from messages array """
        messages = self.get_messages()
        if messages:
            return random.choice(messages)
        return None


class MiddayGun(Messenger):

    """ Midday gun messanger """

    filename = 'midday_gun'
