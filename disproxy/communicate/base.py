import urlparse

class BaseBroadcast(object):
    def __init__(self, connUrl, listener):
        self.connUrl = urlparse.urlparse(connUrl)
        self.listener = listener

    def broadcast(self, msg):
        raise NotImplementedError

class BaseMessageQueue(object):
    def __init__(self, connUrl, listener):
        self.connUrl = urlparse.urlparse(connUrl)
        self.listener = listener

    def send(self, msg):
        raise NotImplementedError