"""This module extracts information from a message string."""

from collections import defaultdict
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
    ATTR_REGEX = re.compile(r"^@(?P<mentions>\w+)"
                            r"|\((?P<emoticons>\w{1,15})\)"
                            r"|(?P<links>https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)")

    def __init__(self, message=''):
        if len(message) > Message.MAX_MESSAGE_LEN:
            self.message = message[:Message.MAX_MESSAGE_LEN]
        else:
            self.message = message

    def parse(self):
        """Return desired information from the message.

        Find mentions, emoticons, and HTTP(S) URLs.

        Returns:
            Dict of attributes extracted from the message.
        """
        matched_groupdicts = [match.groupdict()
                              for match in Message.ATTR_REGEX.finditer(self.message)]

        result = defaultdict(set)
        for match_dict in matched_groupdicts:
            for key, value in match_dict.iteritems():
                if value is not None:
                    result[key].add(value)

        # Convert sets of tokens to lists of tokens.
        result = {key: list(value) for key, value in result.iteritems()}

        if result.get('links'):
            enhanced_links = []
            for link in result['links']:
                enhanced_links.append(self.get_link(link))
            result['links'] = enhanced_links

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
