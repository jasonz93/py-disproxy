import pymongo
from .communicate import RedisMessageQueue, RedisBroadcast
import urlparse
import logging
from bson import ObjectId

class DisproxyClient(object):
    logger = logging

    def __init__(self, mongodb='mongodb://localhost/disproxy'
                 , message_queue='redis://localhost/disproxy_mq'
                 , broadcast='redis://localhost/disproxy_broadcast'
                 , internal=True
                ):
        self.mongo = pymongo.MongoClient(mongodb)
        self.db = self.mongo.get_default_database()
        self.mq = RedisMessageQueue(message_queue)
        self.broadcast = RedisBroadcast(broadcast, self.onMessage)
        self.internal = internal
        self.proxy_nodes = {}
        self.current = 0
        for proxy in self.db.proxies.find():
            node = ProxyNode(proxy, self)
            self.proxy_nodes[node.id] = node

    def getProxy(self, url):
        proxyIds = self.proxy_nodes.keys()
        if len(proxyIds) == 0:
            self.logger.error("Local proxy pool is empty.")
            return None
        parsedUrl = urlparse.urlparse(url)
        host = parsedUrl.hostname
        for tries in range(0, len(proxyIds)):
            if self.current >= len(proxyIds):
                self.current = 0
            node = self.proxy_nodes[proxyIds[self.current]]
            self.current += 1
            if host in node.bans:
                continue
            else:
                return node
        self.logger.error("All proxies has been ban for this host. %s", host)
        return None

    def onMessage(self, msg):
        type = msg['type']
        if type == 'PROXY_ONLINE':
            proxy = self.db.proxies.find_one(ObjectId(msg['proxy_id']))
            if proxy:
                self.proxy_nodes[msg['proxy_id']] = ProxyNode(proxy, self)
            else:
                self.logger.error('New onlined proxy does not exist in mongo.')
        elif type == 'PROXY_OFFLINE':
            del self.proxy_nodes[msg['proxy_id']]
        elif type == 'BAN_NOTIFY':
            proxy = self.proxy_nodes[msg['proxy_id']]
            if proxy:
                proxy.bans.append(msg['host'])
                self.logger.debug("Proxy %s ban for %s", msg['proxy_id'], msg['host'])
            else:
                self.logger.error("Cannot find ban proxy in local cache. ID: %s", msg['proxy_id'])

class ProxyNode(object):
    def __init__(self, doc, client):
        self.id = str(doc['_id'])
        self.client = client
        self.url = "%s://%s:%d"%(doc['protocol'], doc['internal_ip'] if self.client.internal else doc['external_ip'], doc['port'])
        self.bans = doc['bans']

    def ban(self, url):
        parsedUrl = urlparse.urlparse(url)
        host = parsedUrl.hostname
        if host not in self.bans:
            self.bans.append(host)
        self.client.mq.send({
            'type': 'BAN_REQUEST',
            'proxy_id': self.id,
            'url': url
        })

    def broken(self):
        self.client.mq.send({
            'type': 'PROXY_BROKEN_REQUEST',
            'proxy_id': self.id
        })

    def __str__(self):
        return self.url