import json


class Message(object):

    def __init__(self, message):
        self.message = message
        self.data = None

    def parse(self):
        tokens = self.message.split()
        for token in tokens:
            if token.startswith('@'):
                self.mention(token)
            elif token.startswith('(') and token.endswith(')'):
                self.emoticon(token)
            elif self.url(token) == True:
                self.link(token)

        return json.dumps(self.data, sort_keys=True, indent=2)

    def mention(self, user):
        print('mention: {}'.format(user))

    def emoticon(self, emoticon):
        print('emoticon: {}'.format(emoticon))

    def link(self, url):
        print('url: {}'.format(url))

    def url(self, token):
        """Check to see if a token is a url."""
        url_prefixes = ['http://', 'https://', 'ftp://', 'ssh://']
        for prefix in url_prefixes:
            if token.startswith(prefix):
                return True
        return False


def main():
    test_input = '@foo hello world (allthethings) bar https://example.com bye! asdf@asdf.com'

    while True:
        input = raw_input('>')
        if not input:
            input = test_input
        message = Message(input)
        output = message.parse()
        print(output)


if __name__ == '__main__':
    main()
