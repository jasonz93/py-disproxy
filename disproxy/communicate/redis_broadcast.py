from .base import BaseBroadcast
import json
import redis

class RedisBroadcast(BaseBroadcast):
    def __init__(self, connUrl, listener):
        super(RedisBroadcast, self).__init__(connUrl, listener)
        opts = {}
        if self.connUrl.hostname:
            opts['host'] = self.connUrl.hostname
        if self.connUrl.port:
            opts['port'] = int(self.connUrl.port)
        self.connPool = redis.ConnectionPool(**opts)
        self.key = self.connUrl.path[1:]
        self.pub = redis.Redis(connection_pool=self.connPool)
        if listener:
            self.sub = self.pub.pubsub()
            self.sub.subscribe(**{self.key: self.onMessage})
            thread = self.sub.run_in_thread(0.01)

    def onMessage(self, data):
        if data['type'] == 'message':
            self.listener(json.loads(data['data']))

    def broadcast(self, msg):
        self.pub.publish(self.key, json.dumps(msg))
