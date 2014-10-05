# -*- coding: utf-8 -*-

from sevboats.settings import MESSAGES_DIR
import os
import yaml


class Message(object):

    filename = ''
    filename_suffix = '.yaml'

    @property
    def get_messages_path(self):
        return os.path.join(MESSAGES_DIR, self.filename + self.filename_suffix)

    def get_messages(self):
        try:
            with open(self.get_messages_path, 'r') as messages_file:
                messages = yaml.load(messages_file)
            return messages
        except IOError:
            return None
