from disproxy.communicate.redis_broadcast import RedisBroadcast
import unittest2 as unittest
import time
import threading
class RedisBroadcastTest(unittest.TestCase):
    def test_broadcast_listen(self):
        def listener(msg):
            print 'received in ', threading.currentThread().ident
            print msg
        broadcast = RedisBroadcast('redis://localhost/disproxy_broadcast', listener)
        broadcast.broadcast({'foo': 'bar'})
        broadcast.broadcast({'foo': 'bar'})
        time.sleep(1)
        print 'broadcast in ', threading.currentThread().ident