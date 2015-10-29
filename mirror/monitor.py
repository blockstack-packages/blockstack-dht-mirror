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

import json

from basicrpc import Proxy

from .utils import pretty_print

from .config import DEFAULT_SERVER, MIRROR_TCP_PORT, DEBUG
from .config import DHT_STATE_FILE

dht_client = Proxy(DEFAULT_SERVER, MIRROR_TCP_PORT, timeout=30)


def refresh_dht_entries():

    fin = open(DHT_STATE_FILE, 'r')

    data = fin.read()
    data = json.loads(data)

    counter = 0

    for entry in data:

        print '-' * 5
        print "Processing key: %s" % entry['key']
        key = entry['key']
        value = entry['value']
        print "(%s, %s)" % (key, value)

        try:
            dht_client = Proxy(DEFAULT_SERVER, MIRROR_TCP_PORT, timeout=5)
            resp = dht_client.dht_set(key, value)
            print resp
            counter += 1
            print counter
            print '-' * 5
        except Exception as e:
            print e
            print "Problem with key: %s" % key

# ------------------------------
if __name__ == '__main__':

    pretty_print(dht_client.ping())
    #pretty_print(c.stats())
    refresh_dht_entries()
