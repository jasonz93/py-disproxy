from .base import BaseMessageQueue
import redis
import json

class RedisMessageQueue(BaseMessageQueue):
    def __init__(self, connUrl, listener=None):
        super(RedisMessageQueue, self).__init__(connUrl, listener)
        opts = {}
        if self.connUrl.hostname:
            opts['host'] = self.connUrl.hostname
        if self.connUrl.port:
            opts['port'] = int(self.connUrl.port)
        self.redis = redis.Redis(**opts)
        self.key = self.connUrl.path[1:]

    def send(self, msg):
        self.redis.rpush(self.key, json.dumps(msg))
