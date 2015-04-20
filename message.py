"""This module extracts information from a message string.

TODO
"""

import json
import re
import urllib2

from bs4 import BeautifulSoup


class Message(object):
    """This class parses a message and stores selected message attributes.

    Attributes:
        message (str): Contents of the message.
    """

    def __init__(self, message=''):
        self.message = message

    def check_token(self, token):
        """Check for the presence of desired data in the token.

        Args:
            token (str): Token to search.
        Returns:
            MatchObject if match present, None otherwise.
        """
        regex = re.compile(r'(?P<mentions>^@\w+)|(?P<emoticons>^\(\w{1,15}\)$)|(?P<links>^https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?$)')
        return regex.match(token)

    def parse(self):
        """Return desired information from the message.

        Returns:
            Dict of attributes extracted from the message.
        """
        def map_token(token):
            """Return a tuple with the token type and token.

            Args:
                token (str): Token to search.
            Returns:
                (token_type, token)
            """
            result = self.check_token(token)
            if result:
                if result.groupdict().get('emoticons'):
                    return ('emoticons', self.get_emoticon(token))
                elif result.groupdict().get('mentions'):
                    return ('mentions', self.get_mention(token))
                elif result.groupdict().get('links'):
                    return ('links', self.get_link(token))

        tokens = self.message.split()
        tuples = map(map_token, tokens)
        tuples = filter(lambda x: x is not None, tuples)

        data = {}
        for key, value in tuples:
            self.add_attribute(data, key, value)
        return data

    @staticmethod
    def add_attribute(data, key, value):
        """Store a message attribute.

        Args:
            data (dict): Dict to store the key/value.
            key (str): Type of attribute.
            value (str): Value of attribute extracted from token.
        """
        if key not in data.keys():
            data[key] = list()
        data[key].append(value)

    def get_mention(self, token):
        """Return username from a mention token.

        Args:
            token (str): Token containining mentioned username.
        Returns:
            Username string.
        """
        return re.sub(r'\W+', '', token)

    def get_emoticon(self, token):
        """Return emoticon from an emoticon token.

        Args:
            token (str): Token containing emoticon.
        Returns:
            Emoticon string.
        """
        return token.strip('()')

    def get_link(self, url):
        """Return link metadata including title of the URL.

        Args:
            url (str): HTTP(S) URL to retrieve.
        Returns:
            Dict of URL and page title.
        """
        title = self.get_title(url)
        return {'url': url, 'title': title}

    def get_title(self, url):
        """Return title of the URL.

        Args:
            url (str): HTTP(S) URL to get page title from.
        Returns:
            Title string or None if page not available.
        """
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            return soup.title.string
        except urllib2.URLError:
            return None


def main():
    test_input = '@foo hello world (allthethings) @bar https://example.com\
                  (notbad) ftp://filez.com asdf@asdf.com fake@fake,com\
                  http://google.com https://en.wikipedia.org/wiki/Computer bye!'

    while True:
        input_str = raw_input('>')
        if not input_str:
            input_str = test_input
        message = Message(input_str)
        output = json.dumps(message.parse(), sort_keys=True, indent=2)
        print(output)


if __name__ == '__main__':
    main()
