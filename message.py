"""This module extracts information from a message string."""

import json
import re
import urllib2

from bs4 import BeautifulSoup


class Message(object):
    """This class parses a message and finds selected message attributes.

    Truncates messages longer than Message.MAX_MESSAGE_LEN.

    Attributes:
        message (str): Contents of the message.
    """
    MAX_MESSAGE_LEN = 1000000

    def __init__(self, message=''):
        if len(message) > Message.MAX_MESSAGE_LEN:
            self.message = message[:Message.MAX_MESSAGE_LEN]
        else:
            self.message = message

    @staticmethod
    def check_token(token):
        """Check for the presence of desired data in the token.

        Searches for mentions, emoticons, and HTTP(S) links.

        Args:
            token (str): Token to search.
        Returns:
            MatchObject if match present, None otherwise.
        """
        regex = re.compile(r"(?P<mentions>^@\w+)|"
                           r"(?P<emoticons>.*\(\w{1,15}\).*)|"
                           r"(?P<links>^https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?$)")
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
        tuples = [x for x in tuples if x is not None]

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

    @staticmethod
    def get_mention(token):
        """Return username from a mention token.

        Mention token starts with '@' and ends with non-alphanumeric
        character.

        Args:
            token (str): Token containining mentioned username.
        Returns:
            Username string.
        """
        subtokens = re.findall(r'\w+', token)
        return subtokens[0]

    @staticmethod
    def get_emoticon(token):
        """Return the first emoticon from an emoticon token.

        Emoticon is alphanumeric characters enclosed by parenthesis.

        Args:
            token (str): Token containing emoticon.
        Returns:
            Emoticon string.
        """
        emoticon_start = token.split('(')
        emoticon_end = emoticon_start[1].split(')')
        return emoticon_end[0]

    def get_link(self, url):
        """Return link metadata including title of the URL.

        Args:
            url (str): HTTP(S) URL to retrieve.
        Returns:
            Dict of URL and page title.
        """
        title = self.get_title(url)
        return {'url': url, 'title': title}

    @staticmethod
    def get_title(url):
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

    def to_json(self):
        """Parse message and return JSON of extracted message attributes.

        Returns:
            JSON of extracted message attributes.
        """
        return json.dumps(self.parse(), sort_keys=True, indent=2)


def main():
    """Parse input from stdin as a Message to extract attributes."""
    while True:
        input_str = raw_input('>')
        message = Message(input_str)
        output = message.to_json()
        print output


if __name__ == '__main__':
    main()
