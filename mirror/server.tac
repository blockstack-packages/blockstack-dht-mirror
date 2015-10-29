#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    DHT-Mirror
    ~~~~~

    copyright: (c) 2015 by Blockstack.org

This file is part of DHT-Mirror.

    DHT-Mirror is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    DHT-Mirror is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with DHT-Mirror. If not, see <http://www.gnu.org/licenses/>.
"""


from txjsonrpc.netstring import jsonrpc
from twisted.application import service, internet

from mirror.server import DHTMirrorRPC

from kademlia.network import Server
from blockstore.dht.storage import BlockStorage, hostname_to_ip

from mirror.config import DEFAULT_DHT_SERVERS
from mirror.config import DHT_UDP_PORT, MIRROR_TCP_PORT
from mirror.config import MAX_LENGTH

application = service.Application("dht-mirror")

# now setup the kademlia node
dht_server = Server(storage=BlockStorage())
bootstrap_servers = hostname_to_ip(DEFAULT_DHT_SERVERS)
bootstrap_servers = ['52.20.98.85']
dht_server.bootstrap(bootstrap_servers)

factory_dhtmirror = jsonrpc.RPCFactory(DHTMirrorRPC(dht_server), maxLength=MAX_LENGTH)

server_dhtmirror = internet.TCPServer(MIRROR_TCP_PORT, factory_dhtmirror)
server_dhtmirror.setServiceParent(application)


server_dht = internet.UDPServer(DHT_UDP_PORT, dht_server.protocol)
server_dht.setServiceParent(application)
