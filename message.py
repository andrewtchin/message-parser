"""This module extracts information from a message string."""

import json
import re
import urllib2

from bs4 import BeautifulSoup


class Message(object):
    """This class parses a message and finds mentions, emoticons, and links.

    Truncates messages longer than Message.MAX_MESSAGE_LEN.
    Attributes to extract are defined by Message.ATTR_REGEX.

    Attributes:
        message (str): Contents of the message.
    """
    MAX_MESSAGE_LEN = 1000000
    MENTIONS_REGEX = re.compile(r"(?:^| )@(\w+)")
    EMOTICONS_REGEX = re.compile(r"\((\w{1,15})\)")
    LINKS_REGEX = re.compile(r"(https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)")

    def __init__(self, message=''):
        if len(message) > Message.MAX_MESSAGE_LEN:
            self.message = message[:Message.MAX_MESSAGE_LEN]
        else:
            self.message = message

    def search(self, key, regex, result):
        """Search message for regex matches and store result.

        Args:
            key (str): key to store matches.
            regex (compiled re): regex to search for.
            result (dict): store match list at key.
        """
        matches = regex.findall(self.message)
        if matches:
            result[key] = matches

    def parse(self):
        """Return desired information from the message.

        Find mentions, emoticons, and HTTP(S) URLs.

        Returns:
            Dict of attributes extracted from the message.
        """
        result = {}
        searches = [('mentions', Message.MENTIONS_REGEX),
                    ('emoticons', Message.EMOTICONS_REGEX),
                    ('links', Message.LINKS_REGEX)]

        for key, regex in searches:
            self.search(key, regex, result)

        if result.get('links'):
            links = [self.get_link(match[0]) for match in result['links']]
            result['links'] = links

        return result

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
