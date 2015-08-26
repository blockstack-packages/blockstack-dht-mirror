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

from config import DEFAULT_SERVER, DEFAULT_PORT, DEBUG


def format_response(response):

    response = response[0]
    return json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

# ------------------------------
if __name__ == '__main__':

    c = Proxy(DEFAULT_SERVER, DEFAULT_PORT)
    resp = c.ping()
    print format_response(resp)

    key = {"name": "Muneeb Ali"}

    resp = c.dht_get(key)
    print format_response(resp)
