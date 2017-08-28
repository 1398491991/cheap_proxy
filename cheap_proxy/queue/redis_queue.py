

class RedisQueue(object):
    # 先进先出


    def __init__(self,server, key,):

        self._server = server
        self.key = key

    @property
    def server(self):
        return self._server.conn

    def serializer(self,x):
        return x

    def deserialize(self,x):
        return x

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def __next__(self):
        obj = self.pop(10)
        if obj:
            return obj

        raise StopIteration


    def push(self, obj):

        self.server.lpush(self.key, self.serializer(obj))


    def pop(self, timeout=0):

        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(self.key)
        if data:
            return self.deserialize(data)


    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)
