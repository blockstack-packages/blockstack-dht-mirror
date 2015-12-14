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
from txjsonrpc.netstring import jsonrpc
from kademlia.log import Logger

from twisted.internet import protocol
from pybitcoin import hex_hash160
from threading import Thread

from pymongo import MongoClient
c = MongoClient()
db = c['dht-mirror']
dht_mirror = db.dht_mirror


def write_to_cache(key, value):

    new_entry = {}
    new_entry['key'] = key
    new_entry['value'] = value

    try:
        entry = dht_mirror.find_one({"key": key})
    except:
        self.log.info("Error on %s" % key)

    if entry is None:
        self.log.info("Writing new entry %s" % key)
        dht_mirror.insert(new_entry)
    else:
        self.log.info("Entry already in mirror")


class DHTMirrorRPC(jsonrpc.JSONRPC):
    """ A DHT Mirror with faster get/set."""

    def _get_hash(self, value):

        if type(value) is not dict:
            try:
                #self.log.info("WARNING: converting to json")
                value = json.loads(value)
            except:
                self.log.info("WARNING: not valid json")

        return hex_hash160(json.dumps(value, sort_keys=True))

    def __init__(self, dht_server=None):
        self.dht_server = dht_server
        self.log = Logger(system=self)

    def jsonrpc_ping(self):

        reply = {}
        reply['status'] = "alive"
        return reply

    def jsonrpc_stats(self):
        stats = {}
        stats['entries'] = dht_mirror.count()
        return stats

    def jsonrpc_get(self, key):

        resp = {}
        resp['key'] = key

        self.log.info("Get request for key: %s" % key)

        entry = dht_mirror.find_one({"key": key})

        if entry is not None:
            resp['value'] = entry['value']
        else:
            # if not in mirror/cache get from DHT
            return self.jsonrpc_dht_get(key)

        return resp

    def jsonrpc_set(self, key, value):

        self.log.info("Set request for key: %s" % key)

        resp = {}

        test_hash = self._get_hash(value)

        if test_hash != key:
            resp['error'] = "hash(value) doesn't match key"
            return resp

        write_to_cache(key, value)

        # perform the dht set/refresh in the background
        self.jsonrpc_dht_set(key, value)

        resp['status'] = 'success'

        return resp

    def jsonrpc_dht_get(self, key):

        self.log.info("DHT get request for key: %s" % key)

        resp = {}

        try:
            resp = self.dht_server.get(key)
            value = resp[0]
            write_to_cache(key, value)

        except Exception as e:
            resp['error'] = e

        return resp

    def jsonrpc_dht_set(self, key, value):

        self.log.info("DHT set request for key: %s" % key)

        resp = {}

        try:
            resp = self.dht_server.set(key, value)
        except Exception as e:
            resp['error'] = e

        return resp
