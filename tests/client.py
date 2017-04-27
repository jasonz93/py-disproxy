from disproxy import DisProxy
import unittest2 as unittest
import logging

logging.basicConfig(level=logging.DEBUG)

class ClientTest(unittest.TestCase):
    def testClient(self):
        client = DisProxy(internal=False)
        print client.proxy_nodes
        proxy = client.getProxy('http://www.baidu.com')
        print proxy
        proxy.ban('http://www.baidu.com')