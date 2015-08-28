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

from pymongo import MongoClient
db = MongoClient()
dht_mirror = db.dht_mirror


class DHTMirrorRPC(jsonrpc.JSONRPC):
    """ A DHT Mirror with faster get/set."""

    def __init__(self, dht_server=None):
        self.dht_server = dht_server

    def jsonrpc_ping(self):
        reply = {}
        reply['status'] = "alive"
        return reply

    def jsonrpc_stats(self):
        stats = {}
        return stats

    def jsonrpc_get(self, key):

        entry = dht_mirror.find_one({"key": key})

        if entry is not None:
            return entry['value']
        else:
            return None

    def jsonrpc_set(self, key, value):

        new_entry = {}
        new_entry['key'] = key
        new_entry['value'] = value

        entry = dht_mirror.find_one({"key": key})

        if entry is not None:
            dht_mirror.insert(new_entry)
        else:
            entry['value'] = value
            dht_mirror.save(entry)

        return True

    def jsonrpc_dht_get(self, key):

        resp = {}

        try:
            resp = self.dht_server.get(key)
        except Exception as e:
            resp['error'] = e

        return resp

    def jsonrpc_dht_set(self, key, value):

        print "got here"

        resp = {}

        try:
            resp = self.dht_server.set(key, value)
        except Exception as e:
            resp['error'] = e

        return resp
