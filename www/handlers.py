#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Eonothem'

'''
Define URL manipulation functions
'''

import asyncio
from coroweb import get, post

@get('/')
@asyncio.coroutine
def handler_url_blog(request):
	body = '<h1>Awesome</h1>'
	return body

@get('/greeting')
@asyncio.coroutine
def handler_url_greeting(*, name, request):
	body = '<h1>Awesome: /greeting %s</h1>'%name
	return body

