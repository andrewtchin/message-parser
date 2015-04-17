class Message(object):

    def __init__(self, data):
        self.data = data


def main():
    while True:
        data = raw_input('>')
        if data:
            print data
        else:
            break

if __name__ == '__main__':
    main()
