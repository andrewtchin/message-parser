import json
import re


def ensure_key(func):
    def wrapper(*args):
        key = args[1]
        if not args[0].data.get(key):
            args[0].data[key] = list()
        return func(*args)
    return wrapper


class Message(object):

    def __init__(self, message):
        self.message = message
        self.data = {}

    def parse_string(self, tokens):
        for token in tokens:
            if token.startswith('@'):
                # re.match(r'^@\w+$', token)
                self.add_attribute('mentions', self.get_mention(token))
            elif token.startswith('(') and token.endswith(')'):
                # re.match(r'^\(\w+\)$', emoticon)
                self.add_attribute('emoticons', self.get_emoticon(token))
            elif self.check_url(token):
                # https://daringfireball.net/2010/07/improved_regex_for_matching_urls
                # re.match(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:".,<>?]))', url)
                self.add_attribute('links', self.get_link(token))
            elif self.check_email(token):
                # re.match(r'[^@]+@[^@]+\.[^@]+', token)
                self.add_attribute('emails', token)

    def parse_re(self, tokens):
        # https://rushi.wordpress.com/2008/04/14/simple-regex-for-matching-urls/
        regex = re.compile(r'(?P<mention>^@\w+$)|(?P<emoticon>^\(\w+\)$)|(?P<url>^https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?$)')
        for token in tokens:
            result = regex.match(token)
            if result:
                if result.get('emoticon'):
                    self.add_attribute('emoticons', self.get_emoticon(token))
                elif result.get('mention'):
                    self.add_attribute('mentions', self.get_mention(token))
                elif result.get('url'):
                    self.add_attribute('links', self.get_link(token))

    def parse(self):
        tokens = self.message.split()
        self.parse_re(tokens)
        return json.dumps(self.data, sort_keys=True, indent=2)

    @ensure_key
    def add_attribute(self, key, value):
        self.data[key].append(value)

    def get_mention(self, token):
        return token.lstrip('@')

    def get_emoticon(self, token):
        return token.strip('()')

    def get_link(self, url):
        title = self.get_title(url)
        return {'url': url, "title": title}

    def check_url(self, token):
        """Check to see if a token is a url.
        """
        url_prefixes = ['http://', 'https://', 'ftp://', 'ssh://']
        for prefix in url_prefixes:
            if token.startswith(prefix):
                return True
        return False

    def get_title(self, url):
        return None

    def check_email(self, token):
        if re.match(r"[^@]+@[^@]+\.[^@]+", token):
            return True
        return False


def main():
    test_input = '@foo hello world (allthethings) @bar https://example.com\
                  (notbad) ftp://filez.com bye! asdf@asdf.com fake@fake,com'

    while True:
        input = raw_input('>')
        if not input:
            input = test_input
        message = Message(input)
        output = message.parse()
        print(output)


if __name__ == '__main__':
    main()
