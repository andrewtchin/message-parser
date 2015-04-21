import string
import unittest

import rstr

from message import Message


class TestMessage(unittest.TestCase):

    MENTION = '@test_mention'
    MENTION_RESULT = 'test_mention'
    EMOTICON = '(test_emoticon)'
    EMOTICON_RESULT = 'test_emoticon'
    LINK = 'http://example.com'
    LINK_TITLE = 'Example Domain'

    def setUp(self):
        self.message = Message()

    def test_message_len(self):
        message_len = Message.MAX_MESSAGE_LEN + 1
        self.message = Message(rstr.rstr(string.ascii_letters,
                                         message_len))
        self.assertEqual(len(self.message.message), Message.MAX_MESSAGE_LEN)

        message_len = Message.MAX_MESSAGE_LEN
        self.message = Message(rstr.rstr(string.ascii_letters,
                                         message_len))
        self.assertEqual(len(self.message.message), Message.MAX_MESSAGE_LEN)

        message_len = Message.MAX_MESSAGE_LEN - 1
        self.message = Message(rstr.rstr(string.ascii_letters,
                                         message_len))
        self.assertEqual(len(self.message.message), message_len)

    def test_check_token_mention(self):
        result = self.message.check_token(TestMessage.MENTION).groupdict()
        mention_dict = {'mentions': TestMessage.MENTION_RESULT,
                        'emoticons': None,
                        'links': None}
        self.assertEqual(result, mention_dict)

    def test_check_token_emoticon(self):
        min_emoticon = '(a)'
        result = self.message.check_token(min_emoticon).groupdict()
        emoticon_dict = {'mentions': None,
                         'emoticons': 'a',
                         'links': None}
        self.assertEqual(result, emoticon_dict)

        max_emoticon = '(aaaaaaaaaaaaaaa)'
        result = self.message.check_token(max_emoticon).groupdict()
        emoticon_dict = {'mentions': None,
                         'emoticons': 'aaaaaaaaaaaaaaa',
                         'links': None}
        self.assertEqual(result, emoticon_dict)

        embedded_emoticon = 'bbb(a)bbb'
        result = self.message.check_token(embedded_emoticon).groupdict()
        emoticon_dict = {'mentions': None,
                         'emoticons': 'a',
                         'links': None}
        self.assertEqual(result, emoticon_dict)

    def test_check_not_emoticon(self):
        no_emoticon = '()'
        result = self.message.check_token(no_emoticon)
        self.assertEqual(result, None)

        long_emoticon = '(aaaaaaaaaaaaaaaa)'
        result = self.message.check_token(long_emoticon)
        self.assertEqual(result, None)

    def test_check_token_link(self):
        result = self.message.check_token(TestMessage.LINK).groupdict()
        link_dict = {'mentions': None,
                     'emoticons': None,
                     'links': TestMessage.LINK}
        self.assertEqual(result, link_dict)

    def test_parse(self):
        self.message.message = ' '.join([TestMessage.MENTION,
                                         TestMessage.EMOTICON,
                                         TestMessage.LINK])
        result = self.message.parse()
        message_dict = {'mentions': [TestMessage.MENTION_RESULT],
                        'emoticons': [TestMessage.EMOTICON_RESULT],
                        'links': [{'title': TestMessage.LINK_TITLE,
                                   'url': TestMessage.LINK}]}
        self.assertEqual(result, message_dict)

    def test_add_attribute(self):
        data = {}
        self.message.add_attribute(data, 'key', 'value1')
        data_dict1 = {'key': ['value1']}
        self.assertEqual(data, data_dict1)

        self.message.add_attribute(data, 'key', 'value2')
        data_dict2 = {'key': ['value1', 'value2']}
        self.assertEqual(data, data_dict2)

    def test_get_link(self):
        result = self.message.get_link(TestMessage.LINK)
        link_dict = {'url': TestMessage.LINK,
                     'title': TestMessage.LINK_TITLE}
        self.assertEqual(result, link_dict)

    def test_get_title(self):
        title = self.message.get_title(TestMessage.LINK)
        self.assertEqual(title, TestMessage.LINK_TITLE)

    def test_get_title_unavailable(self):
        title = self.message.get_title('http://example')
        self.assertEqual(title, None)
