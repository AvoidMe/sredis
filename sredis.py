import redis


# TODO: check difference between Strict and default Redis
class Redis(redis.StrictRedis):

    def __init__(self, *args, **kwargs):
        kwargs['decode_responses'] = True
        super().__init__(*args, **kwargs)
        self.flushdb()

    def __getitem__(self, key):
        typeinfo = self.type(key)
        if typeinfo == 'string':
            return self.get(key)
        elif typeinfo == 'list':
            return PyRedisList(self, key)
        elif typeinfo == 'set':
            return PyRedisSet(self, key)
        elif typeinfo == 'hash':
            return PyRedisDict(self, key)

    def __setitem__(self, key, value):
        if isinstance(value, list):
            self.rpush(key, *value)
        elif isinstance(value, set):
            self.sadd(key, *value)
        else:
            self.set(key, value)


class PyRedisList:

    def __init__(self, connection, key):
        self.connection = connection
        self.key = key

    def __len__(self):
        return self.connection.llen(self.key)

    # TODO: can be slice too!
    def __getitem__(self, index):
        return self.connection.lindex(self.key, index)

    # TODO: can be slice too!
    def __setitem__(self, index, value):
        self.connection.lset(self.key, index, value)

    # TODO:
    # def __iter__
    # def append
    # def clear
    # def copy
    # def count
    # def extend
    # def index
    # def insert
    # def pop
    # def remove
    # def reverse
    # def sort


class PyRedisDict(dict):
    pass


class PyRedisSet(set):
    pass
