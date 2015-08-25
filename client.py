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

import jsonrpc_ns
import json

from config import DEFAULT_SERVER, DEFAULT_PORT, DEBUG


# ------------------------------
if __name__ == '__main__':

    from jsonrpc_ns import JSONRPCProxy
    jsonrpc = JSONRPCProxy(DEFAULT_SERVER, DEFAULT_PORT)
    resp = jsonrpc.request('ping')
    print resp

    key = {"name": "Muneeb Ali"}

    resp = jsonrpc.request('dht_get', key)
    print resp
