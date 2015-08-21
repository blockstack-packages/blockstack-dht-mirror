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

import zerorpc
from blockstore.client import BlockstoreRPCClient

from config import DEFAULT_URI, DEBUG, SERVER_IP, SERVER_PORT

from pymongo import MongoClient
db = MongoClient().get_default_database()
dht_mirror = db.dht_mirror


class DHTMirror(object):
    """ A DHT Mirror with faster get/set."""

    def get(self, key):

        entry = dht_mirror.find_one({"key": key})

        if entry is not None:
            return entry['value']
        else:
            return None

    def set(self, key, value):

        new_entry = {}
        new_entry['key'] = key
        new_entry['value'] = value

        entry = dht_mirror.find_one({"key": key})

        if entry is not None:
            dht_mirror.insert(new_entry)
        else:
            entry['value'] = value
            dht_mirror.save()

        return True

    def stats(self, sentence):
        stats = {}
        return stats

    def dht_get(key):

        blockstored = BlockstoreRPCClient(SERVER_IP, SERVER_PORT)

        resp = {}

        try:
            resp = blockstored.get(key)
        except Exception as e:
            resp['error'] = e

        return resp

    def dht_set(key, value):

        blockstored = BlockstoreRPCClient(SERVER_IP, SERVER_PORT)

        resp = {}

        try:
            resp = blockstored.set(key, value)
        except Exception as e:
            resp['error'] = e

        return resp


# ------------------------------
def runserver():

    s = zerorpc.Server(DHTMirror())
    s.bind(DEFAULT_URI)
    s.run()


# ------------------------------
if __name__ == '__main__':

    runserver()
