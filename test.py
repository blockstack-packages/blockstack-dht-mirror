#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from time import sleep
from pymongo import MongoClient

from basicrpc import Proxy
from pybitcoin import hex_hash160

from mirror.config import DEFAULT_SERVER, DEFAULT_PORT, DEBUG

c = MongoClient()
namespace_db = c['namespace']
btc_state = namespace_db.btc_state


def pretty_print(data):

    try:
        data = data[0]
    except:
        pass

    if type(data) is not dict:
        try:
            data = json.loads(data)
        except Exception as e:
            print e

    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


def get_hash(profile):

    if type(profile) is not dict:
        try:
            print "WARNING: converting to json"
            profile = json.loads(profile)
        except:
            print "WARNING: not valid json"

    return hex_hash160(json.dumps(profile, sort_keys=True))

# ------------------------------
if __name__ == '__main__':

    c = Proxy(DEFAULT_SERVER, DEFAULT_PORT)
    resp = c.ping()
    print pretty_print(resp)

    error_usernames = ['surzayonghosh', 'captaincalliope']

    write_usernames = ['judecn', 'ryan']

    counter = 0

    resp = c.dht_get('dbbdedc2b81d875403cc76486625a19f1e3b3c6f')
    print resp[0]

    fin = open('btc_state_v1.json', 'r')

    data = fin.read()
    data = json.loads(data)

    for entry in data:
    #for entry in btc_state.find(timeout=False):

        if entry['username'] in error_usernames:
            continue

        #if entry['username'] not in write_usernames:
        #    continue

        print entry['username']
        key = entry['profile_hash']
        value = json.dumps(entry['profile'], sort_keys=True)

        #resp = c.dht_get(key)

        #print resp[0]

        #continue

        try:
            resp = c.dht_set(key, value)
            resp = resp[0]

            print entry['username']
            print resp
            counter += 1
            print counter
            print '-' * 5
        except:
            print "problem %s" % entry['username']
            print key
            print value
            break

        #if resp is None:
        #    print"trying set"
        #    print c.dht_set(key, value)

        """

        #print "username: " + username

        try:
            temp = "profile:" + resp
        except Exception as e:
            print resp

        continue

        print "hash of profile (namecoin): " + profile_hash
        print "hash of profile (DHT): " + hex_hash160(resp)

        if hex_hash160(resp) != profile_hash:
            print profile_hash
            print hex_hash160(resp)
        else:
            print "match"

        print "-" * 5

        #resp = c.dht_get(profile_hash)
        #if pretty_print(resp) == "null":
        #    print username
        """