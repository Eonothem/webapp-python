#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Eonothem'

'''
aysnc web application.
'''

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

def index(request):
	return web.Response(body=b'<h1>Awesome<\h1>')

@asyncio.coroutine#to sign a generator as a coroutine an put it into a eventloop
def init(loop):
	app = web.Application(loop=loop)#to build a http server through aiohttp
	app.router.add_route('GET', '/', index)
	srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
	logging.info('server started at http://127.0.0.1:9000...')
	return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()