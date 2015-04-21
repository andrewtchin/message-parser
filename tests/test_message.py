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

    def test_parse_mention(self):
        self.message = Message(TestMessage.MENTION)
        result = self.message.parse()
        mention_dict = {'mentions': [TestMessage.MENTION_RESULT]}
        self.assertEqual(result, mention_dict)

    def test_parse_emoticon(self):
        min_emoticon = '(a)'
        self.message = Message(min_emoticon)
        result = self.message.parse()
        emoticon_dict = {'emoticons': ['a']}
        self.assertEqual(result, emoticon_dict)

        max_emoticon = '(aaaaaaaaaaaaaaa)'
        self.message = Message(max_emoticon)
        result = self.message.parse()
        emoticon_dict = {'emoticons': ['aaaaaaaaaaaaaaa']}
        self.assertEqual(result, emoticon_dict)

        embedded_emoticon = 'bbb(a)bbb(x)bbb(a)bbb'
        self.message = Message(embedded_emoticon)
        result = self.message.parse()
        emoticon_dict = {'emoticons': ['a', 'x']}
        self.assertEqual(result, emoticon_dict)

    def test_parse_not_emoticon(self):
        no_emoticon = '()'
        self.message = Message(no_emoticon)
        result = self.message.parse()
        self.assertEqual(result, {})

        long_emoticon = '(aaaaaaaaaaaaaaaa)'
        self.message = Message(long_emoticon)
        result = self.message.parse()
        self.assertEqual(result, {})

    def test_parse_link(self):
        self.message = Message(TestMessage.LINK)
        result = self.message.parse()
        link_dict = {'links': [{'title': TestMessage.LINK_TITLE,
                                'url': TestMessage.LINK}]}
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
