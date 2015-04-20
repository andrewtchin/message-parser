import json
import re
import urllib2

from bs4 import BeautifulSoup


class Message(object):

    def __init__(self, message):
        self.message = message
        self.data = {}

    def parse_regex(self, token):
        regex = re.compile(r'(?P<mentions>^@\w+$)|(?P<emoticons>^\(\w+\)$)|(?P<links>^https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?$)')
        return regex.match(token)

    def parse(self):
        tokens = self.message.split()
        for token in tokens:
            result = self.parse_regex(token)
            if result:
                if result.groupdict().get('emoticons'):
                    self.add_attribute('emoticons', self.get_emoticon(token))
                elif result.groupdict().get('mentions'):
                    self.add_attribute('mentions', self.get_mention(token))
                elif result.groupdict().get('links'):
                    self.add_attribute('links', self.get_link(token))

        return json.dumps(self.data, sort_keys=True, indent=2)

    def add_attribute(self, key, value):
        if not self.data.get(key):
            self.data[key] = list()
        self.data[key].append(value)

    def get_mention(self, token):
        return token.lstrip('@')

    def get_emoticon(self, token):
        return token.strip('()')

    def get_link(self, url):
        title = self.get_title(url)
        return {'url': url, "title": title}

    def get_title(self, url):
        page = BeautifulSoup(urllib2.urlopen(url))
        return page.title.string


def main():
    test_input = '@foo hello world (allthethings) @bar https://example.com\
                  (notbad) ftp://filez.com asdf@asdf.com fake@fake,com\
                  http://google.com https://en.wikipedia.org/wiki/Computer bye!'

    while True:
        input = raw_input('>')
        if not input:
            input = test_input
        message = Message(input)
        output = message.parse()
        print(output)


if __name__ == '__main__':
    main()
