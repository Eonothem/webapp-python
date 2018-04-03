#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Eonothem'

'''
Define URL manipulation functions

connect the ORM frame and the web frame to write the MVC
'''

import time
from coroweb import get, post
import asyncio
from models import User, Comment, Blog, next_id

@get('/')
@asyncio.coroutine
def index(request):
	summary = 'Hello, World.'
	blogs = [
    	Blog(id='1', name='Test Blog', summary=summary, create_at=time.time()-120),
    	Blog(id='2', name='Something New', summary=summary, create_at=time.time()-3600),
    	Blog(id='3', name='Learn Swift', summary=summary, create_at=time.time()-7200)
    ]
	return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }

