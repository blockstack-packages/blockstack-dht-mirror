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

DEBUG = True

DEFAULT_SERVER = '127.0.0.1'

DHT_UDP_PORT = 6265  # blockstored defaults to port 6264
MIRROR_TCP_PORT = 6266

DEFAULT_DHT_SERVERS = [('dht.blockstack.org', DHT_UDP_PORT),
                       ('dht.onename.com', DHT_UDP_PORT),
                       ('dht.halfmoonlabs.com', DHT_UDP_PORT),
                       ('127.0.0.1', DHT_UDP_PORT)]

# see rpcudp/protocol.py
MAX_LENGTH = 8 * 1024
