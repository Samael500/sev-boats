# -*- coding: utf-8 -*-

import unittest
from sevboats.src.messages import Message


class TestMessage(unittest.TestCase):

    def setUp(self):
        self.message = Message()

    def test_message_class(self):
        self.assertEqual(self.message.filename, '')
        self.assertEqual(self.message.filename_suffix, '.yaml')

    def test_get_messages_none(self):
        self.message.filename = 'no_file'
        self.assertTrue(self.message.get_messages() is None)

    def test_get_messages_path(self):
        self.assertIn('/sev-boats/sevboats/messages/.yaml', self.message.get_messages_path)

    def test_get_messages_ok(self):
        messages = self.message.get_messages()
        self.assertEqual(u'Тестовый текст 1', messages[0])
        self.assertEqual(u'Тестовый текст 2', messages[1])
        self.assertEqual(None, messages[2])
        self.assertEqual(u'Тестовый текст 4', messages[3])
