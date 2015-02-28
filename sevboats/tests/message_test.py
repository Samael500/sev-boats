# -*- coding: utf-8 -*-

import unittest
from sevboats.src.messages import Messenger, MiddayGun, ShipMessenger


class TestMessenger(unittest.TestCase):

    """ Test base messenger class """

    def setUp(self):
        self.messager = Messenger()

    def test_message_class(self):
        """ Check file name and ext default """
        self.assertEqual(self.messager.filename, '')
        self.assertEqual(self.messager.filename_suffix, '.yaml')

    def test_get_messages_none(self):
        """ Check get None if no file name """
        self.messager.filename = 'no_file'
        self.assertTrue(self.messager.get_messages() is None)

    def test_get_messages_path(self):
        """ Check file path for messages file """
        self.assertIn('/sev-boats/sevboats/messages/.yaml', self.messager.get_messages_path)

    def test_get_messages_ok(self):
        """ Check get correct messages if file exist """
        messages = self.messager.get_messages()
        for i in range(len(messages)):
            self.assertEqual(u'Тестовый текст %d' % (i + 1), messages[i])
        self.assertEqual(len(messages), 5)

    def test_get_message_rand(self):
        """ Get random message OK """
        message = self.messager.get_message()
        messages = self.messager.get_messages()
        self.assertIn(message, messages)

    def test_get_message_rand_none(self):
        """ Get random message None if file no exist """
        self.messager.filename = 'no_file'
        self.assertTrue(self.messager.get_message() is None)
        self.assertTrue(self.messager.get_messages() is None)


class TestMiddayGunMessager(unittest.TestCase):

    """ Test Midday Gun messenger class """

    def setUp(self):
        self.messager = MiddayGun()

    def test_message_class(self):
        """ Check file name and ext default """
        self.assertEqual(self.messager.filename, 'midday_gun')
        self.assertEqual(self.messager.filename_suffix, '.yaml')

    def test_get_messages_none(self):
        """ Check get None if no file name """
        self.messager.filename = 'no_file'
        self.assertTrue(self.messager.get_messages() is None)

    def test_get_messages_path(self):
        """ Check file path for messages file """
        self.assertIn('/sev-boats/sevboats/messages/midday_gun.yaml', self.messager.get_messages_path)


class TestShipMessager(unittest.TestCase):

    """ Test ship messenger class """

    def setUp(self):
        self.messager = ShipMessenger()

    def test_message_class(self):
        """ Check file name and ext default """
        self.assertEqual(self.messager.filename, 'ships')
        self.assertEqual(self.messager.filename_suffix, '.yaml')

    def test_get_messages_none(self):
        """ Check get None if no file name """
        self.messager.filename = 'no_file'
        self.assertTrue(self.messager.get_message('test') is None)

    def test_get_messages_path(self):
        """ Check file path for messages file """
        self.assertIn('/sev-boats/sevboats/messages/ships.yaml', self.messager.get_messages_path)

    def test_get_messages_rand(self):
        """ Get random message OK """
        messages = self.messager.get_messages()
        message = self.messager.get_message('on')
        dict_message = dict(text=message, status='on')
        self.assertIn(dict_message, messages)
        message = self.messager.get_message('off')
        dict_message = dict(text=message, status='off')
        self.assertIn(dict_message, messages)
