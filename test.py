#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from time import sleep
from pymongo import MongoClient

from basicrpc import Proxy

from mirror.config import DEFAULT_SERVER, MIRROR_TCP_PORT, DEBUG

CACHE_FILENAME = 'btc_state_v1.json'

from pymongo import MongoClient
c = MongoClient()
db = c['dht-mirror']
dht_mirror = db.dht_mirror


def pretty_print(data):

    try:
        data = data[0]
    except:
        pass

    if type(data) is not dict:
        try:
            data = json.loads(data)
        except Exception as e:
            print "got here"
            print e

    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


def warmup_mirror():
    fin = open(CACHE_FILENAME, 'r')

    data = fin.read()
    data = json.loads(data)

    counter = 0

    error_usernames = ['surzayonghosh', 'captaincalliope']

    checked_names = []

    for entry in data:

        if entry['username'] in error_usernames:
            continue

        print entry['username']
        key = entry['profile_hash']
        value = json.dumps(entry['profile'], sort_keys=True)

        resp = c.get(key)
        pretty_print(resp)
        continue

        try:
            resp = c.set(key, value)
            pretty_print(resp)
            counter += 1
            print counter
            print '-' * 5
        except Exception as e:
            print e
            print "problem %s" % entry['username']
            print key
            print value
            break

        #if resp is None:
        #    print"trying set"
        #    print c.dht_set(key, value)

# ------------------------------
if __name__ == '__main__':

    test_hash = "3b04c220530154898d02463fba83a235de184936"

    c = Proxy(DEFAULT_SERVER, MIRROR_TCP_PORT, timeout=30)
    pretty_print(c.ping())
    #pretty_print(c.stats())
    result = c.dht_get(test_hash)
    print result
    #pretty_print(result)
    #warmup_mirror()