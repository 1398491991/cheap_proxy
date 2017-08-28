#coding=utf8

class RedisQueue(object):
    # 先进先出


    def __init__(self,
                 server,
                 key,
                 serialize,
                 deserialize,
                 verify_idle_time_out = 10):

        self._server = server
        self.key = key

        self.serialize = serialize
        self.deserialize = deserialize

        self.verify_idle_time_out = verify_idle_time_out


    @property
    def server(self):
        return self._server.conn

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def __next__(self):
        obj = self.pop(self.verify_idle_time_out)
        if obj:
            return obj

        # 迭代完毕
        raise StopIteration()

    next = __next__  # 为了兼容 py2

    def __iter__(self):
        return self


    def push(self, obj):

        self.server.lpush(self.key, self.serialize(obj))


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

    def __str__(self):
        return 'server %s, key %s'%(self.server,self.key)
