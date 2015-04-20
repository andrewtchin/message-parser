"""
This module extracts information from a message string.
"""

import json
import re
import urllib2

from bs4 import BeautifulSoup


class Message(object):
    """
    This class parses a message and stores selected message attributes.

    Attributes:
        message (str): Contents of the message.
        data (dict): Attributes extracted from the message.
    """

    def __init__(self, message):
        self.message = message
        self.data = {}

    def check_token(self, token):
        """Check for the presence of desired data in the token.

        Args:
            token (str): Token to search.
        Returns:
            MatchObject if match present, None otherwise.
        """
        regex = re.compile(r'(?P<mentions>^@\w+$)|(?P<emoticons>^\(\w+\)$)|(?P<links>^https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?$)')
        return regex.match(token)

    def parse(self):
        """Extract desired information from the message."""
        tokens = self.message.split()
        for token in tokens:
            result = self.check_token(token)
            if result:
                if result.groupdict().get('emoticons'):
                    self.add_attribute('emoticons', self.get_emoticon(token))
                elif result.groupdict().get('mentions'):
                    self.add_attribute('mentions', self.get_mention(token))
                elif result.groupdict().get('links'):
                    self.add_attribute('links', self.get_link(token))

    def add_attribute(self, key, value):
        """Store a message attribute.

        Args:
            key (str): Type of attribute.
            value (str): Value of attribute extracted from token.
        """
        if not self.data.get(key):
            self.data[key] = list()
        self.data[key].append(value)

    def get_mention(self, token):
        """Return username from a mention token.

        Args:
            token (str): Token containining mentioned username.
        Returns:
            Username string.
        """
        return token.lstrip('@')

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
        return {'url': url, "title": title}

    def get_title(self, url):
        """Return title of the URL.

        Args:
            url (str): HTTP(S) URL to get page title from.
        Returns:
            Title string.
        """
        page = BeautifulSoup(urllib2.urlopen(url))
        return page.title.string

    def to_json(self):
        """Return JSON representation of message attributes.

        Returns:
            JSON of message attributes.
        """
        self.parse()
        return json.dumps(self.data, sort_keys=True, indent=2)


def main():
    test_input = '@foo hello world (allthethings) @bar https://example.com\
                  (notbad) ftp://filez.com asdf@asdf.com fake@fake,com\
                  http://google.com https://en.wikipedia.org/wiki/Computer bye!'

    while True:
        input = raw_input('>')
        if not input:
            input = test_input
        message = Message(input)
        output = message.to_json()
        print(output)


if __name__ == '__main__':
    main()
