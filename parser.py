import json
import re


class Message(object):

    def __init__(self, message):
        self.message = message
        self.data = {}

    def parse(self):
        """ TODO: pretty"""
        tokens = self.message.split()
        for token in tokens:
            if token.startswith('@'):
                self.add_mention(token)
            elif token.startswith('(') and token.endswith(')'):
                self.add_emoticon(token)
            elif self.url(token):
                self.add_link(token)
            elif self.email(token):
                self.add_email(token)

        return json.dumps(self.data, sort_keys=True, indent=2)

    def add_mention(self, user):
        if not self.data.get('mentions'):
            self.data['mentions'] = list()
        self.data['mentions'].append(user.lstrip('@'))

    def add_emoticon(self, emoticon):
        if not self.data.get('emoticons'):
            self.data['emoticons'] = list()
        self.data['emoticons'].append(emoticon.strip('()'))

    def add_link(self, url):
        if not self.data.get('links'):
            self.data['links'] = list()
        title = self.get_title(url)
        self.data['links'].append({'url': url, "title": title})

    def url(self, token):
        """Check to see if a token is a url.
        """
        url_prefixes = ['http://', 'https://', 'ftp://', 'ssh://']
        for prefix in url_prefixes:
            if token.startswith(prefix):
                return True
        return False

    def get_title(self, url):
        return None

    def add_email(self, email):
        if not self.data.get('emails'):
            self.data['emails'] = list()
        self.data['emails'].append(email)

    def email(self, token):
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
