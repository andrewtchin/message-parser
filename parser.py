import json


class Message(object):

    def __init__(self, message):
        self.message = message
        self.data = None

    def parse(self):
        return json.dumps(self.data, sort_keys=True, indent=2)

    def mention(self, user):
        pass

    def emoticon(self, emoticon):
        pass

    def link(self, url):
        pass


def main():
    while True:
        input = raw_input('>')
        if input:
            message = Message(input)
            output = message.parse()
            print(output)
        else:
            break

if __name__ == '__main__':
    main()
