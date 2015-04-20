import unittest

from message import Message


class TestMessage(unittest.TestCase):

    MENTION = '@test_mention'
    EMOTICON = '(test_emoticon)'
    LINK = 'http://example.com'

    def setUp(self):
        self.message = Message()

    def test_check_token_mention(self):
        result = self.message.check_token(TestMessage.MENTION).groupdict()
        mention_dict = {'mentions': TestMessage.MENTION,
                        'emoticons': None,
                        'links': None}
        self.assertEqual(result, mention_dict)

    def test_check_token_emoticon(self):
        min_emoticon = '(a)'
        result = self.message.check_token(min_emoticon).groupdict()
        emoticon_dict = {'mentions': None,
                         'emoticons': min_emoticon,
                         'links': None}
        self.assertEqual(result, emoticon_dict)

        max_emoticon = '(aaaaaaaaaaaaaaa)'
        result = self.message.check_token(max_emoticon).groupdict()
        emoticon_dict = {'mentions': None,
                         'emoticons': max_emoticon,
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
        message_dict = {
                           'mentions': ['test_mention'],
                           'emoticons': ['test_emoticon'],
                           'links': [
                               {
                                   'title': 'Example Domain',
                                   'url': 'http://example.com'
                               }
                           ]
                       }
        self.assertEqual(result, message_dict)

    def test_add_attribute(self):
        data = {}
        self.message.add_attribute(data, 'key', 'value1')
        data_dict1 = {'key': ['value1']}
        self.assertEqual(data, data_dict1)

        self.message.add_attribute(data, 'key', 'value2')
        data_dict2 = {'key': ['value1', 'value2']}
        self.assertEqual(data, data_dict2)

    def test_get_mention(self):
        result = self.message.get_mention(TestMessage.MENTION)
        self.assertEqual(result, 'test_mention')

        result = self.message.get_mention(''.join([TestMessage.MENTION, '!']))
        self.assertEqual(result, 'test_mention')

    def test_get_emoticon(self):
        result = self.message.get_emoticon(TestMessage.EMOTICON)
        self.assertEqual(result, 'test_emoticon')

    def test_get_link(self):
        result = self.message.get_link(TestMessage.LINK)
        link_dict = {'url': TestMessage.LINK,
                     'title': 'Example Domain'}
        self.assertEqual(result, link_dict)

    def test_get_title(self):
        title = self.message.get_title(TestMessage.LINK)
        self.assertEqual(title, 'Example Domain')

    def test_get_title_unavailable(self):
        title = self.message.get_title('http://example')
        self.assertEqual(title, None)
