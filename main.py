from sredis import Redis


def main():
    client = Redis()
    client['test'] = 'test'
    print(client['test'])


if __name__ == '__main__':
    main()
